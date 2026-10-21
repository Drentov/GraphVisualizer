import { GraphZoom } from "./zoom.js";



const burger_button = document.querySelector('.dropdown-toggle');
const burger_menu = document.querySelector('.dropdown-items');

burger_button.addEventListener('click', function(){
	burger_menu.classList.toggle('show');
});

//Section related to Graph stabilisation.


class Node{

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

class Edge{

    /**
    * @param {SVGLineElement} DOM_line_object
    * @param {Node} sourceNode
    * @param {Node} destinationNode
    */

	constructor(DOM_line_object, sourceNode, destinationNode){

		/** @type {SVGLineElement} */
		this.DOM_line_object = DOM_line_object;

		/** @type {Node} */
		this.sourceNode = sourceNode;

		/** @type {Node} */
		this.destinationNode = destinationNode;

		//TODO!!!
		//this.directed = False (NOTE: If undirected, 
		//this.Cyclic = False		it doesnt matter which is the source and which is the destination node!)
	}

	toString(){
		return "LEFT: \n" +
				"---------------------\n" +
				this.sourceNode.toString()  +
				"RIGHT: \n" +
				"---------------------\n" +
				this.destinationNode.toString() +
				"\n";
	}	
}


class Graph{

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

			let DOM_edge = edge.DOM_line_object;

			DOM_edge.setAttribute("x1", edge.sourceNode.x);
			DOM_edge.setAttribute("y1", edge.sourceNode.y);

			DOM_edge.setAttribute("x2", edge.destinationNode.x);
			DOM_edge.setAttribute("y2", edge.destinationNode.y);
		});

	}
}


class LayoutAdjustmentCalculator{

	constructor(){

		//Hypeparameters
		//TODO: hook them up to the UI sliders.

		/** @type {Number} */
	    this.kRepulsion = 100;  // How strongly nodes push each other apart
	    
	    /** @type {Number} */
	    this.kAttraction = 0.20; // How strongly edges pull nodes together
	    
	    /** @type {Number} */
	    this.damping = 0.85;    // Friction (prevents infinite oscillation)
	}


	//Computes a single step/frame of the physics simulation

	/**
	* @param {Graph} graph 
	*/
	createNextState(graph){

	    // 1. Repulsive Forces: Every node pushes every other node away
	    for (let i = 0; i < graph.nodeList.length; i++) {
	      
	      	/** @type {Node} */
	      	let nodeA = graph.nodeList[i];
		      
	      	for (let j = i + 1; j < graph.nodeList.length; j++) {
		        
		        /** @type {Node} */
		        let nodeB = graph.nodeList[j];
		        
		        let dx = nodeB.x - nodeA.x;
		        let dy = nodeB.y - nodeA.y;
		        
		        let distance = Math.sqrt(dx * dx + dy * dy) || 1; // Prevent division by zero

		        // Coulomb-like repulsion force formula
		        let force = (this.kRepulsion * this.kRepulsion) / distance;
		        let fx = (dx / distance) * force;
		        let fy = (dy / distance) * force;

		        // Push away from each other
		        nodeA.x_velocity -= fx;
		        nodeA.y_velocity -= fy;
		        nodeB.x_velocity += fx;
		        nodeB.y_velocity += fy;
			}
		}

	    // 2. Attractive Forces: Connected nodes pull each other together

		const calculator_this = this;

	    graph.edgeList.forEach(function(edge) {
	      	let sourceNode = edge.sourceNode;
		    let destinationNode = edge.destinationNode;

		    let dx = destinationNode.x - sourceNode.x;
		    let dy = destinationNode.y - sourceNode.y;
		    let distance = Math.sqrt(dx * dx + dy * dy) || 1;

		    // Hooke's Law spring force
		    let force = calculator_this.kAttraction * distance;
		    let fx = (dx / distance) * force;
		    let fy = (dy / distance) * force;

		    sourceNode.x_velocity += fx;
		    sourceNode.y_velocity += fy;
		    destinationNode.x_velocity -= fx;
		    destinationNode.y_velocity -= fy;
    	});

	    // 3. Update Positions and Apply Damping and Gravity
        graph.nodeList.forEach(function(node) {
			
			// Small gravitational pull toward center to avoid floating away
			let gravity = 0.01;
			node.x_velocity += (graph.canvasWidth / 2 - node.x) * gravity;
			node.y_velocity += (graph.canvasHeight / 2 - node.y) * gravity;

			// Apply forces to positions
			node.x += node.x_velocity;
			node.y += node.y_velocity;

			// Apply friction/damping
			node.x_velocity *= calculator_this.damping;
			node.y_velocity *= calculator_this.damping;
		});
	}
}


class LayoutConfigManager{
	/**
	* @param {LayoutAdjustmentCalculator} calculator_object
	*/
	constructor(calculator_object){

		/** @type {LayoutAdjustmentCalculator} */
		this.calculator_object = calculator_object;

		/** @type {HTMLInputElement} */
		this.DOM_repulsion = document.getElementById("repulsion");
	    
	    /** @type {HTMLInputElement} */
	    this.DOM_attraction = document.getElementById("attraction");
	    
	    /** @type {HTMLInputElement} */
	    this.DOM_damping = document.getElementById("damping");
	
	    //Registering listeners

	    this.DOM_repulsion.addEventListener("input", () => {
	    	this.calculator_object.kRepulsion = Number(this.DOM_repulsion.value);
	    });

	    this.DOM_attraction.addEventListener("input", () => {
	    	this.calculator_object.kAttraction = Number(this.DOM_attraction.value);
	    });

    	this.DOM_damping.addEventListener("input", () => {
	    	this.calculator_object.damping = Number(this.DOM_damping.value);
	    });
	}
}


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

function test_Edges(){ //OUTDATED!!!

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

	//console.log(graph.toString());

    function animate() {
        graph.tick();
        requestAnimationFrame(animate);
    }

	animate();
}


test_Graph();