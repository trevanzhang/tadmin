
from datetime import datetime
import secrets
import string
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, func
from typing import Optional, Dict, Any

from app.api.deps import get_current_active_user
from app.core.database import get_session
from app.core.security import get_password_hash
from app.crud import create_user, get_user, get_users, update_user
from app.models import User, UserCreate, UserRead, UserUpdate, Role

router = APIRouter()


@router.get("/")
def read_users(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = Query(None, description="搜索用户名、邮箱或姓名"),
    is_active: Optional[bool] = Query(None, description="筛选用户状态"),
    role_name: Optional[str] = Query(None, description="筛选角色"),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
) -> Dict[str, Any]:
    # 检查权限：只有管理员可以查看用户列表
    if not current_user.has_permission("user:read"):
        raise HTTPException(status_code=403, detail="权限不足")

    # 构建基础查询
    count_statement = select(func.count(User.id)).join(User.roles, isouter=True)
    statement = select(User).join(User.roles, isouter=True).distinct()

    # 搜索条件
    if search:
        search_condition = (
            (User.username.contains(search)) |
            (User.email.contains(search)) |
            (User.full_name.contains(search))
        )
        statement = statement.where(search_condition)
        count_statement = count_statement.where(search_condition)

    # 状态筛选
    if is_active is not None:
        statement = statement.where(User.is_active == is_active)
        count_statement = count_statement.where(User.is_active == is_active)

    # 角色筛选
    if role_name:
        statement = statement.where(Role.name == role_name)
        count_statement = count_statement.where(Role.name == role_name)

    # 获取总数
    total = session.exec(count_statement).one()

    # 分页和排序
    statement = statement.offset(skip).limit(limit).order_by(User.created_at.desc())

    users = session.exec(statement).all()

    return {
        "data": [user.to_read() for user in users],
        "total": total,
        "skip": skip,
        "limit": limit
    }


@router.post("/", response_model=UserRead)
def create_new_user(
    user: UserCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
) -> UserRead:
    # 检查权限：需要用户创建权限
    if not current_user.has_permission("user:create"):
        raise HTTPException(status_code=403, detail="权限不足")

    db_user = create_user(session, user)
    return db_user.to_read()


@router.get("/me", response_model=UserRead)
def read_user_me(current_user: User = Depends(get_current_active_user)) -> UserRead:
    return current_user.to_read()


@router.get("/{user_id}", response_model=UserRead)
def read_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
) -> UserRead:
    if not current_user.is_superuser and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="权限不足")

    user = get_user(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user.to_read()


@router.put("/{user_id}", response_model=UserRead)
def update_existing_user(
    user_id: int,
    user_update: UserUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
) -> UserRead:
    # 检查权限：用户可以更新自己的信息，管理员可以更新任何用户
    is_self_update = current_user.id == user_id
    if not is_self_update and not current_user.has_permission("user:update"):
        raise HTTPException(status_code=403, detail="权限不足")

    # 获取目标用户
    user = get_user(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 如果不是自己更新，限制可以更新的字段
    if not is_self_update:
        # 管理员不能修改他人密码，需要重置密码功能
        if user_update.password is not None:
            raise HTTPException(status_code=403, detail="不能直接修改他人密码")

    # 更新用户基本信息
    update_data = user_update.dict(exclude_unset=True, exclude={"role_ids"})
    for field, value in update_data.items():
        if hasattr(user, field):
            setattr(user, field, value)

    # 处理角色分配（只有管理员可以分配角色）
    if user_update.role_ids is not None and current_user.has_permission("role:assign"):
        # 获取角色对象
        roles = session.exec(select(Role).where(Role.id.in_(user_update.role_ids))).all()
        user.roles = roles

    # 更新时间戳
    user.updated_at = datetime.utcnow()

    session.add(user)
    session.commit()
    session.refresh(user)

    return user.to_read()


def generate_random_password(length: int = 8) -> str:
    """生成随机密码"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password


@router.post("/{user_id}/reset-password")
def reset_user_password(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    # 检查权限：需要用户管理权限
    if not current_user.has_permission("user:update"):
        raise HTTPException(status_code=403, detail="权限不足")

    # 获取目标用户
    user = get_user(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 生成新密码
    new_password = generate_random_password()
    user.hashed_password = get_password_hash(new_password)
    user.updated_at = datetime.utcnow()

    session.add(user)
    session.commit()
    session.refresh(user)

    return {
        "message": f"用户 {user.username} 的密码已重置",
        "new_password": new_password
    }


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    # 检查权限：需要用户删除权限
    if not current_user.has_permission("user:delete"):
        raise HTTPException(status_code=403, detail="权限不足")

    # 不能删除自己
    if current_user.id == user_id:
        raise HTTPException(status_code=400, detail="不能删除自己")

    user = get_user(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    session.delete(user)
    session.commit()

    return {"message": f"用户 {user.username} 已删除"}
