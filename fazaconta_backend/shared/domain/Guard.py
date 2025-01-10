from enum import Enum
from typing import Type


class GuardException(Exception): ...


class Guard:
    @staticmethod
    def against_empty_list(argument: list, argument_name) -> None:
        """
        Raises GuardException if argument is an empty list.
        """
        if len(argument) == 0:
            raise GuardException(f"{argument_name} cannot be empty.")

    @staticmethod
    def greater_than(min_value: float, actual_value: float) -> None:
        """
        Raises GuardException if actual_value is NOT strictly greater than min_value.
        """
        if not (actual_value > min_value):
            raise GuardException(
                f"Number given ({actual_value}) is not greater than ({min_value})."
            )

    @staticmethod
    def against_empty_str(argument: object, argument_name: str) -> None:
        """
        Raises GuardException if argument is a empty string.
        """
        if str(argument) == "":
            raise GuardException(f"{argument_name} cannot be a empty.")

    @staticmethod
    def against_empty_str_bulk(args: list[dict]) -> None:
        """
        Expects a list of dicts with keys: 'argument' and 'argumentName'.
        For each item, raises GuardException if the argument is an empty string.
        Example of args:
          [
            {"argument": user_input, "argumentName": "user_input"},
            {"argument": count,      "argumentName": "count"}
          ]
        """
        for arg_item in args:
            Guard.against_empty_str(arg_item["argument"], arg_item["argumentName"])

    @staticmethod
    def against_at_least(num_chars: int, text: str) -> None:
        """
        Raises GuardException if text is shorter than num_chars.
        """
        if len(text) < num_chars:
            raise GuardException(f"Text is not at least {num_chars} characters long.")

    @staticmethod
    def against_at_most(num_chars: int, text: str) -> None:
        """
        Raises GuardException if text is longer than num_chars.
        """
        if len(text) > num_chars:
            raise GuardException(f"Text is greater than {num_chars} characters.")

    @staticmethod
    def against_undefined(argument: object, argument_name: str) -> None:
        """
        Raises GuardException if the argument is None.
        (Python does not distinguish between null and undefined like TypeScript.)
        """
        if argument is None:
            raise GuardException(f"{argument_name} is undefined.")

    @staticmethod
    def against_undefined_bulk(args: list[dict]) -> None:
        """
        Expects a list of dicts with keys: 'argument' and 'argumentName'.
        For each item, raises GuardException if the argument is None.
        Example of args:
          [
            {"argument": user_input, "argumentName": "user_input"},
            {"argument": count,      "argumentName": "count"}
          ]
        """
        for arg_item in args:
            Guard.against_undefined(arg_item["argument"], arg_item["argumentName"])

    @staticmethod
    def is_one_of(value: object, valid_values: list, argument_name: str) -> None:
        """
        Raises GuardException if value is not in the list of valid_values.
        """
        if value not in valid_values:
            raise GuardException(
                f'{argument_name} must be one of {valid_values}. Got "{value}".'
            )

    @staticmethod
    def is_one_of_enum(value, enum_class: Type[Enum], argument_name: str) -> None:
        """
        Raises GuardException if value is not in enum class.
        """
        values = set(item.value for item in enum_class)
        if not value in values:
            raise GuardException(
                f'{argument_name} must be one of {values}. Got "{value}".'
            )

    @staticmethod
    def in_range(
        num: float, min_value: float, max_value: float, argument_name: str
    ) -> None:
        """
        Raises GuardException if num is not between [min_value, max_value].
        """
        if not (min_value <= num <= max_value):
            raise GuardException(
                f"{argument_name} is not within range [{min_value}, {max_value}]."
            )

    @staticmethod
    def all_in_range(
        numbers: list[float], min_value: float, max_value: float, argument_name: str
    ) -> None:
        """
        Raises GuardException if any number in the list is out of [min_value, max_value].
        """
        for num in numbers:
            if not (min_value <= num <= max_value):
                raise GuardException(
                    f"One of the values for '{argument_name}' is not within the range [{min_value}, {max_value}]."
                )
