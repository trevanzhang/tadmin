# Backend 模块文档

[根目录](../../CLAUDE.md) > **backend**

## 变更记录 (Changelog)

### 2025-11-09 22:13:52 - 自适应初始化架构师系统
- 创建backend模块文档
- 分析API路由和数据模型
- 识别核心服务和安全机制

## 模块职责

Backend模块负责提供完整的RESTful API服务，包括用户认证、数据管理和业务逻辑处理。采用FastAPI框架构建，支持自动API文档生成和类型验证。

## 入口与启动

### 应用入口
- **主文件**: `app/main.py`
- **启动命令**: `uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
- **健康检查**: `GET /health`
- **API文档**: `GET /docs` (Swagger UI)

### 启动流程
1. 加载配置和设置日志系统
2. 配置全局中间件（CORS、安全头、请求日志）
3. 注册异常处理器
4. 包含API路由模块
5. 创建数据库表

## 对外接口

### 认证模块 (`/api/v1/auth`)
- **POST `/auth/login`** - OAuth2兼容登录（form格式）
- **POST `/auth/sessions`** - JSON格式登录
- **POST `/auth/refresh-token`** - 刷新访问令牌

### 用户管理 (`/api/v1/users`)
- **GET `/users/`** - 获取用户列表（需认证）
- **POST `/users/`** - 创建新用户（需管理员权限）
- **GET `/users/me`** - 获取当前用户信息
- **GET `/users/{user_id}`** - 获取指定用户信息
- **PUT `/users/{user_id}`** - 更新用户信息

### 系统路由
- **GET `/`** - 服务状态信息
- **GET `/health`** - 健康检查
- **GET `/test/error`** - 异常处理测试
- **GET `/test/validation`** - 验证异常测试

## 关键依赖与配置

### 核心依赖
```python
# 主要框架
fastapi[standard]>=0.114.2
sqlmodel>=0.0.21
alembic>=1.12.1

# 认证与安全
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
pyjwt>=2.8.0

# 数据库
psycopg[binary]>=3.1.13  # PostgreSQL
```

### 配置系统
- **配置文件**: `app/core/config.py`
- **环境变量**: 支持 `.env` 文件配置
- **数据库配置**: 智能切换SQLite/PostgreSQL
- **JWT配置**: 密钥、过期时间、算法配置

### 关键配置项
```python
DATABASE_TYPE: str = "sqlite"          # 数据库类型
SECRET_KEY: str = "your-secret-key"    # JWT密钥
ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # 访问令牌过期时间
REFRESH_TOKEN_EXPIRE_DAYS: int = 7     # 刷新令牌过期时间
BACKEND_CORS_ORIGINS: list[str] = [...] # CORS配置
```

## 数据模型

### 用户模型 (User)
```python
class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    full_name: str | None = None
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### 数据传输对象 (DTOs)
- **UserCreate**: 用户创建请求
- **UserRead**: 用户信息响应
- **UserUpdate**: 用户更新请求
- **Token**: 令牌响应
- **TokenData**: 令牌数据

### 数据库迁移
- **迁移目录**: `app/alembic/`
- **当前版本**: `5c191043847c_initial_migration.py`
- **迁移命令**:
  - 生成: `uv run alembic revision --autogenerate -m "描述"`
  - 应用: `uv run alembic upgrade head`

## 测试与质量

### 代码质量工具
- **Ruff**: 代码检查和格式化
- **MyPy**: 静态类型检查（严格模式）
- **Pre-commit**: Git钩子检查

### 测试策略
- **单元测试**: 使用pytest测试业务逻辑
- **API测试**: 使用httpx测试接口
- **数据库测试**: SQLite内存数据库
- **安全测试**: 密码强度验证、JWT令牌验证

### 密码安全机制
- **强度验证**: 长度、字符类型、常见弱密码检查
- **哈希算法**: bcrypt
- **评分系统**: 0-100分密码强度评分

## 核心服务

### 安全服务 (`app/core/security.py`)
- JWT令牌生成和验证
- 密码哈希和验证
- 密码强度验证和评分

### 认证服务 (`app/api/auth.py`)
- 用户登录验证
- 令牌刷新机制
- 统一认证响应格式

### CRUD操作 (`app/crud.py`)
- 用户数据增删改查
- 认证逻辑
- 数据验证

### 异常处理 (`app/core/exceptions.py`)
- 自定义异常类型
- 全局异常处理器
- 统一错误响应格式

## 常见问题 (FAQ)

### Q: 如何添加新的API端点？
A: 在`app/api/`目录下创建新的路由文件，然后在`app/main.py`中注册路由。

### Q: 如何修改数据模型？
A: 修改`app/models.py`，然后使用Alembic生成数据库迁移。

### Q: 如何配置生产环境数据库？
A: 设置环境变量`DATABASE_TYPE=postgresql`并配置相关数据库连接参数。

### Q: JWT令牌过期时间如何调整？
A: 修改`app/core/config.py`中的`ACCESS_TOKEN_EXPIRE_MINUTES`和`REFRESH_TOKEN_EXPIRE_DAYS`。

## 相关文件清单

### 核心文件
- `app/main.py` - 应用入口和路由注册
- `app/models.py` - SQLModel数据模型
- `app/crud.py` - 数据库操作
- `app/core/config.py` - 配置管理

### API路由
- `app/api/auth.py` - 认证相关接口
- `app/api/users.py` - 用户管理接口
- `app/api/routes.py` - 通用路由
- `app/api/deps.py` - 依赖注入

### 核心服务
- `app/core/security.py` - 安全服务
- `app/core/database.py` - 数据库连接
- `app/core/exceptions.py` - 异常处理
- `app/core/global_middleware.py` - 全局中间件

### 配置文件
- `pyproject.toml` - Python项目配置
- `app/alembic/` - 数据库迁移文件

## 变更记录 (Changelog)

### 2025-11-09 22:13:52 - 自适应初始化架构师系统
- 创建backend模块文档
- 分析API路由和数据模型
- 识别核心服务和安全机制