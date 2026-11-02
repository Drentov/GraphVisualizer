import math
from typing import Dict, Tuple, List
from api.models.edge import Edge
from api.models.graph import Graph
from api.models.node import Node
from api.plugin_interfaces.visualizer_interface import VisualizerInterface


class SimpleVisualizer(VisualizerInterface):

    def __init__(self, canvas_width=600, canvas_height=400):
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self._center_point = (canvas_width/2, canvas_height/2)

        if canvas_height < canvas_width:
            self._circle_radius = canvas_height / 4  #the radius of the "circle"
        else:                                         #on which all points will be initially drawn!
            self._circle_radius = canvas_width / 4

    def to_visual_form(self, graph: Graph) -> str:

        grap_node_positions_map = self._create_graph_node_positions(graph)  # a map of {Node : (x, y)} so we do not have to recalculate edge positions!
        return self._get_from_template(graph, grap_node_positions_map)


    def _create_graph_node_positions(self, graph: Graph) -> Dict[Node, Tuple[float, float]]:

        #Calculates where to place the nodes on the canvas
        #It will place them on a circle

        graph_node_positions = {}

        all_nodes_list = graph.get_all_nodes()

        if len(all_nodes_list) == 0: return graph_node_positions #to avoid division by 0!

        angle = 2 * math.pi / len(all_nodes_list)

        for i in range(len(all_nodes_list)):
            node = all_nodes_list[i]

            x = round(self._center_point[0] + self._circle_radius * math.cos(i * angle))
            y = round(self._center_point[1] + self._circle_radius * math.sin(i * angle))

            graph_node_positions[node] = (x, y)

        return graph_node_positions

    def _get_from_template(self, graph: Graph, grap_node_positions_map: Dict[Node, Tuple[float, float]]) -> str:

        return  f"""

            <div class="graph" id="{graph.graph_id}" visualizer-type="simple">
            
            <svg class="graph-canvas" viewBox="0 0 {self.canvas_width} {self.canvas_height}">

                <!-- defs: reusable svg defined shapes, in our cas, our arrowhead -->
                <defs>
                    <marker id="arrowhead"
                            markerWidth="22.5"
                            markerHeight="22.5"
                            refX="40"
                            refY="11.25"
                            orient="auto"
                            markerUnits="userSpaceOnUse">
                        <polygon points="0 0, 22.5 11.25, 0 22.5"
                            fill="context-stroke"/>
                    </marker>
                </defs>

                <g class="zoom-content">
                    <g class="pan-content">

                        <!-- Edges -->
                        <!-- NOTE: due to how svg drawing order works, edges must come first in the html declaration -->
                        <g class="edges">
                            {self._get_all_html_edges(graph.get_all_edges(), grap_node_positions_map)}
                        </g>

                        <!-- Nodes -->
                        <g class="nodes">
                            {self._get_all_html_nodes(grap_node_positions_map)}
                        </g>
                    </g>
                </g>
            </svg>
        </div>
    """

    @staticmethod
    def _get_all_html_nodes(grap_node_positions_map: Dict[Node, Tuple[float, float]]) -> str:

        string_to_return = ""

        for key, value in grap_node_positions_map.items():

            node = key
            x, y = value

            string_to_return += SimpleVisualizer._to_html_node(node, x, y)

        return string_to_return


    @staticmethod
    def _to_html_node(node: Node, x:float, y:float) -> str:

        return f"""
                            <g id="{node.node_id}" class="node" transform="translate({x}, {y})">
                                <circle/>
                                <text dy="5">{node.node_id}</text>
                            </g>
            """

    @staticmethod
    def _get_all_html_edges(edges_list:List[Edge], grap_node_positions_map: Dict[Node, Tuple[float, float]]) -> str:

        string_to_return = ""

        for edge in edges_list:
            string_to_return += SimpleVisualizer._to_html_edge(edge, grap_node_positions_map)

        return string_to_return

    @staticmethod
    def _to_html_edge(edge: Edge, grap_node_positions_map: Dict[Node, Tuple[float, float]]) -> str:

        source_coords_x, source_coords_y = grap_node_positions_map[edge.source_node]
        destination_coords_x, destination_coords_y = grap_node_positions_map[edge.destination_node]
        midpoint_coords_x = (source_coords_x + destination_coords_x) / 2
        midpoint_coords_y = (source_coords_y + destination_coords_y) / 2

        if edge.source_node != edge.destination_node:
            path_string = f"M {source_coords_x} {source_coords_y} Q {midpoint_coords_x} {midpoint_coords_y} {destination_coords_x} {destination_coords_y}"
        else: #in case edge starts and ends in the same node!
            path_string = f"M {source_coords_x} {source_coords_y} C {source_coords_x-100} {source_coords_y-100} , {source_coords_x+100} {source_coords_y-100}, {source_coords_x} {source_coords_y}"

        directed_attribute = 'directed="true"' if edge.directed else 'directed="false"'
        weight = edge.get_attribute("weight")
        weight_attribute = "" if weight is None else "\n" + "\t" * 8 + f'weight="{weight}"'

        return f"""   
                            <path id="{edge.edge_id}" class="edge"
                                source-node="{edge.source_node.node_id}"
                                destination-node="{edge.destination_node.node_id}"
                                {directed_attribute}{weight_attribute}
                                d="{path_string}"
                            />
        """

    """"
    NOTE:
    USAGE OF THE HTML path ELEMENT: 
    M 50 100 = start at the left end
    Q quadratic "bezier" curve
    300 0 = put the control point of the bend there
    (BY DEFAULT set it to the line's center point!)
    250 100 = end at the right end
    """