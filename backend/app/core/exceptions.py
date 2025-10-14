"""
自定义异常类
"""
from typing import Any


class TAdminException(Exception):
    """TAdmin 基础异常类"""

    def __init__(
        self,
        message: str = "服务器内部错误",
        status_code: int = 500,
        details: dict[str, Any] | None = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class AuthenticationError(TAdminException):
    """认证异常"""

    def __init__(self, message: str = "认证失败", details: dict[str, Any] | None = None):
        super().__init__(message, 401, details)


class AuthorizationError(TAdminException):
    """授权异常"""

    def __init__(self, message: str = "权限不足", details: dict[str, Any] | None = None):
        super().__init__(message, 403, details)


class ValidationError(TAdminException):
    """数据验证异常"""

    def __init__(self, message: str = "数据验证失败", details: dict[str, Any] | None = None):
        super().__init__(message, 422, details)


class NotFoundError(TAdminException):
    """资源未找到异常"""

    def __init__(self, message: str = "资源未找到", details: dict[str, Any] | None = None):
        super().__init__(message, 404, details)


class BusinessError(TAdminException):
    """业务逻辑异常"""

    def __init__(self, message: str = "业务处理失败", details: dict[str, Any] | None = None):
        super().__init__(message, 400, details)
