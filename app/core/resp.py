from typing import TypeVar, Generic

from pydantic import BaseModel

T = TypeVar('T')


class Result(BaseModel, Generic[T]):
    code: int
    msg: str
    data: T = None

    @staticmethod
    def success(*, data: T = None, msg: str = "success"):
        """
        Success response
        :param data: response data
        :param msg: response message
        :return:
        """
        return Result[T](code=200, msg=msg, data=data)

    @staticmethod
    def error(*, code: str, msg: str):
        """
        Error response
        :param code: error code
        :param msg: error message
        :return:
        """
        return Result(code=code, msg=msg)
