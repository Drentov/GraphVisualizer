import {LayoutAdjustmentCalculator} from "../classes/layout_adjustment_calculator.js"
import { Node } from "../classes/graph_subelements/node.js";
import { Edge } from "../classes/graph_subelements/egde.js";
import { Graph } from "../classes/graph_subelements/graph.js";

function test_Nodes(){

	/** @type {Node[]} */
	let nodes = [];

	let DOM_nodes = document.querySelectorAll(".node");

	DOM_nodes.forEach(function(DOM_node) {
		let node = new Node(DOM_node);
		nodes.push(node);
	});

	nodes.forEach(function(node){
		console.log(node.toString())
	});

}

function test_Edges(){

	//We first load the Nodes.
	/** @type {Node[]} */
	let nodes = [];

	let DOM_nodes = document.querySelectorAll(".node");

	DOM_nodes.forEach(function(DOM_node) {
		let node = new Node(DOM_node);
		nodes.push(node);
	});


	//Then we create a temporary map. All nodes are uniquely identifyable.
	const nodeMap = new Map();

	nodes.forEach(function(node) {
	    nodeMap.set(node.id, node);
	});


	//We load the DOM of the edges.
	/** @type {Edge[]} */
	let edges = [];

	let DOM_edges = document.querySelectorAll(".edge");

	DOM_edges.forEach(function(DOM_edge){

		//We get each Edge's Node IDs.
		const sourceNode_id = DOM_edge.getAttribute("source-node");
    	const destinationNode_id = DOM_edge.getAttribute("destination-node");

		let sourceNode = nodeMap.get(sourceNode_id);
		let destinationNode = nodeMap.get(destinationNode_id);

		let edge = new Edge(DOM_edge, sourceNode, destinationNode);
		edges.push(edge);
	});

	edges.forEach(function(edge){
		console.log(edge.toString());
	});
}


function test_Graph(){

	let layout_calculator = new LayoutAdjustmentCalculator();
	let DOM_graph = document.querySelector(".graph");
	let graph = new Graph(DOM_graph, layout_calculator);

	console.log(graph.toString());
}


function test_GraphManager(){


	let DOM_graph = document.querySelector(".graph");
	let graph_manager = new GraphManger(DOM_graph);

    function animate() {
        graph_manager.tick();
        requestAnimationFrame(animate);
    }

	animate();
}

export {test_GraphManager, test_Graph, test_Nodes, test_Edges};