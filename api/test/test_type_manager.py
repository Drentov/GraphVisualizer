"""
Unit tests for TypeManager.
"""
import unittest
from datetime import date
from api.type_manager import TypeManager

class TestTypeManager(unittest.TestCase):

    # ---------------------------------------------------------
    # detect_type()
    # ---------------------------------------------------------

    def test_detect_type(self):

        test_cases = [
            # (input, expected_output)
            (True, bool),
            (False, bool),
            (42, int),
            (-15, int),
            (3.14, float),
            (-2.5, float),
            (date(2026, 10, 30), date),

            # Strings are further analyzed
            ("42", int),
            ("3.14", float),
            ("2026-10-30", date),
            ("Hello World", str),
        ]

        for input_value, expected_output in test_cases:
            with self.subTest(input=input_value):
                self.assertEqual(
                    TypeManager.detect_type(input_value),
                    expected_output
                )

    # ---------------------------------------------------------
    # detect_string_type()
    # ---------------------------------------------------------

    def test_detect_string_type(self):

        test_cases = [
            # (input, expected_output)
            ("42", int),
            ("-15", int),
            ("3.14", float),
            ("-2.5", float),
            ("2026-10-30", date),
            ("Hello World", str),
            ("", str),
            ("12.5.8", str),
        ]

        for input_value, expected_output in test_cases:
            with self.subTest(input=input_value):
                self.assertEqual(
                    TypeManager.detect_string_type(input_value),
                    expected_output
                )

    # ---------------------------------------------------------
    # _convert_to_type()
    # ---------------------------------------------------------

    def test_convert_to_type(self):

        test_cases = [
            # (input, target_type, expected_output)
            (42, str, "42"),
            ("42", int, 42),
            ("3.14", float, 3.14),
            (1, float, 1.0),
            (0, bool, False),
            (1, bool, True),
            ("True", bool, True),
            ("False", bool, True),
            ("2026-10-30", date, date(2026, 10, 30)),
            (date(2026, 10, 30), str, "2026-10-30"),
        ]

        for input_value, target_type, expected_output in test_cases:
            with self.subTest(
                input=input_value,
                target_type=target_type
            ):
                self.assertEqual(
                    TypeManager._convert_to_type(input_value, target_type),
                    expected_output
                )

    def test_convert_to_type_unsupported_target(self):

        test_cases = [
            (42, list),
            ("Hello", dict),
            (3.14, tuple),
        ]

        for input_value, target_type in test_cases:
            with self.subTest(target_type=target_type):
                with self.assertRaises(TypeError):
                    TypeManager._convert_to_type(
                        input_value,
                        target_type
                    )

    def test_convert_to_type_invalid_conversion(self):

        test_cases = [
            ("Hello", int),
            ("3.14.15", float),
            ("Not a date", date),
        ]

        for input_value, target_type in test_cases:
            with self.subTest(
                input=input_value,
                target_type=target_type
            ):
                with self.assertRaises(ValueError):
                    TypeManager._convert_to_type(
                        input_value,
                        target_type
                    )

    # ---------------------------------------------------------
    # validate_and_convert()
    # ---------------------------------------------------------

    def test_validate_and_convert(self):

        test_cases = [
            # (input, target_type, expected_output)
            ("42", int, 42),
            ("3.14", float, 3.14),
            (42, str, "42"),
            (0, bool, False),
            (1, bool, True),
            ("True", bool, True),
            ("2026-10-30", date, date(2026, 10, 30)),
            (date(2026, 10, 30), str, "2026-10-30"),
        ]

        for input_value, target_type, expected_output in test_cases:
            with self.subTest(
                input=input_value,
                target_type=target_type
            ):
                self.assertEqual(
                    TypeManager.validate_and_convert(
                        input_value,
                        target_type
                    ),
                    expected_output
                )

    def test_validate_and_convert_invalid(self):

        test_cases = [
            ("Hello", int),
            ("Not a date", date),
            ("3.14.15", float),
            (42, list),
        ]

        for input_value, target_type in test_cases:
            with self.subTest(
                input=input_value,
                target_type=target_type
            ):
                with self.assertRaises(ValueError):
                    TypeManager.validate_and_convert(
                        input_value,
                        target_type
                    )


if __name__ == "__main__":
    unittest.main()
