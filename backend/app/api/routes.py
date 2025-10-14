import logging
from typing import Any

from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.models import User

router = APIRouter()
logger = logging.getLogger("routes")


@router.get("/get-async-routes")
def get_async_routes(current_user: User = Depends(get_current_user)) -> dict[str, Any]:
    """获取异步路由（动态菜单）"""
    logger.info(f"Route request from user: {current_user.username} (superuser: {current_user.is_superuser})")

    # 根据用户角色返回不同的路由
    if current_user.is_superuser:
        # 管理员路由
        routes = [
            {
                "path": "/dashboard",
                "name": "Dashboard",
                "meta": {
                    "title": "仪表板",
                    "icon": "dashboard",
                    "rank": 1
                }
            },
            {
                "path": "/users",
                "name": "Users",
                "meta": {
                    "title": "用户管理",
                    "icon": "user",
                    "rank": 2
                }
            },
            {
                "path": "/system",
                "name": "System",
                "meta": {
                    "title": "系统管理",
                    "icon": "system",
                    "rank": 3
                }
            }
        ]
        logger.info(f"Returning admin routes: {len(routes)} routes")
        return {
            "success": True,
            "data": routes
        }
    else:
        # 普通用户路由
        routes = [
            {
                "path": "/dashboard",
                "name": "Dashboard",
                "meta": {
                    "title": "仪表板",
                    "icon": "dashboard",
                    "rank": 1
                }
            }
        ]
        logger.info(f"Returning user routes: {len(routes)} routes")
        return {
            "success": True,
            "data": routes
        }
