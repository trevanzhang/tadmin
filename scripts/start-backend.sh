#!/bin/bash

echo "启动后端服务..."

# 检查是否存在虚拟环境
if [ ! -d "backend/.venv" ]; then
    echo "虚拟环境不存在，正在创建..."
    cd backend
    uv sync
    cd ..
fi

# 激活虚拟环境并启动服务
cd backend
source .venv/bin/activate 2>/dev/null || source .venv/Scripts/activate

# 检查环境变量文件
if [ ! -f "../.env" ]; then
    echo "错误: .env 文件不存在，请先创建环境配置文件"
    exit 1
fi

# 检查数据库配置
echo "检查数据库配置..."
DB_TYPE=$(uv run python -c "from app.core.config import settings; print(settings.DATABASE_TYPE)")
echo "数据库类型: $DB_TYPE"

if [ "$DB_TYPE" = "sqlite" ]; then
    SQLITE_PATH=$(uv run python -c "from app.core.config import settings; print(settings.SQLALCHEMY_DATABASE_URI.replace('sqlite:///', ''))")
    echo "SQLite数据库路径: $SQLITE_PATH"
    # 确保SQLite数据库目录存在
    SQLITE_DIR=$(dirname "$SQLITE_PATH")
    mkdir -p "$SQLITE_DIR"
else
    echo "PostgreSQL数据库，请确保服务正在运行..."
fi

echo "启动 FastAPI 服务..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000