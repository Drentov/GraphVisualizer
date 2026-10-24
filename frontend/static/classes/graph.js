import { GraphZoom } from "./zoom.js";
import { Panner } from "./pan.js";
import { LayoutAdjustmentCalculator} from "./layout_adjustment_calculator.js"
import { LayoutConfigManager } from "./layout_config_manager.js";

export class Node{

	//These make autocomplete function!
    /**
     * @param {SVGGElement} DOM_g_object
     */

	constructor(DOM_g_object){

		/** @type {SVGGElement} */
		this.DOM_g_object = DOM_g_object;
		
		let transform = DOM_g_object.transform.baseVal.getItem(0);

		/** @type {number} */
		this.x = transform.matrix.e;
		
		/** @type {number} */
		this.y = transform.matrix.f;

		/** @type {string}*/
		this.id = DOM_g_object.getAttribute("data-node-id");

		//Parameters needed for force calculation.
        
        /** @type {number} */
        this.x_velocity = 0;

        /** @type {number} */
        this.y_velocity = 0;
	}

	toString(){
		return "id = " + this.id  + ", \n" + 
			   "x = " + this.x  + ", \n" +
			   "y = " + this.y  + ", \n";
	}

}

export class Edge{

    /**
    * @param {SVGPathElement} DOM_path_object
    * @param {Node} sourceNode
    * @param {Node} destinationNode
    */

	constructor(DOM_path_object, sourceNode, destinationNode){

		/** @type {SVGLineElement} */
		this.DOM_path_object = DOM_path_object;

		/** @type {Node} */
		this.sourceNode = sourceNode;

		/** @type {Node} */
		this.destinationNode = destinationNode;

		/** @type {Number} */
		this.curveOffset = 100;

		/** @type {Boolean} */
		this.directed = this.DOM_path_object.getAttribute("directed") === "true";
	}

	/**
 	* @returns {{x: number, y: number}} The "bezier" curve's control point.
 	*/
	getCurveControlCoordinates(){

		const x1 = this.sourceNode.x;
		const y1 = this.sourceNode.y;
		const x2 = this.destinationNode.x;
		const y2 = this.destinationNode.y;

		// Direction of the edge
		const dx = x2 - x1;
		const dy = y2 - y1;

		// Length of the edge
		const length = Math.sqrt(dx * dx + dy * dy);

		// Normalized perpendicular direction
		const perpendicularX = -dy / length;
		const perpendicularY = dx / length;


		// Midpoint, offset perpendicular to the edge
		const controlX = (x1 + x2) / 2
		    + perpendicularX * this.curveOffset;

		const controlY = (y1 + y2) / 2
		    + perpendicularY * this.curveOffset;

	    var controlTuple = {
	    	x: controlX,
	    	y: controlY
	    }

	    return controlTuple;
	}


	toString(){
		return "LEFT: \n" +
				"---------------------\n" +
				this.sourceNode.toString()  +
				"RIGHT: \n" +
				"---------------------\n" +
				this.destinationNode.toString() +
				"\n" +
				"directed: " + this.directed +
				"\n";
	}	
}


export class Graph{

	/**
	* @param {HTMLDivElement} DOM_div_graph_object
	* @param {LayoutAdjustmentCalculator} layout_calculator
	*/

	constructor(DOM_div_graph_object, layout_calculator){

        /** @type {LayoutAdjustmentCalculator} */
        this.layoutCalculator = layout_calculator;

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

		/** @type {Number} */
		this.canvasWidth = this.DOM_svg_canvas.viewBox.baseVal.width;

		/** @type {Number} */
		this.canvasHeight = this.DOM_svg_canvas.viewBox.baseVal.height;

		this.#createSubcomponents();
	}

	#createSubcomponents(){
		new GraphZoom(this.DOM_svg_canvas); //Makes zooming work!
		new LayoutConfigManager(this.layoutCalculator); //Makes the sliders work!
		new Panner(this.DOM_div_graph_object);
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

	toString(){
		return "Graph ID: " + this.id + "\n" +
			   "Nodes:\n\n" +
			   this.nodeList.map(node => node.toString()).join("\n") + "\n" +
			   "Edges:\n\n" +
			   this.edgeList.map(edge => edge.toString()).join("\n") + "\n";
	}

	//This function updates the graph in every interval.
	tick(){
		
		//This sets all of the NODE's DATA to the next frame's position
		this.layoutCalculator.createNextState(this);

		//What is left is actually displaying said change, and also, updating the edges.

		this.nodeList.forEach(function(node){

			let DOM_node = node.DOM_g_object;
			DOM_node.setAttribute("transform", "translate(" + node.x + ", " + node.y + ")");
		});

		this.edgeList.forEach(function(edge){

			let DOM_edge = edge.DOM_path_object;

			const controlTuple = edge.getCurveControlCoordinates();

			DOM_edge.setAttribute("d",
   				`M ${edge.sourceNode.x} ${edge.sourceNode.y}
				Q ${controlTuple.x} ${controlTuple.y}
				${edge.destinationNode.x} ${edge.destinationNode.y}`
   			);
		});
	}
}