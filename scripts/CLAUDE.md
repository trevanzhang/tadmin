# Scripts 模块文档

[根目录](../CLAUDE.md) > **scripts**

## 变更记录 (Changelog)

### 2025-11-09 22:13:52 - 自适应初始化架构师系统
- 创建scripts模块文档
- 分析运维脚本功能和依赖关系
- 识别系统启动和测试流程

## 模块职责

Scripts模块提供Tadmin项目的完整运维脚本集合，实现一键启动、数据库初始化、API测试等核心运维功能。所有脚本都经过优化，确保服务的可靠启动和优雅关闭。

## 脚本清单

### 系统启动脚本

#### start-all.sh - 一键启动完整系统
**功能**: 同时启动后端和前端服务，提供完整的开发环境
```bash
./scripts/start-all.sh
```
**特性**:
- 自动检查.env配置文件
- 后台启动后端服务（端口8000）
- 等待后端启动完成（8秒）
- 健康检查验证后端可用性
- 启动前端服务（端口8848）
- 支持Ctrl+C优雅关闭所有服务

**服务地址**:
- 前端: http://localhost:8848
- 后端API: http://localhost:8000/docs

#### start-backend.sh - 启动后端服务
**功能**: 单独启动FastAPI后端服务
```bash
./scripts/start-backend.sh
```
**配置**:
- 主机: 0.0.0.0
- 端口: 8000
- 自动重载: 开发模式

#### start-frontend.sh - 启动前端服务
**功能**: 单独启动Vue3前端开发服务器
```bash
./scripts/start-frontend.sh
```
**配置**:
- 主机: 0.0.0.0
- 端口: 8848
- 包管理器: pnpm

### 数据库管理脚本

#### init-database.sh - 初始化数据库
**功能**: 创建数据库表并插入初始数据
```bash
./scripts/init-database.sh
```
**流程**:
1. 检查后端环境配置
2. 应用数据库迁移
3. 插入默认管理员账户
4. 验证数据库连接

**默认管理员账户**:
- 邮箱: admin@example.com
- 用户名: admin
- 密码: admin123

### 测试脚本

#### test-api.sh - API接口测试
**功能**: 测试后端API接口的可用性和正确性
```bash
./scripts/test-api.sh
```
**测试覆盖**:
- 用户认证接口
- 用户管理接口
- 健康检查接口
- 错误处理接口

## 脚本依赖关系

### 依赖层次
```
start-all.sh
├── start-backend.sh
├── start-frontend.sh
└── init-database.sh (首次运行时)

test-api.sh
└── start-backend.sh (自动启动)
```

### 环境依赖
- **Python**: 3.10+ (后端)
- **Node.js**: 20.19.0+ (前端)
- **pnpm**: 9+ (前端包管理)
- **uv**: 最新版本 (Python包管理)
- **curl**: 网络请求测试

## 使用规范

### 必须使用脚本的原因
1. **环境一致性**: 确保所有开发人员使用相同的启动方式
2. **配置管理**: 统一管理端口、主机等配置
3. **依赖检查**: 自动检查必要的环境和依赖
4. **错误处理**: 提供完善的错误提示和日志
5. **优雅关闭**: 支持服务的优雅启动和关闭

### 禁止直接使用的命令
```bash
# ❌ 错误方式 - 直接使用包管理器
cd backend && uv run uvicorn ...
cd frontend && pnpm dev

# ✅ 正确方式 - 使用项目脚本
./scripts/start-all.sh
./scripts/start-backend.sh
./scripts/start-frontend.sh
```

## 配置文件要求

### 环境变量文件 (.env)
所有脚本都要求存在.env文件，包含以下关键配置：
```bash
DATABASE_TYPE=sqlite
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 脚本权限
首次使用前需要确保脚本具有执行权限：
```bash
chmod +x scripts/*.sh
```

## 错误处理

### 常见错误及解决方案

#### 1. .env文件不存在
**错误**: `错误: .env 文件不存在，请先创建环境配置文件`
**解决**: 复制`.env.example`为`.env`并填入正确配置

#### 2. 后端启动失败
**错误**: `后端服务启动失败，请检查日志`
**解决**:
- 检查Python环境和依赖
- 查看后端日志输出
- 确认端口8000未被占用

#### 3. 前端启动失败
**错误**: `前端服务启动失败`
**解决**:
- 检查Node.js和pnpm版本
- 进入frontend目录运行`pnpm install`
- 确认端口8848未被占用

#### 4. 数据库初始化失败
**错误**: `数据库迁移失败`
**解决**:
- 检查数据库配置
- 确认数据库文件权限
- 手动运行`uv run alembic upgrade head`

## 日志和监控

### 日志输出
- **后端日志**: 控制台实时输出
- **前端日志**: 开发服务器日志
- **系统日志**: 脚本执行状态

### 健康检查
- **后端健康**: `curl http://localhost:8000/docs`
- **前端健康**: `curl http://localhost:8848`
- **API测试**: `./scripts/test-api.sh`

## 开发工作流

### 首次设置
```bash
# 1. 克隆项目
git clone <repository-url>
cd tadmin

# 2. 配置环境
cp .env.example .env
# 编辑.env文件

# 3. 初始化数据库
./scripts/init-database.sh

# 4. 启动系统
./scripts/start-all.sh
```

### 日常开发
```bash
# 启动完整系统
./scripts/start-all.sh

# 测试API接口
./scripts/test-api.sh
```

### 生产部署
```bash
# 构建前端
cd frontend && pnpm build

# 启动生产服务
./scripts/start-backend.sh  # 使用生产配置
```

## 性能优化

### 启动优化
- **并行启动**: 后端和前端可以并行启动
- **健康检查**: 避免启动未完成的服务
- **缓存机制**: 重复启动时利用缓存

### 资源管理
- **后台进程**: 使用&符号后台启动服务
- **进程管理**: 记录进程ID，支持优雅关闭
- **端口检查**: 避免端口冲突

## 扩展和维护

### 添加新脚本
1. 创建Shell脚本文件
2. 添加执行权限
3. 更新本模块文档
4. 测试脚本功能

### 脚本模板
```bash
#!/bin/bash

echo "描述脚本功能..."

# 检查必要条件
if [ ! condition ]; then
    echo "错误信息"
    exit 1
fi

# 执行主要逻辑
echo "执行中..."

# 完成
echo "完成"
```

## 常见问题 (FAQ)

### Q: 可以同时运行多个实例吗？
A: 不建议，端口会冲突。如需多实例，请修改端口配置。

### Q: 如何修改服务端口？
A: 修改对应的脚本文件或配置文件中的端口号。

### Q: 脚本支持Windows吗？
A: 当前脚本为Linux/macOS设计，Windows用户建议使用WSL。

### Q: 如何查看服务状态？
A: 使用`ps aux | grep uvicorn`查看后端，`ps aux | grep vite`查看前端。

## 相关文件清单

### 启动脚本
- `start-all.sh` - 一键启动完整系统
- `start-backend.sh` - 后端服务启动
- `start-frontend.sh` - 前端服务启动

### 管理脚本
- `init-database.sh` - 数据库初始化
- `test-api.sh` - API接口测试

### 配置文件
- `../.env` - 环境变量配置
- `../backend/pyproject.toml` - 后端配置
- `../frontend/package.json` - 前端配置

## 变更记录 (Changelog)

### 2025-11-09 22:13:52 - 自适应初始化架构师系统
- 创建scripts模块文档
- 分析运维脚本功能和依赖关系
- 识别系统启动和测试流程