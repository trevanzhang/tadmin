#!/bin/bash

echo "启动前端服务..."

# 切换到frontend目录
cd "$(dirname "$0")/../frontend"

# 检查是否存在 node_modules
if [ ! -d "node_modules" ]; then
    echo "依赖未安装，正在安装..."
    pnpm install
fi

# 启动前端服务
echo "启动 Vue 开发服务器..."
exec pnpm dev