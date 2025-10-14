#!/bin/bash

echo "启动前端服务..."

# 检查是否存在 node_modules
if [ ! -d "frontend/node_modules" ]; then
    echo "依赖未安装，正在安装..."
    cd frontend
    pnpm install
    cd ..
fi

# 启动前端服务
cd frontend
echo "启动 Vue 开发服务器..."
pnpm dev