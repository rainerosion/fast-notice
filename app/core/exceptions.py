"""
Custom exceptions for the application
"""
from app.core.errors import ErrorCode


class BusinessException(Exception):
    """
    Business Exception
    """

    def __init__(self, code: int, message: str):
        self.error_code = code
        self.message = message


class UnauthorizedException(Exception):
    """
    Unauthorized Exception
    """

    def __init__(self, code: int, message: str):
        self.error_code = code
        self.message = message


class ForbiddenException(Exception):
    """
    Forbidden Exception
    """

    def __init__(self, code: int, message: str):
        self.error_code = code
        self.message = message


"""
Exception utility
"""


class ExceptionUtil:

    @staticmethod
    def raise_business_exception(error_code: ErrorCode):
        code, message = error_code.value
        raise BusinessException(code, message)

    @staticmethod
    def raise_unauthorized_exception(error_code: ErrorCode):
        code, message = error_code.value
        raise UnauthorizedException(code, message)

    @staticmethod
    def raise_forbidden_exception(error_code: ErrorCode):
        code, message = error_code.value
        raise ForbiddenException(code, message)
