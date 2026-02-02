"""
用户上下文管理

用于在请求中传递用户认证信息到 Langfuse 追踪
"""

from contextvars import ContextVar
from typing import Optional

# 使用 contextvars 存储当前请求的用户 token
# 这样可以在异步环境中正确传递用户上下文
current_user_token: ContextVar[Optional[str]] = ContextVar("current_user_token", default=None)


def set_user_token(token: str):
    """设置当前请求的用户 token"""
    current_user_token.set(token)


def get_user_token() -> Optional[str]:
    """获取当前请求的用户 token"""
    return current_user_token.get()


def get_masked_token() -> Optional[str]:
    """获取脱敏后的 token（只显示前后4位）"""
    token = current_user_token.get()
    if not token:
        return None
    if len(token) <= 8:
        return token[:2] + "****" + token[-2:]
    return token[:4] + "****" + token[-4:]


def clear_user_context():
    """清除用户上下文"""
    current_user_token.set(None)
