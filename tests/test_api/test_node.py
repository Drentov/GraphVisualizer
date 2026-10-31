
"""
Unit tests for the Node implementation.
Tests interact through the BaseNode interface.
"""

import unittest
from datetime import date

from api.models.implementation.node import Node

class TestNode(unittest.TestCase):

    def setUp(self):
        # Instantiate implementation
        self.node: Node = Node(
            1,
            name="Alice",
            age=25,
            height=1.75,
            active=True,
            birthday=date(2001, 5, 12)
        )

    # ---------------------------------------------------------
    # Construction
    # ---------------------------------------------------------

    def test_initialization(self):

        test_cases = [
            # (input, expected_output)
            (self.node.get_attribute("name"), "Alice"),
            (self.node.get_attribute("age"), 25),
            (self.node.get_attribute("height"), 1.75),
            (self.node.get_attribute("active"), True),
            (self.node.get_attribute("birthday"), date(2001, 5, 12)),
        ]

        for input_value, expected_output in test_cases:
            with self.subTest(input=input_value):
                self.assertEqual(input_value, expected_output)

        self.assertEqual(self.node.node_id, "1")

    # ---------------------------------------------------------
    # set_attribute()
    # ---------------------------------------------------------

    def test_set_attribute(self):

        test_cases = [
            # (input, expected_output)
            (("score", 100), 100),
            (("description", "Test node"), "Test node"),
            (("ratio", 2.5), 2.5),
            (("enabled", False), False),
            (("created", date(2026, 10, 30)), date(2026, 10, 30)),
            (("numeric_string", "42"), 42),
        ]

        for input_value, expected_output in test_cases:
            key, value = input_value

            with self.subTest(input=input_value):
                self.node.set_attribute(key, value)
                self.assertEqual(
                    self.node.get_attribute(key),
                    expected_output
                )

    # ---------------------------------------------------------
    # get_attribute()
    # ---------------------------------------------------------

    def test_get_attribute(self):

        test_cases = [
            # (input, expected_output)
            ("name", "Alice"),
            ("age", 25),
            ("height", 1.75),
            ("active", True),
            ("birthday", date(2001, 5, 12)),
            ("nonexistent", None),
        ]

        for input_value, expected_output in test_cases:
            with self.subTest(input=input_value):
                self.assertEqual(
                    self.node.get_attribute(input_value),
                    expected_output
                )

    # ---------------------------------------------------------
    # update_attribute()
    # ---------------------------------------------------------

    def test_update_attribute(self):

        test_cases = [
            # (input, expected_output)
            (("age", 30), 30),
            (("name", "Bob"), "Bob"),
            (("height", 1.85), 1.85),
            (("active", False), False),
            (("age", "35"), 35),
        ]

        for input_value, expected_output in test_cases:
            key, value = input_value

            with self.subTest(input=input_value):
                self.node.update_attribute(key, value)

                self.assertEqual(
                    self.node.get_attribute(key),
                    expected_output
                )

    def test_update_nonexistent_attribute(self):

        test_cases = [
            # (input, expected_output)
            (("new_attribute", 42), 42),
            (("another_attribute", "Hello"), "Hello"),
        ]

        for input_value, expected_output in test_cases:
            key, value = input_value

            with self.subTest(input=input_value):
                self.node.update_attribute(key, value)

                self.assertEqual(
                    self.node.get_attribute(key),
                    expected_output
                )

    # ---------------------------------------------------------
    # delete_attribute()
    # ---------------------------------------------------------

    def test_delete_attribute(self):

        test_cases = [
            # (input, expected_output)
            ("name", False),
            ("age", False),
            ("height", False),
            ("active", False),
        ]

        for input_value, expected_output in test_cases:
            with self.subTest(input=input_value):
                self.node.delete_attribute(input_value)

                self.assertEqual(
                    self.node.has_attribute(input_value),
                    expected_output
                )

    def test_delete_nonexistent_attribute(self):

        # Deleting an attribute that doesn't exist should do nothing.
        self.node.delete_attribute("nonexistent")

        self.assertEqual(
            self.node.get_all_attributes(),
            {
                "name": "Alice",
                "age": 25,
                "height": 1.75,
                "active": True,
                "birthday": date(2001, 5, 12)
            }
        )

    # ---------------------------------------------------------
    # get_attribute_type()
    # ---------------------------------------------------------

    def test_get_attribute_type(self):

        test_cases = [
            # (input, expected_output)
            ("name", str),
            ("age", int),
            ("height", float),
            ("active", bool),
            ("birthday", date),
        ]

        for input_value, expected_output in test_cases:
            with self.subTest(input=input_value):
                self.assertIs(
                    self.node.get_attribute_type(input_value),
                    expected_output
                )

    def test_get_attribute_type_nonexistent(self):

        with self.assertRaises(KeyError):
            self.node.get_attribute_type("nonexistent")

    # ---------------------------------------------------------
    # get_all_attributes()
    # ---------------------------------------------------------

    def test_get_all_attributes(self):

        expected_output = {
            "name": "Alice",
            "age": 25,
            "height": 1.75,
            "active": True,
            "birthday": date(2001, 5, 12)
        }

        self.assertEqual(
            self.node.get_all_attributes(),
            expected_output
        )

    def test_get_all_attributes_returns_copy(self):

        # Modify the returned dictionary.
        attributes = self.node.get_all_attributes()
        attributes["age"] = 999
        attributes["new_attribute"] = "Injected"

        # Original node must remain unchanged.
        self.assertEqual(self.node.get_attribute("age"), 25)
        self.assertIsNone(
            self.node.get_attribute("new_attribute")
        )

    # ---------------------------------------------------------
    # has_attribute()
    # ---------------------------------------------------------

    def test_has_attribute(self):

        test_cases = [
            # (input, expected_output)
            ("name", True),
            ("age", True),
            ("height", True),
            ("active", True),
            ("NAME", True),
            ("Age", True),
            ("nam", True),
            ("eight", True),
            ("nonexistent", False),
            ("", False),
        ]

        for input_value, expected_output in test_cases:
            with self.subTest(input=input_value):
                self.assertEqual(
                    self.node.has_attribute(input_value),
                    expected_output
                )

    # ---------------------------------------------------------
    # __repr__()
    # ---------------------------------------------------------

    def test_repr(self):

        test_cases = [
            # (input, expected_output)
            (
                Node(1, name="Alice", age=25),
                "Node(1, name=Alice, age=25)"
            ),
            (
                Node("A"),
                "Node(A, )"
            ),
            (
                Node(2, active=True),
                "Node(2, active=True)"
            ),
        ]

        for input_value, expected_output in test_cases:
            with self.subTest(input=input_value):
                self.assertEqual(
                    repr(input_value),
                    expected_output
                )

    # ---------------------------------------------------------
    # __eq__()
    # ---------------------------------------------------------

    def test_equality(self):

        node_a = Node(1, name="Alice")
        node_b = Node(1, name="Bob")
        node_c = Node(2, name="Alice")

        test_cases = [
            # (input, expected_output)
            ((node_a, node_b), True),
            ((node_a, node_c), False),
            ((node_a, node_a), True),
            ((node_a, "1"), False),
            ((node_a, None), False),
        ]

        for input_value, expected_output in test_cases:
            left, right = input_value

            with self.subTest(input=input_value):
                self.assertEqual(
                    left == right,
                    expected_output
                )

    # ---------------------------------------------------------
    # to_dict()
    # ---------------------------------------------------------

    def test_to_dict(self):

        expected_output = {
            "id": "1",
            "attributes": {
                "name": "Alice",
                "age": 25,
                "height": 1.75,
                "active": True,
                "birthday": date(2001, 5, 12)
            }
        }

        self.assertEqual(
            self.node.to_dict(),
            expected_output
        )


if __name__ == "__main__":
    unittest.main()
