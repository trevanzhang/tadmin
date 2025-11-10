#!/usr/bin/env python3
"""
创建测试用户数据的脚本
"""

import requests
import json

# API配置
BASE_URL = "http://localhost:8000"
LOGIN_URL = f"{BASE_URL}/api/v1/auth/login"
USERS_URL = f"{BASE_URL}/api/v1/users/"

# 测试用户数据
test_users = [
    {
        "username": "zhangsan",
        "email": "zhangsan@example.com",
        "password": "SecurePass123!",
        "full_name": "张三"
    },
    {
        "username": "lisi",
        "email": "lisi@example.com",
        "password": "StrongPass@456",
        "full_name": "李四"
    },
    {
        "username": "wangwu",
        "email": "wangwu@example.com",
        "password": "ComplexPass789!",
        "full_name": "王五"
    },
    {
        "username": "zhaoliu",
        "email": "zhaoliu@example.com",
        "password": "SafePass321@",
        "full_name": "赵六"
    },
    {
        "username": "sunqi",
        "email": "sunqi@example.com",
        "password": "Powerful654!",
        "full_name": "孙七"
    },
    {
        "username": "zhouba",
        "email": "zhouba@example.com",
        "password": "GreatPass987!",
        "full_name": "周八"
    },
    {
        "username": "wujiu",
        "email": "wujiu@example.com",
        "password": "Excellent123@",
        "full_name": "吴九"
    },
    {
        "username": "zhengshi",
        "email": "zhengshi@example.com",
        "password": "PerfectPass456!",
        "full_name": "郑十"
    }
]

def get_auth_token():
    """获取认证令牌"""
    login_data = {
        "username": "admin",
        "password": "admin123"
    }

    response = requests.post(LOGIN_URL, data=login_data)
    if response.status_code == 200:
        data = response.json()
        return data["data"]["accessToken"]
    else:
        print(f"登录失败: {response.status_code}")
        print(response.text)
        return None

def create_user(token, user_data):
    """创建单个用户"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.post(USERS_URL, json=user_data, headers=headers)
    return response

def main():
    """主函数"""
    print("正在获取认证令牌...")
    token = get_auth_token()

    if not token:
        print("无法获取认证令牌，退出")
        return

    print(f"认证令牌获取成功")

    print(f"\n开始创建 {len(test_users)} 个测试用户...")

    success_count = 0
    for i, user in enumerate(test_users, 1):
        print(f"正在创建用户 {i}/{len(test_users)}: {user['username']}")

        response = create_user(token, user)

        if response.status_code == 200:
            print(f"✅ 用户 {user['username']} 创建成功")
            success_count += 1
        else:
            print(f"❌ 用户 {user['username']} 创建失败: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   错误信息: {error_data}")
            except:
                print(f"   响应内容: {response.text}")

    print(f"\n创建完成！成功创建 {success_count}/{len(test_users)} 个用户")

if __name__ == "__main__":
    main()