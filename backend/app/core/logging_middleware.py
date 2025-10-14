import logging
import time
from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


class LoggingMiddleware(BaseHTTPMiddleware):
    """HTTP请求响应日志中间件"""

    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.logger = logging.getLogger("http")

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        start_time = time.time()

        # 记录请求信息
        client_ip = request.client.host if request.client else "unknown"
        method = request.method
        path = request.url.path
        user_agent = request.headers.get("user-agent", "")

        # 处理请求
        response = await call_next(request)

        # 计算响应时间
        process_time = time.time() - start_time

        # 记录响应信息
        log_record = logging.LogRecord(
            name="http",
            level=logging.INFO,
            pathname=__file__,
            lineno=0,
            msg=f"{method} {path} {response.status_code}",
            args=(),
            exc_info=None
        )

        # 添加额外字段
        log_record.client_ip = client_ip
        log_record.method = method
        log_record.path = path
        log_record.status_code = response.status_code
        log_record.response_time = round(process_time * 1000, 2)  # 毫秒
        log_record.user_agent = user_agent

        # 记录日志
        self.logger.handle(log_record)

        # 添加响应头
        response.headers["X-Response-Time"] = f"{process_time:.3f}s"

        return response


class ErrorLoggingMiddleware(BaseHTTPMiddleware):
    """错误日志中间件"""

    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.logger = logging.getLogger("error")

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        try:
            response = await call_next(request)

            # 记录4xx和5xx错误
            if response.status_code >= 400:
                self._log_error(request, response)

            return response

        except Exception as exc:
            # 记录未捕获的异常
            self._log_exception(request, exc)
            raise

    def _log_error(self, request: Request, response: Response) -> None:
        """记录HTTP错误"""
        client_ip = request.client.host if request.client else "unknown"
        method = request.method
        path = request.url.path

        self.logger.error(
            f"HTTP Error {response.status_code}: {method} {path}",
            extra={
                "extra_fields": {
                    "client_ip": client_ip,
                    "method": method,
                    "path": path,
                    "status_code": response.status_code,
                    "error_type": "http_error"
                }
            }
        )

    def _log_exception(self, request: Request, exc: Exception) -> None:
        """记录异常"""
        client_ip = request.client.host if request.client else "unknown"
        method = request.method
        path = request.url.path

        self.logger.error(
            f"Unhandled exception: {str(exc)}",
            exc_info=True,
            extra={
                "extra_fields": {
                    "client_ip": client_ip,
                    "method": method,
                    "path": path,
                    "error_type": "unhandled_exception"
                }
            }
        )
