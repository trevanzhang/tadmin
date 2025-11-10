from datetime import datetime
from typing import List

from sqlmodel import Field, SQLModel, Relationship

from app.core.security import get_password_hash, validate_password_strength


# 用户-角色关联表（多对多关系）
class UserRoleLink(SQLModel, table=True):
    __tablename__ = "user_role_links"

    user_id: int | None = Field(default=None, foreign_key="users.id", primary_key=True)
    role_id: int | None = Field(default=None, foreign_key="roles.id", primary_key=True)


class RoleBase(SQLModel):
    name: str = Field(index=True, unique=True)
    description: str | None = None
    is_active: bool = True


class Role(RoleBase, table=True):
    __tablename__ = "roles"

    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # 与用户的关联关系
    users: List["User"] = Relationship(back_populates="roles", link_model=UserRoleLink)


class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    full_name: str | None = None
    is_active: bool = True
    is_superuser: bool = False


class User(UserBase, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # 与角色的关联关系
    roles: List[Role] = Relationship(back_populates="users", link_model=UserRoleLink)

    def to_read(self) -> "UserRead":
        return UserRead(
            id=self.id,
            username=self.username,
            email=self.email,
            full_name=self.full_name,
            is_active=self.is_active,
            is_superuser=self.is_superuser,
            created_at=self.created_at,
            updated_at=self.updated_at,
            role_names=[role.name for role in self.roles] if self.roles else []
        )

    def has_role(self, role_name: str) -> bool:
        """检查用户是否拥有指定角色"""
        return any(role.name == role_name for role in self.roles) if self.roles else False

    def has_permission(self, permission: str) -> bool:
        """检查用户是否拥有指定权限（基于角色的简化权限检查）"""
        # 简化权限模型：超级管理员拥有所有权限
        if self.is_superuser:
            return True

        # 管理员权限
        if self.has_role("admin"):
            admin_permissions = [
                "user:read", "user:create", "user:update", "user:delete",
                "role:read", "role:create", "role:update", "role:assign"
            ]
            return permission in admin_permissions

        # 普通用户权限
        if self.has_role("user"):
            user_permissions = ["profile:read", "profile:update"]
            return permission in user_permissions

        return False


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
    role_names: List[str] = []


class UserUpdate(SQLModel):
    username: str | None = None
    email: str | None = None
    full_name: str | None = None
    password: str | None = None
    is_active: bool | None = None
    role_ids: List[int] | None = None  # 用于分配角色


# Role 相关的 DTOs
class RoleCreate(RoleBase):
    pass


class RoleRead(RoleBase):
    id: int
    created_at: datetime
    updated_at: datetime


class RoleUpdate(SQLModel):
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


# 用户角色分配 DTO
class UserRoleAssign(SQLModel):
    user_id: int
    role_ids: List[int]


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    username: str | None = None
