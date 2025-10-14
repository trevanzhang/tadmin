import json
import logging
import sys
from datetime import datetime
from pathlib import Path


class JSONFormatter(logging.Formatter):
    """JSON格式的日志格式化器"""

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # 添加额外字段
        if hasattr(record, 'extra_fields') and record.extra_fields:
            log_entry.update(record.extra_fields)

        # 添加异常信息
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry, ensure_ascii=False)


class RequestResponseFormatter(logging.Formatter):
    """HTTP请求响应日志格式化器"""

    def format(self, record: logging.LogRecord) -> str:
        # 从extra参数中获取字段
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "type": "http_request",
            "client_ip": getattr(record, 'client_ip', 'unknown'),
            "method": getattr(record, 'method', 'unknown'),
            "path": getattr(record, 'path', 'unknown'),
            "status_code": getattr(record, 'status_code', None),
            "response_time": getattr(record, 'response_time', None),
            "user_agent": getattr(record, 'user_agent', ''),
        }

        return json.dumps(log_entry, ensure_ascii=False)


def setup_logging() -> logging.Logger:
    """设置日志配置"""
    # 创建日志目录
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # 配置根日志器
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # 清除现有的处理器
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # 控制台处理器 - 用于开发环境
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)

    # 文件处理器 - JSON格式，用于生产环境
    file_handler = logging.FileHandler(
        log_dir / "app.log",
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    json_formatter = JSONFormatter()
    file_handler.setFormatter(json_formatter)

    # 请求日志处理器
    request_handler = logging.FileHandler(
        log_dir / "requests.log",
        encoding='utf-8'
    )
    request_handler.setLevel(logging.INFO)
    request_formatter = RequestResponseFormatter()
    request_handler.setFormatter(request_formatter)

    # 错误日志处理器
    error_handler = logging.FileHandler(
        log_dir / "errors.log",
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(json_formatter)

    # 添加处理器
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(error_handler)

    # 为http_request日志器添加专门的请求日志处理器
    http_request_logger = logging.getLogger("http_request")
    http_request_logger.setLevel(logging.INFO)
    http_request_logger.addHandler(request_handler)
    http_request_logger.propagate = False  # 防止重复记录

    # 设置特定模块的日志级别
    logging.getLogger("uvicorn.access").handlers = []
    logging.getLogger("uvicorn.error").handlers = []

    return root_logger


def get_logger(name: str) -> logging.Logger:
    """获取指定名称的日志器"""
    return logging.getLogger(name)


# 常用日志器
app_logger = get_logger("app")
database_logger = get_logger("database")
auth_logger = get_logger("auth")
api_logger = get_logger("api")
