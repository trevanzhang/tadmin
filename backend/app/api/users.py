
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.api.deps import get_current_active_user
from app.core.database import get_session
from app.crud import create_user, get_user, get_users, update_user
from app.models import User, UserCreate, UserRead, UserUpdate

router = APIRouter()


@router.get("/", response_model=list[UserRead])
def read_users(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
) -> list[UserRead]:
    users = get_users(session, skip=skip, limit=limit)
    return [user.to_read() for user in users]


@router.post("/", response_model=UserRead)
def create_new_user(
    user: UserCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
) -> UserRead:
    if not current_user.is_superuser:
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
    if not current_user.is_superuser and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="权限不足")

    user = update_user(session, user_id, user_update)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user.to_read()
