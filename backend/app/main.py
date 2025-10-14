from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, routes, users
from app.core.config import settings
from app.core.database import create_db_and_tables
from app.core.exceptions import TAdminException
from app.core.global_middleware import (
    GlobalExceptionHandler,
    RequestLoggingMiddleware,
    SecurityHeadersMiddleware,
)
from app.core.logging_config import setup_logging

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    openapi_url="/api/v1/openapi.json"
)

# 配置日志系统
setup_logging()

# 设置应用状态
app.state.DEBUG = True  # 开发环境设为True

# 配置全局中间件
app.add_middleware(SecurityHeadersMiddleware)  # 安全头中间件
app.add_middleware(RequestLoggingMiddleware)   # 请求日志中间件（带请求ID）

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册全局异常处理器
app.add_exception_handler(TAdminException, GlobalExceptionHandler.tadmin_exception_handler)
app.add_exception_handler(HTTPException, GlobalExceptionHandler.http_exception_handler)
app.add_exception_handler(Exception, GlobalExceptionHandler.general_exception_handler)

# 包含路由
app.include_router(auth.router, prefix="/api/v1/auth", tags=["认证"])
app.include_router(users.router, prefix="/api/v1/users", tags=["用户"])
app.include_router(routes.router, prefix="/api/v1", tags=["路由"])


@app.on_event("startup")
def on_startup() -> None:
    create_db_and_tables()


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Tadmin API 服务运行中"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}


@app.get("/test/error")
def test_error() -> None:
    """测试异常处理端点"""
    # 测试自定义异常
    from app.core.exceptions import NotFoundError
    raise NotFoundError("测试资源未找到异常", {"resource": "test", "id": 123})


@app.get("/test/validation")
def test_validation() -> None:
    """测试验证异常"""
    from app.core.exceptions import ValidationError
    raise ValidationError("测试数据验证失败", {"field": "username", "reason": "不能为空"})


@app.get("/test/general")
def test_general() -> None:
    """测试通用异常"""
    # 模拟未处理的异常
    raise ValueError("这是一个测试的通用异常")
