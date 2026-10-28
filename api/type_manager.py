"""
    Type detection and conversion support,
    in accordance with the specifications.
"""
from datetime import date, datetime
from typing import Any

class TypeManager:

    @staticmethod
    def detect_type(value: Any) -> type:

        if isinstance(value, bool):  return bool
        if isinstance(value, int):   return int
        if isinstance(value, float): return float
        if isinstance(value, date): return date
        if isinstance(value, str): return TypeManager._detect_string_type(value)
        return str


    @staticmethod
    def _detect_string_type(value: str) -> type:

        possible_converters = [
            (int, int),
            (float, float),
            (date.fromisoformat, date),
        ]

        for converter, detected_type in possible_converters:
            try:
                converter(value)
                return detected_type
            except ValueError:
                continue

        #in none worked,
        #then the string will be considered to be of type string!
        return str


    @staticmethod
    def _convert_to_type(value: Any, target_type: type) -> Any:

        if target_type is date and isinstance(value, str) :
            return date.fromisoformat(value)

        return target_type(value)


    @staticmethod
    def validate_and_convert(value: Any, target_type: type) -> Any:
        """Validate and convert value"""
        try:
            return TypeManager._convert_to_type(value, target_type)
        except (ValueError, TypeError) as error:
            raise ValueError(f"Cannot convert {value} to {target_type}: {str(error)}")

