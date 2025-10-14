#!/bin/bash

echo "启动 tadmin 管理系统..."

# 检查环境变量文件
if [ ! -f ".env" ]; then
    echo "错误: .env 文件不存在，请先创建环境配置文件"
    echo "参考 docs/环境配置说明.md 创建配置文件"
    exit 1
fi

# 启动后端服务
echo "启动后端服务..."
chmod +x scripts/start-backend.sh
chmod +x scripts/start-frontend.sh

# 在后台启动后端服务
./scripts/start-backend.sh &
BACKEND_PID=$!

# 等待后端服务启动
echo "等待后端服务启动..."
sleep 8

# 检查后端服务是否启动成功
if curl -s http://localhost:8000/docs > /dev/null; then
    echo "后端服务启动成功！"
else
    echo "后端服务启动失败，请检查日志"
    kill $BACKEND_PID
    exit 1
fi

# 启动前端服务
echo "启动前端服务..."
./scripts/start-frontend.sh &
FRONTEND_PID=$!

echo "系统启动完成！"
echo "前端地址: http://localhost:8848"
echo "后端API文档: http://localhost:8000/docs"
echo ""
echo "按 Ctrl+C 停止所有服务"

# 等待用户中断
trap 'echo "正在停止服务..."; kill $BACKEND_PID $FRONTEND_PID; exit' INT
wait