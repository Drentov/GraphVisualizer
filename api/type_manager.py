"""
    Type detection and conversion support,
    we support the data types mentioned in
    the specifications.
"""
from datetime import date
from typing import Union, Dict

SupportedValue = Union[bool, int, float, date, str]
SupportedType = type[SupportedValue]
SUPPORTED_TYPES = (bool, int, float, date, str)

#usefult for to_dict functions, where 'attribute' is a nestled dictionary
SupportedValueOrDict = Union[SupportedValue, Dict[str, SupportedValue]]

class TypeManager:

    @staticmethod
    def detect_type(value: SupportedValue) -> SupportedType:

        #loops over all supported types until it finds what the type of value is
        for supported_type in SUPPORTED_TYPES:

            if supported_type is str:
                if isinstance(value, str): return TypeManager.detect_string_type(value)

            if isinstance(value, supported_type): return supported_type

        return str


    @staticmethod
    def detect_string_type(value: str) -> SupportedType:

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
    def _convert_to_type(value: object, target_type: SupportedType) -> SupportedValue:

        if target_type not in SUPPORTED_TYPES:
            raise TypeError(f"Unsupported target type: {target_type}")

        if isinstance(value, target_type): #If no type conversion necessary, do nothing!
            return value

        if target_type is date and isinstance(value, str) :
            return date.fromisoformat(value)

        return target_type(value)


    @staticmethod
    def validate_and_convert(value: object, target_type: SupportedType) -> SupportedValue:
        """Validate and convert value"""
        try:
            return TypeManager._convert_to_type(value, target_type)
        except (ValueError, TypeError) as error:
            raise ValueError(f"Cannot convert {value} to {target_type}: {str(error)}")

