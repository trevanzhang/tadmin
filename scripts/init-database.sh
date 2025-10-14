#!/bin/bash

echo "初始化数据库..."

# 检查环境变量文件
if [ ! -f ".env" ]; then
    echo "错误: .env 文件不存在，请先创建环境配置文件"
    exit 1
fi

# 检查虚拟环境
if [ ! -d "backend/.venv" ]; then
    echo "虚拟环境不存在，正在创建..."
    cd backend
    uv sync
    cd ..
fi

# 激活虚拟环境
cd backend
source .venv/bin/activate 2>/dev/null || source .venv/Scripts/activate

# 检查数据库类型
echo "检查数据库配置..."
DB_TYPE=$(uv run python -c "from app.core.config import settings; print(settings.DATABASE_TYPE)")
echo "数据库类型: $DB_TYPE"

if [ "$DB_TYPE" = "sqlite" ]; then
    echo "检测到SQLite数据库，创建数据库文件..."
    # SQLite会自动创建数据库文件，但我们可以确保目录存在
    SQLITE_PATH=$(uv run python -c "from app.core.config import settings; print(settings.SQLALCHEMY_DATABASE_URI.replace('sqlite:///', ''))")
    SQLITE_DIR=$(dirname "$SQLITE_PATH")
    mkdir -p "$SQLITE_DIR"
    echo "SQLite数据库路径: $SQLITE_PATH"
else
    echo "检测到PostgreSQL数据库，请确保PostgreSQL服务正在运行..."
fi

echo "应用数据库迁移..."
uv run alembic upgrade head

echo "初始化数据..."
uv run python -m app.initial_data

echo "数据库初始化完成！"
echo ""
echo "数据库类型: $DB_TYPE"
if [ "$DB_TYPE" = "sqlite" ]; then
    echo "SQLite数据库文件: $SQLITE_PATH"
fi
echo ""
echo "默认管理员账号:"
echo "邮箱: admin@example.com"
echo "密码: admin123"
echo ""
echo "也可以使用用户名登录:"
echo "用户名: admin"
echo "密码: admin123"