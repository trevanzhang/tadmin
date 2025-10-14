# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

**Tadmin** 是一个基于现代技术栈构建的全栈管理系统（全栈开发脚手架），采用前后端分离架构，提供完整的用户认证、权限管理和数据管理功能。该项目非常适合用作开发其他应用的模版，开箱即用。

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

## 常用开发命令

### 使用项目脚本（推荐）

根据项目规则，所有 Run & Debug 操作都应该使用 `scripts/` 目录下的脚本：

```bash
# 初始化数据库
./scripts/init-database.sh

# 启动完整系统
./scripts/start-all.sh

# 分别启动服务
./scripts/start-backend.sh    # 后端: http://localhost:8000
./scripts/start-frontend.sh   # 前端: http://localhost:8848

# API 测试
./scripts/test-api.sh
```

### 后端命令

```bash
cd backend
# 依赖管理
uv sync                    # 安装依赖
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000  # 开发服务器

# 数据库迁移
uv run alembic revision --autogenerate -m "描述变更内容"
uv run alembic upgrade head

# 代码质量
uv run ruff check          # 代码检查
uv run ruff format         # 代码格式化
```

### 前端命令

```bash
cd frontend
pnpm install               # 安装依赖
pnpm dev                   # 开发服务器
pnpm build                 # 生产构建
pnpm lint                  # 代码检查和格式化
pnpm typecheck             # 类型检查

# Playwright E2E测试
pnpm test:e2e              # 运行E2E测试
pnpm test:e2e:ui           # UI模式测试
pnpm test:e2e:debug        # 调试模式测试
pnpm test:e2e:codegen      # 代码生成器
```

## 项目结构

```
tadmin/
├── backend/                 # FastAPI 后端
│   ├── app/
│   │   ├── api/            # API 路由
│   │   ├── core/           # 核心配置
│   │   ├── models.py       # SQLModel 数据模型
│   │   ├── crud.py         # CRUD 操作
│   │   ├── services/       # 业务逻辑
│   │   ├── alembic/        # 数据库迁移
│   │   └── main.py         # 应用入口
│   └── pyproject.toml      # Python 配置
├── frontend/               # Vue 3 前端
│   ├── src/
│   │   ├── api/            # API 调用
│   │   ├── components/     # 公共组件
│   │   ├── layout/         # 布局组件
│   │   ├── router/         # 路由配置
│   │   ├── store/          # Pinia 状态管理
│   │   ├── views/          # 页面组件
│   │   └── services/       # 服务层
│   ├── tests/              # Playwright E2E测试
│   ├── playwright.config.ts # Playwright配置
│   └── package.json        # 前端配置
├── scripts/                # 运维脚本（必须使用）
├── docs/                   # 项目文档
└── .kilocode/             # Kilocode 配置
```

## 数据库工作流程

### 智能环境配置

- 开发环境自动使用 SQLite
- 生产环境使用 PostgreSQL
- 环境变量配置在 `.env` 文件

### 迁移流程

```bash
# 1. 修改数据模型 (backend/app/models.py)

# 2. 生成迁移
cd backend
uv run alembic revision --autogenerate -m "变更描述"

# 3. 检查迁移文件 (backend/app/alembic/versions/xxx.py)

# 4. 应用迁移
uv run alembic upgrade head
```

## 开发工作流程

### 环境准备

```bash
# 1. 克隆项目
git clone <repository-url>
cd tadmin

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 文件

# 3. 初始化数据库
./scripts/init-database.sh
```

### 开发启动

```bash
# 启动完整系统
./scripts/start-all.sh

# 访问地址
# 前端: http://localhost:8848
# 后端 API 文档: http://localhost:8000/docs
```

## 代码质量规范

### 工具链

- **Python**: Ruff (检查 + 格式化)
- **TypeScript**: ESLint, Prettier, Stylelint
- **Git Hooks**: Pre-commit 检查

### 提交规范

采用约定式提交：

- `feat`: 新功能
- `fix`: 修复
- `docs`: 文档
- `style`: 格式调整
- `refactor`: 重构
- `test`: 测试
- `chore`: 构建/工具

## Git 开发工作流程

### 分支策略

**Git Flow（适合传统项目）**
- `master` - 生产环境代码
- `develop` - 开发主分支
- `feature/*` - 功能开发分支
- `hotfix/*` - 紧急修复分支
- `release/*` - 发布准备分支

**GitHub Flow（适合持续部署）**
- `main` - 生产环境
- `feature/*` - 功能分支，直接合并到 main

### 日常操作

```bash
# 创建功能分支
git checkout -b feature/new-feature

# 频繁提交，原子化变更
git add .
git commit -m "feat: add user authentication"

# 保持分支更新
git fetch origin
git rebase origin/main

# 创建 Pull Request
# 代码审查后合并
```

### 提交规范

```
类型(范围): 简短描述

feat: 新功能
fix: 修复问题
docs: 文档更新
style: 代码格式
refactor: 重构
test: 测试
chore: 构建/工具
```

### 核心原则

1. **主分支保护** - main/master 分支只接受 PR
2. **原子化提交** - 每个提交只做一件事
3. **频繁同步** - 定期 rebase 远程分支
4. **代码审查** - 所有变更都需要 PR
5. **自动化检查** - CI/CD 自动测试和构建

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
6. **E2E测试支持**: 集成Playwright自动化测试
7. **调试友好**: 支持MCP Playwright实时调试

## 重要提醒

- **永远使用 scripts/ 目录下的脚本进行启停**，不要直接使用 npm、pnpm、uv、python 等命令
- Python 虚拟环境使用 `.venv` 目录名
- 优先使用 TypeScript，强类型数据结构
- 遵循代码文件行数限制（动态语言 300 行，静态语言 400 行）
- 注意代码架构的优雅性，避免"坏味道"模式

## 调试指南

### MCP Playwright调试
项目集成了MCP Playwright调试工具，支持实时浏览器调试：

```bash
# 启动前端服务
./scripts/start-frontend.sh

# 使用MCP Playwright调试
mcp__playwright__browser_navigate "http://localhost:8848"
mcp__playwright__browser_snapshot
mcp__playwright__browser_click "元素描述" "ref引用"
```

### 常见问题调试
1. **Token刷新错误**: 检查frontend/src/utils/http/index.ts中refresh_token参数传递
2. **UI视口问题**: 使用JavaScript直接操作DOM元素绕过视口限制
3. **网络请求监控**: 使用mcp__playwright__browser_network_requests查看API调用

*基于项目现有 CLAUDE.md 和 README 文件整合更新*
- 文档更新制度
必须立即更新的情况
Git commit - 处理完成后立即记录到CHANGELOG.md
系统架构调整 - 结构调整后更新CLAUDE.md和CHANGELOG.md
新增Commands - 新Command创建后添加到CLAUDE.md
重要配置变更 - 任何核心配置修改都要记录