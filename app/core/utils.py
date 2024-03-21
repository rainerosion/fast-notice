"""
ConditionUtils
"""
from typing import Any

from app.core.errors import ErrorCode
from app.core.exceptions import ExceptionUtil


class ConditionUtils:

    @staticmethod
    def must_not_none(obj: Any, error_enum: ErrorCode):
        """
        validate obj is not None
        :param obj:
        :param error_enum:
        :return:
        """
        ConditionUtils.must(obj is not None, error_enum)

    @staticmethod
    def must_not_empty(obj: Any, error_enum: ErrorCode):
        """
        validate obj is not empty
        :param obj:
        :param error_enum:
        :return:
        """
        ConditionUtils.must(obj, error_enum)

    @staticmethod
    def must_equals(obj1: Any, obj2: Any, error_enum: ErrorCode):
        """
        validate obj1 equals obj2
        :param obj1:
        :param obj2:
        :param error_enum:
        :return:
        """
        ConditionUtils.must(obj1 == obj2, error_enum)

    @staticmethod
    def must_not_equals(obj1: Any, obj2: Any, error_enum: ErrorCode):
        """
        validate obj1 not equals obj2
        :param obj1:
        :param obj2:
        :param error_enum:
        :return:
        """
        ConditionUtils.must(obj1 != obj2, error_enum)

    @staticmethod
    def must(b: bool, error_enum: ErrorCode):
        """
        validate b is True
        :param b:
        :param error_enum:
        :return:
        """
        if not b:
            ExceptionUtil.raise_business_exception(error_enum)
