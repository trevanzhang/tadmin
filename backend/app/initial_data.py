from sqlmodel import Session

from app.core.database import engine
from app.crud import create_user
from app.models import UserCreate


def init() -> None:
    with Session(engine) as session:
        # 创建默认管理员用户
        admin_user = UserCreate(
            username="admin",
            email="admin@example.com",
            password="admin123",
            full_name="系统管理员"
        )

        # 检查是否已存在管理员用户
        from app.crud import get_user_by_username
        existing_admin = get_user_by_username(session, "admin")

        if not existing_admin:
            user = create_user(session, admin_user)
            # 设置管理员权限
            user.is_superuser = True
            session.add(user)
            session.commit()
            print(f"创建管理员用户: {user.username}")
        else:
            print("管理员用户已存在")


if __name__ == "__main__":
    init()
