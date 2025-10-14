import logging
from datetime import datetime, timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlmodel import Session

from app.core.config import settings
from app.core.database import get_session
from app.core.security import create_access_token, create_refresh_token, verify_token
from app.crud import authenticate_user, get_user_by_username
from app.models import User

logger = logging.getLogger("auth")

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


def _create_auth_response(user: User) -> dict[str, Any]:
    """创建统一的认证响应"""
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.username, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(subject=user.username)

    return {
        "success": True,
        "data": {
            "username": user.username,
            "nickname": user.full_name or user.username,
            "roles": ["admin"] if user.is_superuser else ["user"],
            "permissions": ["*:*:*"] if user.is_superuser else [],
            "accessToken": access_token,
            "refreshToken": refresh_token,
            "expires": datetime.utcnow() + access_token_expires,
            "avatar": ""
        }
    }


@router.post("/login")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
) -> dict[str, Any]:
    """OAuth2兼容的登录接口，使用form格式"""
    logger.info(f"Form login attempt: {form_data.username}")

    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        logger.warning(f"Form login failed: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    logger.info(f"Form login successful: {user.username} (superuser: {user.is_superuser})")
    return _create_auth_response(user)


@router.post("/sessions")
def create_session(
    login_data: LoginRequest,
    session: Session = Depends(get_session)
) -> dict[str, Any]:
    """创建用户会话（JSON格式登录）"""
    logger.info(f"JSON login attempt: {login_data.username}")

    user = authenticate_user(session, login_data.username, login_data.password)
    if not user:
        logger.warning(f"JSON login failed: {login_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    logger.info(f"JSON login successful: {user.username} (superuser: {user.is_superuser})")
    return _create_auth_response(user)




@router.post("/refresh-token")
def refresh_token(
    refresh_data: RefreshTokenRequest,
    session: Session = Depends(get_session)
) -> dict[str, Any]:
    """使用刷新令牌获取新的访问令牌"""
    logger.info("Refresh token request received")

    # 验证刷新令牌
    payload = verify_token(refresh_data.refresh_token, expected_type="refresh")
    if not payload:
        logger.warning("Invalid refresh token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的刷新令牌",
            headers={"WWW-Authenticate": "Bearer"},
        )

    username = payload.get("sub")
    if not username:
        logger.warning("Refresh token missing subject")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的刷新令牌",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 验证用户是否存在
    user = get_user_by_username(session, username)
    if not user:
        logger.warning(f"User not found for refresh token: {username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 生成新的访问令牌和刷新令牌
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.username, expires_delta=access_token_expires
    )
    new_refresh_token = create_refresh_token(subject=user.username)

    logger.info(f"Token refreshed successfully for user: {user.username}")

    return {
        "success": True,
        "data": {
            "accessToken": access_token,
            "refreshToken": new_refresh_token,
            "expires": datetime.utcnow() + access_token_expires
        }
    }
