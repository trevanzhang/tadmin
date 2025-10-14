import re
from datetime import datetime, timedelta
from typing import Any

import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(subject: str | Any, expires_delta: timedelta | None = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject), "type": "access"}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: str | Any) -> str:
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str, expected_type: str = "access") -> dict[str, Any] | None:
    try:
        payload: dict[str, Any] = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != expected_type:
            return None
        return payload
    except jwt.PyJWTError:
        return None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def validate_password_strength(password: str) -> tuple[bool, list[str]]:
    """
    验证密码强度

    Args:
        password: 要验证的密码

    Returns:
        tuple[bool, list[str]]: (是否通过验证, 错误消息列表)
    """
    errors = []

    # 最小长度检查
    if len(password) < 8:
        errors.append("密码长度至少需要8个字符")

    # 最大长度检查
    if len(password) > 128:
        errors.append("密码长度不能超过128个字符")

    # 包含大写字母检查
    if not re.search(r'[A-Z]', password):
        errors.append("密码必须包含至少一个大写字母")

    # 包含小写字母检查
    if not re.search(r'[a-z]', password):
        errors.append("密码必须包含至少一个小写字母")

    # 包含数字检查
    if not re.search(r'\d', password):
        errors.append("密码必须包含至少一个数字")

    # 包含特殊字符检查
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append("密码必须包含至少一个特殊字符 (!@#$%^&*(),.?\":{}|<>) ")

    # 常见弱密码检查
    weak_passwords = [
        'password', '123456', '12345678', '123456789', '1234567890',
        'admin', 'qwerty', 'abc123', 'letmein', 'welcome', 'monkey',
        'password1', '1234567', '123123', '111111', 'sunshine', 'iloveyou'
    ]
    if password.lower() in weak_passwords:
        errors.append("密码太常见，请使用更复杂的密码")

    # 连续字符检查
    if re.search(r'(.)\1{2,}', password):
        errors.append("密码不能包含连续重复的字符")

    # 连续数字检查
    if re.search(r'(012|123|234|345|456|567|678|789|890)', password):
        errors.append("密码不能包含连续的数字序列")

    return len(errors) == 0, errors


def get_password_strength_score(password: str) -> int:
    """
    计算密码强度分数 (0-100)

    Args:
        password: 要评估的密码

    Returns:
        int: 密码强度分数 (0-100)
    """
    score = 0

    # 长度分数
    if len(password) >= 8:
        score += 10
    if len(password) >= 12:
        score += 10
    if len(password) >= 16:
        score += 10

    # 字符类型分数
    if re.search(r'[A-Z]', password):
        score += 10
    if re.search(r'[a-z]', password):
        score += 10
    if re.search(r'\d', password):
        score += 10
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 10

    # 字符组合分数
    char_types = 0
    if re.search(r'[A-Z]', password):
        char_types += 1
    if re.search(r'[a-z]', password):
        char_types += 1
    if re.search(r'\d', password):
        char_types += 1
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        char_types += 1

    if char_types >= 3:
        score += 10
    if char_types == 4:
        score += 10

    # 熵分数 (基于字符集大小)
    charset_size = 0
    if re.search(r'[a-z]', password):
        charset_size += 26
    if re.search(r'[A-Z]', password):
        charset_size += 26
    if re.search(r'\d', password):
        charset_size += 10
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        charset_size += 20

    if charset_size >= 50:
        score += 10

    # 弱密码惩罚
    weak_passwords = [
        'password', '123456', '12345678', '123456789', '1234567890',
        'admin', 'qwerty', 'abc123', 'letmein', 'welcome', 'monkey'
    ]
    if password.lower() in weak_passwords:
        score = max(0, score - 50)

    return min(100, score)
