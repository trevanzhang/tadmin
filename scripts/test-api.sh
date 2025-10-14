#!/bin/bash

echo "测试 API 接口..."

# 检查后端服务是否运行
if ! curl -s http://localhost:8000/docs > /dev/null; then
    echo "错误: 后端服务未运行，请先启动后端服务"
    exit 1
fi

echo "1. 测试登录接口..."
LOGIN_RESPONSE=$(curl -s -X POST "http://localhost:8000/login" \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "admin123"}')

echo "登录响应: $LOGIN_RESPONSE"

# 提取访问令牌
ACCESS_TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"accessToken":"[^"]*' | cut -d'"' -f4)

if [ -z "$ACCESS_TOKEN" ]; then
    echo "错误: 登录失败，无法获取访问令牌"
    exit 1
fi

echo "访问令牌获取成功: ${ACCESS_TOKEN:0:20}..."

echo ""
echo "2. 测试用户信息接口..."
USER_RESPONSE=$(curl -s -X GET "http://localhost:8000/api/v1/users/me" \
     -H "Authorization: Bearer $ACCESS_TOKEN")

echo "用户信息响应: $USER_RESPONSE"

echo ""
echo "3. 测试动态路由接口..."
ROUTES_RESPONSE=$(curl -s -X GET "http://localhost:8000/get-async-routes" \
     -H "Authorization: Bearer $ACCESS_TOKEN")

echo "动态路由响应: $ROUTES_RESPONSE"

echo ""
echo "4. 测试刷新令牌接口..."
REFRESH_TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"refreshToken":"[^"]*' | cut -d'"' -f4)

REFRESH_RESPONSE=$(curl -s -X POST "http://localhost:8000/refresh-token" \
     -H "Content-Type: application/json" \
     -d "{\"refreshToken\": \"$REFRESH_TOKEN\"}")

echo "刷新令牌响应: $REFRESH_RESPONSE"

echo ""
echo "API 测试完成！"