from enum import Enum


class ErrorCode(Enum):
    """
    Define error code
    """
    USER_NOT_FOUND = (1001, "用户不存在")
    USER_LOGIN_FAILED = (1002, "用户名或密码错误")
    USER_INACTIVE = (1003, "用户未激活")
    USER_NOT_SUPERUSER = (1004, "用户不是超级用户")
    # 无法验证凭据
    USER_CREDENTIALS_INVALID = (1005, "无法验证凭据")
    USER_NOT_LOGGED_IN = (1006, "用户未登录")
