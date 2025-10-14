# Tadmin - 全栈管理系统

Tadmin 是一个基于现代技术栈构建的全栈管理系统，采用前后端分离架构，提供完整的用户认证、权限管理和数据管理功能。

## 技术栈

### 后端
- **框架**: FastAPI 0.114+
- **语言**: Python 3.10+
- **数据库**: SQLite (开发) / PostgreSQL (生产)
- **ORM**: SQLModel
- **认证**: JWT
- **迁移**: Alembic
- **包管理**: uv

### 前端
- **框架**: Vue 3.5+ + TypeScript 5.8+
- **UI库**: Element Plus 2.10+
- **构建**: Vite 7.0+
- **状态**: Pinia 3.0+
- **路由**: Vue Router 4.5+
- **样式**: Tailwind CSS 4.1+
- **包管理**: pnpm

## 快速开始

### 环境准备
```bash
# 克隆项目
git clone <repository-url>
cd tadmin

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件

# 初始化数据库
./scripts/init-database.sh
```

### 启动系统
```bash
# 启动完整系统
./scripts/start-all.sh

# 访问地址
# 前端: http://localhost:8848
# 后端 API 文档: http://localhost:8000/docs
```

## 默认配置

### 管理员账号
- **邮箱**: admin@example.com
- **用户名**: admin
- **密码**: admin123

### 服务地址
- **前端**: http://localhost:8848
- **后端 API**: http://localhost:8000
- **API 文档**: http://localhost:8000/docs

## 项目特性

1. **智能环境配置**: 自动根据环境选择数据库
2. **完整工具链**: 从开发到部署的全套脚本
3. **严格质量控制**: 多层代码检查
4. **脚本化运维**: 必须使用 scripts/ 目录脚本
5. **现代化架构**: 最新技术栈和最佳实践

## 开发指南

详细开发指南请参考 [CLAUDE.md](./CLAUDE.md) 文件。