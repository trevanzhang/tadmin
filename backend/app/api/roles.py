from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, func
from typing import Optional, Dict, Any

from app.api.deps import get_current_active_user
from app.core.database import get_session
from app.models import Role, User, RoleCreate, RoleRead, RoleUpdate, UserRoleAssign

router = APIRouter()


@router.get("/")
def read_roles(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = Query(None, description="搜索角色名称或描述"),
    is_active: Optional[bool] = Query(None, description="筛选角色状态"),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
) -> Dict[str, Any]:
    """获取角色列表"""
    # 检查权限：需要角色读取权限
    if not current_user.has_permission("role:read"):
        raise HTTPException(status_code=403, detail="权限不足")

    # 构建基础查询
    count_statement = select(func.count(Role.id))
    statement = select(Role)

    # 搜索条件
    if search:
        search_condition = (
            (Role.name.contains(search)) |
            (Role.description.contains(search))
        )
        statement = statement.where(search_condition)
        count_statement = count_statement.where(search_condition)

    # 状态筛选
    if is_active is not None:
        statement = statement.where(Role.is_active == is_active)
        count_statement = count_statement.where(Role.is_active == is_active)

    # 获取总数
    total = session.exec(count_statement).one()

    # 分页和排序
    statement = statement.offset(skip).limit(limit).order_by(Role.created_at.desc())

    roles = session.exec(statement).all()

    return {
        "data": roles,
        "total": total,
        "skip": skip,
        "limit": limit
    }


@router.post("/", response_model=RoleRead)
def create_role(
    role: RoleCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
) -> RoleRead:
    """创建新角色"""
    # 检查权限：需要角色创建权限
    if not current_user.has_permission("role:create"):
        raise HTTPException(status_code=403, detail="权限不足")

    # 检查角色名是否已存在
    existing_role = session.exec(select(Role).where(Role.name == role.name)).first()
    if existing_role:
        raise HTTPException(status_code=400, detail="角色名已存在")

    db_role = Role(**role.dict())
    session.add(db_role)
    session.commit()
    session.refresh(db_role)

    return db_role


@router.get("/{role_id}", response_model=RoleRead)
def read_role(
    role_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
) -> RoleRead:
    """获取指定角色详情"""
    if not current_user.has_permission("role:read"):
        raise HTTPException(status_code=403, detail="权限不足")

    role = session.get(Role, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="角色不存在")

    return role


@router.put("/{role_id}", response_model=RoleRead)
def update_role(
    role_id: int,
    role_update: RoleUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
) -> RoleRead:
    """更新角色信息"""
    # 需要角色更新权限
    if not current_user.has_permission("role:update"):
        raise HTTPException(status_code=403, detail="权限不足")

    role = session.get(Role, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="角色不存在")

    # 检查角色名唯一性（如果要更新的话）
    if role_update.name and role_update.name != role.name:
        existing_role = session.exec(select(Role).where(Role.name == role_update.name)).first()
        if existing_role:
            raise HTTPException(status_code=400, detail="角色名已存在")

    # 更新字段
    update_data = role_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        if hasattr(role, field):
            setattr(role, field, value)

    # 更新时间戳
    role.updated_at = datetime.utcnow()

    session.add(role)
    session.commit()
    session.refresh(role)

    return role


@router.delete("/{role_id}")
def delete_role(
    role_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """删除角色"""
    # 只有超级管理员可以删除角色
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="权限不足")

    role = session.get(Role, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="角色不存在")

    # 检查是否有用户使用该角色
    if role.users:
        raise HTTPException(status_code=400, detail=f"无法删除角色 {role.name}，仍有用户使用该角色")

    session.delete(role)
    session.commit()

    return {"message": f"角色 {role.name} 已删除"}


@router.post("/assign")
def assign_user_roles(
    assignment: UserRoleAssign,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """为用户分配角色"""
    if not current_user.has_permission("role:assign"):
        raise HTTPException(status_code=403, detail="权限不足")

    # 获取用户
    user = session.get(User, assignment.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 获取角色
    roles = session.exec(select(Role).where(Role.id.in_(assignment.role_ids))).all()
    if len(roles) != len(assignment.role_ids):
        raise HTTPException(status_code=400, detail="部分角色不存在")

    # 分配角色
    user.roles = roles
    user.updated_at = datetime.utcnow()

    session.add(user)
    session.commit()

    return {"message": f"已为用户 {user.username} 分配角色: {[role.name for role in roles]}"}


@router.get("/{role_id}/users", response_model=list[dict])
def get_role_users(
    role_id: int,
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
) -> list[dict]:
    """获取拥有指定角色的用户列表"""
    if not current_user.has_permission("role:read"):
        raise HTTPException(status_code=403, detail="权限不足")

    role = session.get(Role, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="角色不存在")

    # 获取拥有该角色的用户
    statement = select(User).join(User.roles).where(Role.id == role_id)
    statement = statement.offset(skip).limit(limit).order_by(User.created_at.desc())

    users = session.exec(statement).all()
    return [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "is_active": user.is_active,
            "created_at": user.created_at
        }
        for user in users
    ]