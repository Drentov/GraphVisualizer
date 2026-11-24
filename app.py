from flask import Flask, render_template
import mimetypes

from api.models.graph import Graph
from api.models.node import Node
from api.models.edge import Edge
from plugins.simple_visualizer.simple_visualizer import SimpleVisualizer

mimetypes.add_type('text/javascript', '.js') #needed so flask loads JS code correctly

app = Flask(__name__, template_folder="frontend", static_folder="frontend/static")

@app.route('/')
def hello_world():  # put application's code here
    return render_template("index.html")


#NOTE:! /get_simple_html is just a TEMPORARY endpoint, once core is finished, hook up visualizer plugin to it directly!
@app.route("/get_simple_html")
def get_simple_visualizer_html() -> str:

    nodeA = Node("A", name="Jacob_1")
    nodeB = Node("B", name="Jacob_2")
    nodeC = Node("C", name="Jacob_3")

    edge1 = Edge(1, nodeA, nodeB)
    edge2 = Edge(2, nodeB, nodeC)
    edge3 = Edge(3, nodeA, nodeC)

    example_graph = Graph("testgraph1")

    example_graph.add_node(nodeA)
    example_graph.add_node(nodeB)
    example_graph.add_node(nodeC)

    example_graph.add_edge(edge1)
    example_graph.add_edge(edge2)
    example_graph.add_edge(edge3)

    visualizer_plugin = SimpleVisualizer()
    html_graph = visualizer_plugin.to_visual_form(example_graph)

    return html_graph

if __name__ == '__main__':
    app.run()
