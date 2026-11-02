import unittest
from api.models.edge import Edge
from api.models.graph import Graph
from api.models.node import Node
from plugins.simple_visualizer.simple_visualizer import SimpleVisualizer


class TestSimpleGraphVisualizer(unittest.TestCase):

    def setUp(self):

        self.simple_visualizer = SimpleVisualizer()

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
            directed=True,
            weight=10
        )

        self.edge_bc: Edge = Edge(
            "BC", self.node_b, self.node_c,
            weight=20
        )

        self.edge_cd: Edge = Edge(
            "CD", self.node_c, self.node_d,
            directed=True
        )

        self.graph.add_edge(self.edge_ab)
        self.graph.add_edge(self.edge_bc)
        self.graph.add_edge(self.edge_cd)

    # ---------------------------------------------------------
    # Initialization tests
    # ---------------------------------------------------------

    def test_default_initialization(self):

        visualizer = SimpleVisualizer()

        self.assertEqual(visualizer.canvas_width, 600)
        self.assertEqual(visualizer.canvas_height, 400)
        self.assertEqual(visualizer._center_point, (300, 200))
        self.assertEqual(visualizer._circle_radius, 100)

    def test_custom_canvas_initialization(self):

        visualizer = SimpleVisualizer(800, 600)

        self.assertEqual(visualizer.canvas_width, 800)
        self.assertEqual(visualizer.canvas_height, 600)
        self.assertEqual(visualizer._center_point, (400, 300))
        self.assertEqual(visualizer._circle_radius, 150)

    def test_circle_radius_uses_canvas_width_when_width_is_smaller(self):

        visualizer = SimpleVisualizer(400, 800)

        self.assertEqual(visualizer._circle_radius, 100)

    def test_circle_radius_uses_canvas_height_when_height_is_smaller(self):

        visualizer = SimpleVisualizer(800, 400)

        self.assertEqual(visualizer._circle_radius, 100)

    def test_circle_radius_when_canvas_is_square(self):

        visualizer = SimpleVisualizer(400, 400)

        self.assertEqual(visualizer._circle_radius, 100)

    # ---------------------------------------------------------
    # Node positioning tests
    # ---------------------------------------------------------

    def test_empty_graph_returns_empty_positions(self):

        graph = Graph("Empty")

        positions = self.simple_visualizer._create_graph_node_positions(graph)

        self.assertEqual(positions, {})

    def test_single_node_is_placed_at_right_of_center(self):

        graph = Graph("Single")
        node = Node("A")

        graph.add_node(node)

        positions = self.simple_visualizer._create_graph_node_positions(graph)

        self.assertEqual(len(positions), 1)
        self.assertEqual(positions[node], (400, 200))

    def test_two_nodes_are_placed_on_opposite_sides(self):

        graph = Graph("Two")
        node_a = Node("A")
        node_b = Node("B")

        graph.add_node(node_a)
        graph.add_node(node_b)

        positions = self.simple_visualizer._create_graph_node_positions(graph)

        self.assertEqual(positions[node_a], (400, 200))
        self.assertEqual(positions[node_b], (200, 200))

    def test_four_nodes_are_placed_on_circle(self):

        positions = self.simple_visualizer._create_graph_node_positions(self.graph)

        self.assertEqual(positions[self.node_a], (400, 200))
        self.assertEqual(positions[self.node_b], (300, 300))
        self.assertEqual(positions[self.node_c], (200, 200))
        self.assertEqual(positions[self.node_d], (300, 100))

    def test_node_positions_are_centered_on_custom_canvas(self):

        visualizer = SimpleVisualizer(800, 600)

        graph = Graph("Custom")
        node = Node("A")
        graph.add_node(node)

        positions = visualizer._create_graph_node_positions(graph)

        self.assertEqual(positions[node], (550, 300))

    def test_node_positions_are_rounded_to_integers(self):

        graph = Graph("Three")

        nodes = [
            Node("A"),
            Node("B"),
            Node("C")
        ]

        for node in nodes:
            graph.add_node(node)

        positions = self.simple_visualizer._create_graph_node_positions(graph)

        for x, y in positions.values():
            self.assertIsInstance(x, int)
            self.assertIsInstance(y, int)

    # ---------------------------------------------------------
    # HTML node generation tests
    # ---------------------------------------------------------

    def test_to_html_node(self):

        html = SimpleVisualizer._to_html_node(self.node_a, 150, 100)

        self.assertIn('id="A"', html)
        self.assertIn('class="node"', html)
        self.assertIn('transform="translate(150, 100)"', html)
        self.assertIn("<circle/>", html)
        self.assertIn("<text dy=\"5\">A</text>", html)

    def test_get_all_html_nodes(self):

        positions = {
            self.node_a: (100, 100),
            self.node_b: (200, 200)
        }

        html = SimpleVisualizer._get_all_html_nodes(positions)

        self.assertIn('id="A"', html)
        self.assertIn('id="B"', html)
        self.assertIn('translate(100, 100)', html)
        self.assertIn('translate(200, 200)', html)

    def test_get_all_html_nodes_with_empty_map(self):

        html = SimpleVisualizer._get_all_html_nodes({})

        self.assertEqual(html, "")

    # ---------------------------------------------------------
    # HTML edge generation tests
    # ---------------------------------------------------------

    def test_to_html_edge_directed_with_weight(self):

        positions = {
            self.node_a: (100, 100),
            self.node_b: (300, 100)
        }

        edge = Edge(
            "AB",
            self.node_a,
            self.node_b,
            directed=True,
            weight=10
        )

        html = SimpleVisualizer._to_html_edge(edge, positions)

        self.assertIn('id="AB"', html)
        self.assertIn('class="edge"', html)
        self.assertIn('source-node="A"', html)
        self.assertIn('destination-node="B"', html)
        self.assertIn('directed="true"', html)
        self.assertIn('weight="10"', html)
        self.assertIn('d="M 100 100 Q 200.0 100.0 300 100"', html)

    def test_to_html_edge_undirected_without_weight(self):

        positions = {
            self.node_a: (100, 100),
            self.node_b: (300, 100)
        }

        edge = Edge(
            "AB",
            self.node_a,
            self.node_b
        )

        html = SimpleVisualizer._to_html_edge(edge, positions)

        self.assertIn('directed="false"', html)
        self.assertNotIn('weight=', html)

    def test_to_html_edge_with_zero_weight(self):

        positions = {
            self.node_a: (100, 100),
            self.node_b: (300, 100)
        }

        edge = Edge(
            "AB",
            self.node_a,
            self.node_b,
            weight=0
        )

        html = SimpleVisualizer._to_html_edge(edge, positions)

        self.assertIn('weight="0"', html)

    def test_to_html_edge_self_loop(self):

        positions = {
            self.node_a: (200, 200)
        }

        edge = Edge(
            "AA",
            self.node_a,
            self.node_a
        )

        html = SimpleVisualizer._to_html_edge(edge, positions)

        self.assertIn('id="AA"', html)
        self.assertIn('source-node="A"', html)
        self.assertIn('destination-node="A"', html)
        self.assertIn(
            'd="M 200 200 C 100 100 , 300 100, 200 200"',
            html
        )

    def test_get_all_html_edges(self):

        positions = {
            self.node_a: (100, 100),
            self.node_b: (300, 100),
            self.node_c: (300, 300)
        }

        edges = [
            self.edge_ab,
            self.edge_bc
        ]

        html = SimpleVisualizer._get_all_html_edges(edges, positions)

        self.assertIn('id="AB"', html)
        self.assertIn('id="BC"', html)

    def test_get_all_html_edges_with_empty_list(self):

        html = SimpleVisualizer._get_all_html_edges([], {})

        self.assertEqual(html, "")

    # ---------------------------------------------------------
    # Complete visualization tests
    # ---------------------------------------------------------

    def test_to_visual_form_contains_graph_id(self):

        html = self.simple_visualizer.to_visual_form(self.graph)

        self.assertIn('id="G1"', html)

    def test_to_visual_form_contains_visualizer_type(self):

        html = self.simple_visualizer.to_visual_form(self.graph)

        self.assertIn('visualizer-type="simple"', html)

    def test_to_visual_form_contains_svg_canvas(self):

        html = self.simple_visualizer.to_visual_form(self.graph)

        self.assertIn('class="graph-canvas"', html)
        self.assertIn('viewBox="0 0 600 400"', html)

    def test_to_visual_form_contains_all_nodes(self):

        html = self.simple_visualizer.to_visual_form(self.graph)

        for node_id in ["A", "B", "C", "D"]:
            self.assertIn(f'id="{node_id}"', html)

    def test_to_visual_form_contains_all_edges(self):

        html = self.simple_visualizer.to_visual_form(self.graph)

        for edge_id in ["AB", "BC", "CD"]:
            self.assertIn(f'id="{edge_id}"', html)

    def test_to_visual_form_contains_arrowhead_definition(self):

        html = self.simple_visualizer.to_visual_form(self.graph)

        self.assertIn('<marker id="arrowhead"', html)
        self.assertIn('markerUnits="userSpaceOnUse"', html)
        self.assertIn('fill="context-stroke"', html)

    def test_to_visual_form_contains_edge_attributes(self):

        html = self.simple_visualizer.to_visual_form(self.graph)

        self.assertIn('directed="true"', html)
        self.assertIn('directed="false"', html)
        self.assertIn('weight="10"', html)
        self.assertIn('weight="20"', html)

    def test_to_visual_form_empty_graph(self):

        graph = Graph("Empty")

        html = self.simple_visualizer.to_visual_form(graph)

        self.assertIn('id="Empty"', html)
        self.assertIn('class="graph-canvas"', html)
        self.assertIn('class="edges"', html)
        self.assertIn('class="nodes"', html)

    def test_to_visual_form_custom_canvas_dimensions(self):

        visualizer = SimpleVisualizer(800, 600)

        html = visualizer.to_visual_form(self.graph)

        self.assertIn('viewBox="0 0 800 600"', html)

    #This actually generates a html example document!
    def test_to_visual_form(self):

        html = self.simple_visualizer.to_visual_form(self.graph)

        complete_html = f"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Simple Visualizer Test</title>
    </head>
    <body>
        {html}
    </body>
    </html>
    """

        with open("test_output.html", "w", encoding="utf-8") as file:
            file.write(complete_html)

        print("HTML written to test_output.html")

if __name__ == "__main__":
    unittest.main()
