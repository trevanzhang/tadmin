
from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password, validate_password_strength
from app.models import User, UserCreate, UserUpdate


def get_user_by_username(session: Session, username: str) -> User | None:
    statement = select(User).where(User.username == username)
    return session.exec(statement).first()


def get_user_by_email(session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()


def get_user(session: Session, user_id: int) -> User | None:
    return session.get(User, user_id)


def authenticate_user(session: Session, username: str, password: str) -> User | None:
    user = get_user_by_username(session, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_user(session: Session, user_create: UserCreate) -> User:
    # 验证密码强度
    is_valid, errors = validate_password_strength(user_create.password)
    if not is_valid:
        raise ValueError(f"密码强度不足: {'; '.join(errors)}")

    user = user_create.to_user()
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def update_user(session: Session, user_id: int, user_update: UserUpdate) -> User | None:
    user = get_user(session, user_id)
    if not user:
        return None

    update_data = user_update.dict(exclude_unset=True)
    if "password" in update_data:
        # 验证新密码强度
        is_valid, errors = validate_password_strength(update_data["password"])
        if not is_valid:
            raise ValueError(f"密码强度不足: {'; '.join(errors)}")
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

    for field, value in update_data.items():
        setattr(user, field, value)

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_users(session: Session, skip: int = 0, limit: int = 100) -> list[User]:
    statement = select(User).offset(skip).limit(limit)
    return list(session.exec(statement).all())
