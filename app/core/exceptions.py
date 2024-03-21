"""
Custom exceptions for the application
"""


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
