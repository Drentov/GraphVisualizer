import { ForcePair } from "./force_pair.js";
import { Edge } from "./egde.js";
import { Node } from "./node.js";

export class Graph{

	/**
	* @param {HTMLDivElement} DOM_div_graph_object
	*/

	constructor(DOM_div_graph_object){

        /** @type {HTMLDivElement} */
        this.DOM_div_graph_object = DOM_div_graph_object;
		
		/** @type {SVGSVGElement}*/
        this.DOM_svg_canvas = this.DOM_div_graph_object.querySelector(".graph-canvas");

        /** @type {string} */
        this.id = DOM_div_graph_object.id;

        /** @type {Node[]} */
        this.nodeList = this.#getNodeList();

        /** @type {Edge[]} */
        this.edgeList = this.#getEdgeList();

        /** @type {ForcePair[]} */
        this.forcePairs = this.#getForcePairs();

		/** @type {Number} */
		this.canvasWidth = this.DOM_svg_canvas.viewBox.baseVal.width;

		/** @type {Number} */
		this.canvasHeight = this.DOM_svg_canvas.viewBox.baseVal.height;
	}


	#getNodeList(){

		let nodeList = [];
		let DOM_graph_nodes = this.DOM_div_graph_object.querySelectorAll(".node");

		DOM_graph_nodes.forEach(function(DOM_node) {
			let node = new Node(DOM_node);
			nodeList.push(node);
		});

		return nodeList;
	}


	#getEdgeList(){

		let edgeList = [];

		//we create a temporary map. Since All nodes are uniquely identifyable.
		const nodeMap = new Map();

		this.nodeList.forEach(function(node) {
		    nodeMap.set(node.id, node);
		});


		let DOM_graph_edges = this.DOM_div_graph_object.querySelectorAll(".edge");

		DOM_graph_edges.forEach(function(DOM_edge){

			//We get each Edge's Node IDs.
			const sourceNode_id = DOM_edge.getAttribute("source-node");
        	const destinationNode_id = DOM_edge.getAttribute("destination-node");

			let sourceNode = nodeMap.get(sourceNode_id);
			let destinationNode = nodeMap.get(destinationNode_id);

			let edge = new Edge(DOM_edge, sourceNode, destinationNode);
			edgeList.push(edge);
		});

		return edgeList;
	}

	#getForcePairs() {

		/** @type {ForcePair[]} */
		const forcePairList = [];

	   	/** @type {Map<Node, Map<Node, ForcePair>>} */
		const connectionsMap = new Map();

		this.edgeList.forEach(function(edge){

	        const side1 = edge.sourceNode;
    		const side2 = edge.destinationNode;

    		//We try to find an existing pair.
    		//Only queriing one direction is fine, since we added it to both sides
    		//if such a pair was already encountered!
    		let forcePair = connectionsMap.get(side1)?.get(side2);

    		if(!forcePair){

    			//If none found, create one!
    			forcePair = new ForcePair(side1, side2);

    			forcePairList.push(forcePair);

    			//Register the pair in both directions
    			if(!connectionsMap.has(side1)){
    				connectionsMap.set(side1, new Map());
    			}

    			if(!connectionsMap.has(side2)){
    				connectionsMap.set(side2, new Map());
    			}

	            connectionsMap.get(side1).set(side2, forcePair);
            	connectionsMap.get(side2).set(side1, forcePair);
    		}

    		//IMPORTANT! We associate each edge with a forcePair!
    		forcePair.associate(edge);
		});

		return forcePairList;

		/*
		CONCEPTUALLY:
	
		{
			"A" : {"B" : ForcePair1},
			"B" : {"A" : ForcePair1}
		}
		*/
	}


	toString(){
		return "Graph ID: " + this.id + "\n" +
			   "Nodes:\n\n" +
			   this.nodeList.map(node => node.toString()).join("\n") + "\n" +
			   "Edges:\n\n" +
			   this.edgeList.map(edge => edge.toString()).join("\n") + "\n";
	}



	refresh(){

		//Refreshes the visual look of the graph, also updates the edges positions.

		this.nodeList.forEach(function(node){

			let DOM_node = node.DOM_g_object;
			DOM_node.setAttribute("transform", "translate(" + node.x + ", " + node.y + ")");
		});

		this.edgeList.forEach(function(edge){

			let DOM_edge = edge.DOM_path_object;

			const controlTuple = edge.getCurveControlPointCoordinates();

			DOM_edge.setAttribute("d",
   				`M ${edge.sourceNode.x} ${edge.sourceNode.y}
				Q ${controlTuple.x} ${controlTuple.y}
				${edge.destinationNode.x} ${edge.destinationNode.y}`
   			);

   			edge.updateDOMWeightElement();
		});
	}

}