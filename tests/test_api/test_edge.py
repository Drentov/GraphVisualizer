
"""
Unit tests for the Edge implementation.
Tests interact through the BaseEdge interface.
"""

import unittest

from api.models.implementation.edge import Edge
from api.models.implementation.node import Node


class TestEdge(unittest.TestCase):

    def setUp(self):
        self.node_a = Node("A", name="Alice")
        self.node_b = Node("B", name="Bob")
        self.node_c = Node("C", name="Charlie")

        # Instantiate implementation
        self.edge: Edge = Edge(
            1,
            self.node_a,
            self.node_b,
            weight=10,
            label="Friendship",
            active=True
        )

    # ---------------------------------------------------------
    # Construction
    # ---------------------------------------------------------

    def test_initialization(self):

        test_cases = [
            # (input, expected_output)
            (self.edge.get_attribute("weight"), 10),
            (self.edge.get_attribute("label"), "Friendship"),
            (self.edge.get_attribute("active"), True),
        ]

        for input_value, expected_output in test_cases:
            with self.subTest(input=input_value):
                self.assertEqual(input_value, expected_output)

        self.assertEqual(self.edge.edge_id, "1")
        self.assertIs(self.edge.get_source_node(), self.node_a)
        self.assertIs(self.edge.get_destination_node(), self.node_b)
        self.assertFalse(self.edge.is_directed())

    def test_initialization_without_weight(self):

        edge: Edge = Edge(2, self.node_a, self.node_b)

        self.assertIsNone(edge.get_attribute("weight"))
        self.assertEqual(edge.get_all_attributes(), {})

    def test_initialization_with_directed_edge(self):

        edge: Edge = Edge(
            3,
            self.node_a,
            self.node_b,
            directed=True
        )

        self.assertTrue(edge.is_directed())

    # ---------------------------------------------------------
    # set_attribute()
    # ---------------------------------------------------------

    def test_set_attribute(self):

        test_cases = [
            # (input, expected_output)
            (("score", 100), 100),
            (("description", "Test edge"), "Test edge"),
            (("ratio", 2.5), 2.5),
            (("enabled", False), False),
            (("numeric_string", "42"), 42),
        ]

        for input_value, expected_output in test_cases:
            key, value = input_value

            with self.subTest(input=input_value):
                self.edge.set_attribute(key, value)

                self.assertEqual(
                    self.edge.get_attribute(key),
                    expected_output
                )

    # ---------------------------------------------------------
    # get_source_node()
    # ---------------------------------------------------------

    def test_get_source_node(self):

        self.assertIs(
            self.edge.get_source_node(),
            self.node_a
        )

    # ---------------------------------------------------------
    # get_target_node()
    # ---------------------------------------------------------

    def test_get_target_node(self):

        self.assertIs(
            self.edge.get_destination_node(),
            self.node_b
        )

    # ---------------------------------------------------------
    # get_other_node()
    # ---------------------------------------------------------

    def test_get_other_node(self):

        test_cases = [
            # (input, expected_output)
            (self.node_a, self.node_b),
            (self.node_b, self.node_a),
            (self.node_c, None),
        ]

        for input_value, expected_output in test_cases:
            with self.subTest(input=input_value):
                self.assertEqual(
                    self.edge.get_other_node(input_value),
                    expected_output
                )

    def test_get_other_node_directed_edge(self):

        # The implementation currently returns the other endpoint
        # regardless of whether the edge is directed.
        edge: Edge = Edge(
            2,
            self.node_a,
            self.node_b,
            directed=True
        )

        test_cases = [
            # (input, expected_output)
            (self.node_a, self.node_b),
            (self.node_b, self.node_a),
            (self.node_c, None),
        ]

        for input_value, expected_output in test_cases:
            with self.subTest(input=input_value):
                self.assertEqual(
                    edge.get_other_node(input_value),
                    expected_output
                )

    # ---------------------------------------------------------
    # is_directed()
    # ---------------------------------------------------------

    def test_is_directed(self):

        test_cases = [
            # (input, expected_output)
            (False, False),
            (True, True),
        ]

        for input_value, expected_output in test_cases:
            with self.subTest(input=input_value):
                edge: Edge = Edge(
                    2,
                    self.node_a,
                    self.node_b,
                    directed=input_value
                )

                self.assertEqual(
                    edge.is_directed(),
                    expected_output
                )

    # ---------------------------------------------------------
    # get_attribute()
    # ---------------------------------------------------------

    def test_get_attribute(self):

        test_cases = [
            # (input, expected_output)
            ("weight", 10),
            ("label", "Friendship"),
            ("active", True),
            ("nonexistent", None),
        ]

        for input_value, expected_output in test_cases:
            with self.subTest(input=input_value):
                self.assertEqual(
                    self.edge.get_attribute(input_value),
                    expected_output
                )

    # ---------------------------------------------------------
    # update_attribute()
    # ---------------------------------------------------------

    def test_update_attribute(self):

        test_cases = [
            # (input, expected_output)
            (("weight", 20), 20),
            (("label", "Colleague"), "Colleague"),
            (("active", False), False),
            (("weight", "35"), 35),
        ]

        for input_value, expected_output in test_cases:
            key, value = input_value

            with self.subTest(input=input_value):
                self.edge.update_attribute(key, value)

                self.assertEqual(
                    self.edge.get_attribute(key),
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
                self.edge.update_attribute(key, value)

                self.assertEqual(
                    self.edge.get_attribute(key),
                    expected_output
                )

    # ---------------------------------------------------------
    # delete_attribute()
    # ---------------------------------------------------------

    def test_delete_attribute(self):

        test_cases = [
            # (input, expected_output)
            ("weight", False),
            ("label", False),
            ("active", False),
        ]

        for input_value, expected_output in test_cases:
            with self.subTest(input=input_value):
                self.edge.delete_attribute(input_value)

                self.assertIsNone(
                    self.edge.get_attribute(input_value)
                )

    def test_delete_nonexistent_attribute(self):

        expected_output = {
            "weight": 10,
            "label": "Friendship",
            "active": True
        }

        self.edge.delete_attribute("nonexistent")

        self.assertEqual(
            self.edge.get_all_attributes(),
            expected_output
        )

    # ---------------------------------------------------------
    # get_all_attributes()
    # ---------------------------------------------------------

    def test_get_all_attributes(self):

        expected_output = {
            "weight": 10,
            "label": "Friendship",
            "active": True
        }

        self.assertEqual(
            self.edge.get_all_attributes(),
            expected_output
        )

    def test_get_all_attributes_returns_copy(self):

        attributes = self.edge.get_all_attributes()

        attributes["weight"] = 999
        attributes["new_attribute"] = "Injected"

        self.assertEqual(
            self.edge.get_attribute("weight"),
            10
        )

        self.assertIsNone(
            self.edge.get_attribute("new_attribute")
        )

    # ---------------------------------------------------------
    # __repr__()
    # ---------------------------------------------------------

    def test_repr(self):

        test_cases = [
            # (input, expected_output)
            (
                Edge(1, self.node_a, self.node_b),
                "Edge(A -- B)"
            ),
            (
                Edge(2, self.node_a, self.node_b, directed=True),
                "Edge(A -> B)"
            ),
            (
                Edge(3, self.node_b, self.node_c),
                "Edge(B -- C)"
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

        edge_a = Edge(1, self.node_a, self.node_b)
        edge_b = Edge(1, self.node_b, self.node_c)
        edge_c = Edge(2, self.node_a, self.node_b)

        test_cases = [
            # (input, expected_output)
            ((edge_a, edge_b), True),
            ((edge_a, edge_c), False),
            ((edge_a, edge_a), True),
            ((edge_a, "1"), False),
            ((edge_a, None), False),
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
            "source-node": "A",
            "destination-node": "B",
            "directed": False,
            "attributes": {
                "weight": 10,
                "label": "Friendship",
                "active": True
            }
        }

        self.assertEqual(
            self.edge.to_dict(),
            expected_output
        )

    def test_to_dict_directed_edge(self):

        edge: Edge = Edge(
            2,
            self.node_a,
            self.node_b,
            directed=True,
            weight=5
        )

        expected_output = {
            "id": "2",
            "source-node": "A",
            "destination-node": "B",
            "directed": True,
            "attributes": {
                "weight": 5
            }
        }

        self.assertEqual(
            edge.to_dict(),
            expected_output
        )

if __name__ == "__main__":
    unittest.main()
