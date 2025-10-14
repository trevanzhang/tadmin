"""
全局中间件
"""
import logging
import time
import uuid
from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.exceptions import TAdminException

logger = logging.getLogger("middleware")


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """安全头中间件"""

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        response = await call_next(request)

        # 添加安全头
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # 在生产环境中添加HSTS
        if not getattr(request.app.state, 'DEBUG', True):
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        return response


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """请求日志中间件"""

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        # 生成请求ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        # 记录请求开始时间
        start_time = time.time()

        # 记录请求信息
        client_ip = request.client.host if request.client else "unknown"
        method = request.method
        url = str(request.url)

        # 调试日志
        logger.info(f"RequestLoggingMiddleware: {method} {request.url.path} from {client_ip}")

        # 创建请求日志记录 - 使用extra参数
        request_logger = logging.getLogger("http_request")
        request_logger.info(
            "HTTP请求开始",
            extra={
                "client_ip": client_ip,
                "method": method,
                "path": request.url.path,
                "user_agent": request.headers.get("user-agent", ""),
                "status_code": None,
                "response_time": None
            }
        )

        try:
            # 处理请求
            response = await call_next(request)

            # 计算处理时间
            process_time = time.time() - start_time

            # 记录响应信息
            request_logger.info(
                "HTTP请求完成",
                extra={
                    "client_ip": client_ip,
                    "method": method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "response_time": process_time,
                    "user_agent": request.headers.get("user-agent", "")
                }
            )

            # 添加响应头
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = f"{process_time:.3f}"

            return response

        except Exception as e:
            # 计算处理时间
            process_time = time.time() - start_time

            # 记录错误信息
            log_record = request_logger.makeRecord(
                request_logger.name,
                logging.ERROR,
                "", 0,  # filename, lineno
                "HTTP请求失败",
                (), None  # args, exc_info
            )
            # 设置自定义属性
            log_record.client_ip = client_ip
            log_record.method = method
            log_record.path = request.url.path
            log_record.status_code = 500
            log_record.response_time = process_time
            log_record.user_agent = request.headers.get("user-agent", "")
            log_record.error = str(e)

            request_logger.handle(log_record)

            # 重新抛出异常让全局异常处理器处理
            raise


class GlobalExceptionHandler:
    """全局异常处理器"""

    @staticmethod
    async def tadmin_exception_handler(request: Request, exc: Exception) -> Response:
        """处理自定义异常"""
        if not isinstance(exc, TAdminException):
            # 如果不是TAdminException，让通用异常处理器处理
            return await GlobalExceptionHandler.general_exception_handler(request, exc)

        logger.error(
            f"自定义异常 [{getattr(request.state, 'request_id', 'unknown')}]: {exc.message}",
            extra={
                "request_id": getattr(request.state, 'request_id', 'unknown'),
                "exception_type": type(exc).__name__,
                "error_message": exc.message,
                "details": exc.details,
                "status_code": exc.status_code,
            }
        )

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": type(exc).__name__,
                    "message": exc.message,
                    "details": exc.details,
                },
                "timestamp": time.time(),
                "request_id": getattr(request.state, 'request_id', 'unknown'),
            }
        )

    @staticmethod
    async def http_exception_handler(request: Request, exc: Exception) -> Response:
        """处理HTTP异常"""
        if not isinstance(exc, StarletteHTTPException):
            # 如果不是HTTP异常，让通用异常处理器处理
            return await GlobalExceptionHandler.general_exception_handler(request, exc)

        logger.error(
            f"HTTP异常 [{getattr(request.state, 'request_id', 'unknown')}]: {str(exc)}",
            extra={
                "request_id": getattr(request.state, 'request_id', 'unknown'),
                "exception_type": type(exc).__name__,
                "error_message": str(exc),
            }
        )

        return JSONResponse(
            status_code=getattr(exc, 'status_code', 500),
            content={
                "success": False,
                "error": {
                    "code": type(exc).__name__,
                    "message": str(exc),
                },
                "timestamp": time.time(),
                "request_id": getattr(request.state, 'request_id', 'unknown'),
            }
        )

    @staticmethod
    async def general_exception_handler(request: Request, exc: Exception) -> Response:
        """处理通用异常"""
        logger.error(
            f"未处理异常 [{getattr(request.state, 'request_id', 'unknown')}]: {str(exc)}",
            extra={
                "request_id": getattr(request.state, 'request_id', 'unknown'),
                "exception_type": type(exc).__name__,
                "error_message": str(exc),
            },
            exc_info=True
        )

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": {
                    "code": "InternalServerError",
                    "message": "服务器内部错误" if not getattr(request.app.state, 'DEBUG', True) else str(exc),
                },
                "timestamp": time.time(),
                "request_id": getattr(request.state, 'request_id', 'unknown'),
            }
        )
