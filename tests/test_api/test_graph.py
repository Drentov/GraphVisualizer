
"""
Unit tests for the Graph implementation.
Tests interact through the BaseGraph interface.
"""

import unittest

from api.models.graph import Graph
from api.models.node import Node
from api.models.edge import Edge


class TestGraph(unittest.TestCase):

    def setUp(self):

        # Mock nodes
        self.node_a: Node = Node("A", name="Alice")
        self.node_b: Node = Node("B", name="Bob")
        self.node_c: Node = Node("C", name="Charlie")
        self.node_d: Node = Node("D", name="David")

        # Mock graph
        self.graph: Graph = Graph("G1")

        self.graph.add_node(self.node_a)
        self.graph.add_node(self.node_b)
        self.graph.add_node(self.node_c)
        self.graph.add_node(self.node_d)

        # Mock edges
        self.edge_ab: Edge = Edge(
            "AB", self.node_a, self.node_b,
            weight=10
        )

        self.edge_bc: Edge = Edge(
            "BC", self.node_b, self.node_c,
            weight=20
        )

        self.edge_cd: Edge = Edge(
            "CD", self.node_c, self.node_d,
            weight=30
        )

        self.graph.add_edge(self.edge_ab)
        self.graph.add_edge(self.edge_bc)
        self.graph.add_edge(self.edge_cd)

    # ---------------------------------------------------------
    # Construction
    # ---------------------------------------------------------

    def test_initialization(self):

        test_cases = [
            # (input, expected_output)
            (self.graph.graph_id, "G1"),
            (self.graph.get_number_of_nodes(), 4),
            (self.graph.get_number_of_edges(), 3),
        ]

        for input_value, expected_output in test_cases:
            with self.subTest(input=input_value):
                self.assertEqual(input_value, expected_output)

    # ---------------------------------------------------------
    # add_node()
    # ---------------------------------------------------------

    def test_add_node(self):

        test_cases = [
            # (input, expected_output)
            ("E", 5),
            ("F", 6),
        ]

        for input_value, expected_output in test_cases:
            with self.subTest(input=input_value):

                node: Node = Node(input_value)
                self.graph.add_node(node)

                self.assertEqual(
                    self.graph.get_number_of_nodes(),
                    expected_output
                )

                self.assertIs(
                    self.graph.get_node(input_value),
                    node
                )

    def test_add_duplicate_node(self):

        node: Node = Node("A", name="Duplicate")

        with self.assertRaises(ValueError):
            self.graph.add_node(node)

    # ---------------------------------------------------------
    # get_node()
    # ---------------------------------------------------------

    def test_get_node(self):

        test_cases = [
            # (input, expected_output)
            ("A", self.node_a),
            ("B", self.node_b),
            ("C", self.node_c),
            ("D", self.node_d),
            ("nonexistent", None),
        ]

        for input_value, expected_output in test_cases:
            with self.subTest(input=input_value):

                self.assertEqual(
                    self.graph.get_node(input_value),
                    expected_output
                )

    # ---------------------------------------------------------
    # remove_node()
    # ---------------------------------------------------------

    def test_remove_node(self):

        self.graph.remove_node("B")

        test_cases = [
            # (input, expected_output)
            (self.graph.get_node("B"), None),
            (self.graph.get_number_of_nodes(), 3),
            (self.graph.get_number_of_edges(), 1),
            (self.graph.get_edge("AB"), None),
            (self.graph.get_edge("BC"), None),
            (self.graph.get_edge("CD"), self.edge_cd),
        ]

        for input_value, expected_output in test_cases:
            with self.subTest(input=input_value):
                self.assertEqual(input_value, expected_output)

    def test_remove_node_with_multiple_edges(self):

        # Adding one more edge connected to node A.
        edge_ac: Edge = Edge("AC", self.node_a, self.node_c)
        self.graph.add_edge(edge_ac)

        self.graph.remove_node("A")

        test_cases = [
            # (input, expected_output)
            (self.graph.get_number_of_nodes(), 3),
            (self.graph.get_number_of_edges(), 2),
            (self.graph.get_edge("AB"), None),
            (self.graph.get_edge("AC"), None),
            (self.graph.get_edge("BC"), self.edge_bc),
        ]

        for input_value, expected_output in test_cases:
            with self.subTest(input=input_value):
                self.assertEqual(input_value, expected_output)

    def test_remove_node_nonexistent(self):

        with self.assertRaises(ValueError):
            self.graph.remove_node("nonexistent")

    def test_remove_node_with_self_loop(self):

        edge: Edge = Edge("AA", self.node_a, self.node_a)
        self.graph.add_edge(edge)

        self.graph.remove_node("A")

        self.assertIsNone(self.graph.get_node("A"))
        self.assertIsNone(self.graph.get_edge("AA"))

    # ---------------------------------------------------------
    # add_edge()
    # ---------------------------------------------------------

    def test_add_edge(self):

        test_cases = [
            # (input, expected_output)
            ("AC", 4),
            ("AD", 5),
        ]

        for input_value, expected_output in test_cases:
            with self.subTest(input=input_value):

                edge: Edge = Edge(
                    input_value,
                    self.node_a,
                    self.node_d
                )

                self.graph.add_edge(edge)

                self.assertEqual(
                    self.graph.get_number_of_edges(),
                    expected_output
                )

                self.assertIs(
                    self.graph.get_edge(input_value),
                    edge
                )

    def test_add_edge_missing_source_node(self):

        missing_node: Node = Node("X")

        edge: Edge = Edge(
            "AX",
            missing_node,
            self.node_a
        )

        with self.assertRaises(ValueError):
            self.graph.add_edge(edge)

    def test_add_edge_missing_destination_node(self):

        missing_node: Node = Node("X")

        edge: Edge = Edge(
            "AX",
            self.node_a,
            missing_node
        )

        with self.assertRaises(ValueError):
            self.graph.add_edge(edge)

    def test_add_duplicate_edge(self):

        duplicate_edge: Edge = Edge(
            "AB",
            self.node_a,
            self.node_c
        )

        with self.assertRaises(ValueError):
            self.graph.add_edge(duplicate_edge)

    # ---------------------------------------------------------
    # get_edge()
    # ---------------------------------------------------------

    def test_get_edge(self):

        test_cases = [
            # (input, expected_output)
            ("AB", self.edge_ab),
            ("BC", self.edge_bc),
            ("CD", self.edge_cd),
            ("nonexistent", None),
        ]

        for input_value, expected_output in test_cases:
            with self.subTest(input=input_value):

                self.assertEqual(
                    self.graph.get_edge(input_value),
                    expected_output
                )

    # ---------------------------------------------------------
    # remove_edge()
    # ---------------------------------------------------------

    def test_remove_edge(self):

        self.graph.remove_edge("BC")

        test_cases = [
            # (input, expected_output)
            (self.graph.get_edge("BC"), None),
            (self.graph.get_number_of_edges(), 2),
            (self.graph.get_edge("AB"), self.edge_ab),
            (self.graph.get_edge("CD"), self.edge_cd),
        ]

        for input_value, expected_output in test_cases:
            with self.subTest(input=input_value):
                self.assertEqual(input_value, expected_output)

    def test_remove_edge_nonexistent(self):

        # Removing a nonexistent edge should do nothing.
        self.graph.remove_edge("nonexistent")

        self.assertEqual(self.graph.get_number_of_edges(), 3)

    def test_remove_self_loop_edge(self):

        edge: Edge = Edge("AA", self.node_a, self.node_a)
        self.graph.add_edge(edge)

        self.graph.remove_edge("AA")

        self.assertIsNone(self.graph.get_edge("AA"))
        self.assertEqual(self.graph.get_number_of_edges(), 3)

    # ---------------------------------------------------------
    # get_all_nodes()
    # ---------------------------------------------------------

    def test_get_all_nodes(self):

        expected_output = [
            self.node_a,
            self.node_b,
            self.node_c,
            self.node_d
        ]

        self.assertEqual(
            self.graph.get_all_nodes(),
            expected_output
        )

    # ---------------------------------------------------------
    # get_all_edges()
    # ---------------------------------------------------------

    def test_get_all_edges(self):

        expected_output = [
            self.edge_ab,
            self.edge_bc,
            self.edge_cd
        ]

        self.assertEqual(
            self.graph.get_all_edges(),
            expected_output
        )

    # ---------------------------------------------------------
    # get_number_of_nodes()
    # ---------------------------------------------------------

    def test_get_number_of_nodes(self):

        test_cases = [
            # (input, expected_output)
            (4, 4),
        ]

        for input_value, expected_output in test_cases:
            with self.subTest(input=input_value):
                self.assertEqual(
                    self.graph.get_number_of_nodes(),
                    expected_output
                )

        self.graph.add_node(Node("E"))
        self.assertEqual(self.graph.get_number_of_nodes(), 5)

        self.graph.remove_node("A")
        self.assertEqual(self.graph.get_number_of_nodes(), 4)

    # ---------------------------------------------------------
    # get_number_of_edges()
    # ---------------------------------------------------------

    def test_get_number_of_edges(self):

        self.assertEqual(self.graph.get_number_of_edges(), 3)

        self.graph.add_edge(
            Edge("AD", self.node_a, self.node_d)
        )

        self.assertEqual(self.graph.get_number_of_edges(), 4)

        self.graph.remove_edge("AB")

        self.assertEqual(self.graph.get_number_of_edges(), 3)

    # ---------------------------------------------------------
    # has_cycle()
    # ---------------------------------------------------------

    def test_has_cycle(self):

        # Each case constructs a separate graph.
        # (input, expected_output)

        def create_graph(edges):

            graph: Graph = Graph("CycleTest")

            nodes = {
                node_id: Node(node_id)
                for node_id in ("A", "B", "C", "D")
            }

            for node in nodes.values():
                graph.add_node(node)

            for edge_id, source, target, directed in edges:
                graph.add_edge(
                    Edge(
                        edge_id,
                        nodes[source],
                        nodes[target],
                        directed=directed
                    )
                )

            return graph

        test_cases = [
            # Empty graph
            (
                [],
                False
            ),

            # Single isolated nodes
            (
                [],
                False
            ),

            # Directed acyclic chain: A -> B -> C
            (
                [
                    ("AB", "A", "B", True),
                    ("BC", "B", "C", True),
                ],
                False
            ),

            # Directed cycle: A -> B -> C -> A
            (
                [
                    ("AB", "A", "B", True),
                    ("BC", "B", "C", True),
                    ("CA", "C", "A", True),
                ],
                True
            ),

            # Undirected acyclic chain: A -- B -- C
            (
                [
                    ("AB", "A", "B", False),
                    ("BC", "B", "C", False),
                ],
                False
            ),

            # Undirected cycle: A -- B -- C -- A
            (
                [
                    ("AB", "A", "B", False),
                    ("BC", "B", "C", False),
                    ("CA", "C", "A", False),
                ],
                True
            ),

            # Directed self-loop
            (
                [
                    ("AA", "A", "A", True),
                ],
                True
            ),

            # Undirected self-loop
            (
                [
                    ("AA", "A", "A", False),
                ],
                True
            ),

            # Mixed cycle:
            # A -> B -- C -> A
            (
                [
                    ("AB", "A", "B", True),
                    ("BC", "B", "C", False),
                    ("CA", "C", "A", True),
                ],
                True
            ),

            # Mixed but acyclic:
            # A -> B
            # A -> C
            # D -> B
            (
                [
                    ("AB", "A", "B", True),
                    ("AC", "A", "C", True),
                    ("DB", "D", "B", True),
                ],
                False
            ),

            # Directed edges pointing into an already visited node
            # must not be mistaken for a cycle.
            (
                [
                    ("AB", "A", "B", True),
                    ("CB", "C", "B", True),
                ],
                False
            ),
        ]

        for input_value, expected_output in test_cases:
            with self.subTest(input=input_value):

                graph = create_graph(input_value)

                self.assertEqual(
                    graph.has_cycle(),
                    expected_output
                )

    # ---------------------------------------------------------
    # get_subgraph_by_nodes()
    # ---------------------------------------------------------

    def test_get_subgraph_by_nodes(self):

        test_cases = [
            # (input, expected_output)
            (
                {"A", "B"},
                (2, 1)
            ),
            (
                {"A", "B", "C"},
                (3, 2)
            ),
            (
                {"A", "B", "C", "D"},
                (4, 3)
            ),
            (
                {"A"},
                (1, 0)
            ),
            (
                set(),
                (0, 0)
            ),
            (
                {"X", "Y"},
                (0, 0)
            ),
        ]

        for input_value, expected_output in test_cases:
            with self.subTest(input=input_value):

                subgraph: Graph = (
                    self.graph.get_subgraph_by_nodes(input_value)
                )

                self.assertEqual(
                    (
                        subgraph.get_number_of_nodes(),
                        subgraph.get_number_of_edges()
                    ),
                    expected_output
                )

    def test_subgraph_contains_only_selected_nodes(self):

        subgraph = self.graph.get_subgraph_by_nodes({"A", "C", "D"})

        test_cases = [
            # (input, expected_output)
            ("A", True),
            ("B", False),
            ("C", True),
            ("D", True),
        ]

        for input_value, expected_output in test_cases:
            with self.subTest(input=input_value):

                self.assertEqual(
                    subgraph.get_node(input_value) is not None,
                    expected_output
                )

    def test_subgraph_contains_only_internal_edges(self):

        subgraph = self.graph.get_subgraph_by_nodes({"A", "B", "D"})

        test_cases = [
            # (input, expected_output)
            ("AB", True),
            ("BC", False),
            ("CD", False),
        ]

        for input_value, expected_output in test_cases:
            with self.subTest(input=input_value):

                self.assertEqual(
                    subgraph.get_edge(input_value) is not None,
                    expected_output
                )

    def test_subgraph_has_correct_identity(self):

        subgraph = self.graph.get_subgraph_by_nodes({"A", "B"})

        self.assertEqual(
            subgraph.graph_id,
            "G1_subgraph"
        )

    def test_subgraph_is_deep_copy(self):

        subgraph = self.graph.get_subgraph_by_nodes({"A", "B", "C"})

        original_node = self.graph.get_node("A")
        copied_node = subgraph.get_node("A")

        original_edge = self.graph.get_edge("AB")
        copied_edge = subgraph.get_edge("AB")

        # Objects must be different instances.
        self.assertIsNot(original_node, copied_node)
        self.assertIsNot(original_edge, copied_edge)

        # Modify copied node.
        copied_node.set_attribute("name", "Modified")

        # Original must remain unchanged.
        self.assertEqual(
            original_node.get_attribute("name"),
            "Alice"
        )

        # Modify copied edge.
        copied_edge.set_attribute("weight", 999)

        # Original must remain unchanged.
        self.assertEqual(
            original_edge.get_attribute("weight"),
            10
        )

    def test_subgraph_nodes_are_connected_to_copied_nodes(self):

        subgraph = self.graph.get_subgraph_by_nodes({"A", "B", "C"})

        edge = subgraph.get_edge("AB")

        self.assertIs(
            edge.get_source_node(),
            subgraph.get_node("A")
        )

        self.assertIs(
            edge.get_destination_node(),
            subgraph.get_node("B")
        )

        self.assertIsNot(
            edge.get_source_node(),
            self.graph.get_node("A")
        )

    def test_subgraph_preserves_edge_attributes(self):

        subgraph = self.graph.get_subgraph_by_nodes({"A", "B"})

        edge = subgraph.get_edge("AB")

        self.assertEqual(
            edge.get_attribute("weight"),
            10
        )

    def test_subgraph_preserves_edge_direction(self):

        directed_edge: Edge = Edge(
            "DA",
            self.node_d,
            self.node_a,
            directed=True
        )

        self.graph.add_edge(directed_edge)

        subgraph = self.graph.get_subgraph_by_nodes({"D", "A"})

        self.assertTrue(
            subgraph.get_edge("DA").is_directed()
        )

    def test_subgraph_preserves_self_loops(self):

        self_loop: Edge = Edge(
            "AA",
            self.node_a,
            self.node_a
        )

        self.graph.add_edge(self_loop)

        subgraph = self.graph.get_subgraph_by_nodes({"A"})

        self.assertIsNotNone(subgraph.get_edge("AA"))

    # ---------------------------------------------------------
    # __repr__()
    # ---------------------------------------------------------

    def test_repr(self):

        expected_output = (
            "Graph(G1, "
            "nodes=['A', 'B', 'C', 'D'], "
            "edges=['AB', 'BC', 'CD'])"
        )

        self.assertEqual(
            repr(self.graph),
            expected_output
        )

    # ---------------------------------------------------------
    # to_dict()
    # ---------------------------------------------------------

    def test_to_dict(self):

        expected_output = {
            "id": "G1",

            "nodes": [
                {
                    "id": "A",
                    "attributes": {"name": "Alice"}
                },
                {
                    "id": "B",
                    "attributes": {"name": "Bob"}
                },
                {
                    "id": "C",
                    "attributes": {"name": "Charlie"}
                },
                {
                    "id": "D",
                    "attributes": {"name": "David"}
                },
            ],

            "edges": [
                {
                    "id": "AB",
                    "source-node": "A",
                    "destination-node": "B",
                    "directed": False,
                    "attributes": {"weight": 10}
                },
                {
                    "id": "BC",
                    "source-node": "B",
                    "destination-node": "C",
                    "directed": False,
                    "attributes": {"weight": 20}
                },
                {
                    "id": "CD",
                    "source-node": "C",
                    "destination-node": "D",
                    "directed": False,
                    "attributes": {"weight": 30}
                },
            ]
        }

        self.assertEqual(
            self.graph.to_dict(),
            expected_output
        )

if __name__ == "__main__":
    unittest.main()
