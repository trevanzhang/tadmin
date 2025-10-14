from datetime import datetime

from sqlmodel import Field, SQLModel

from app.core.security import get_password_hash, validate_password_strength


class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    full_name: str | None = None
    is_active: bool = True
    is_superuser: bool = False


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def to_read(self) -> "UserRead":
        return UserRead(
            id=self.id,
            username=self.username,
            email=self.email,
            full_name=self.full_name,
            is_active=self.is_active,
            is_superuser=self.is_superuser,
            created_at=self.created_at,
            updated_at=self.updated_at
        )


class UserCreate(SQLModel):
    username: str
    email: str
    password: str
    full_name: str | None = None

    def to_user(self) -> User:
        return User(
            username=self.username,
            email=self.email,
            full_name=self.full_name,
            hashed_password=get_password_hash(self.password)
        )

    def validate_password(self) -> tuple[bool, list[str]]:
        """验证密码强度"""
        return validate_password_strength(self.password)


class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime


class UserUpdate(SQLModel):
    username: str | None = None
    email: str | None = None
    full_name: str | None = None
    password: str | None = None
    is_active: bool | None = None


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    username: str | None = None
