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
    * @param {Node} leftNode
    * @param {Node} rightNode
    */

	constructor(DOM_line_object, leftNode, rightNode){

		/** @type {SVGLineElement} */
		this.DOM_line_object = DOM_line_object;

		/** @type {Node} */
		this.leftNode = leftNode;

		/** @type {Node} */
		this.rightNode = rightNode;

		//TODO!!!
		//this.directed = False (NOTE: Directed from left to right)
		//this.Cyclic = False
	}

	toString(){
		return "LEFT: \n" +
				"---------------------\n" +
				this.leftNode.toString()  +
				"RIGHT: \n" +
				"---------------------\n" +
				this.rightNode.toString() +
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
		
        /** @type {string} */
        this.id = DOM_div_graph_object.id;

        /** @type {Node[]} */
        this.nodeList = this.#getNodeList();

        /** @type {Edge[]} */
        this.edgeList = this.#getEdgeList();

        let DOM_svg_canvas = this.DOM_div_graph_object.querySelector(".graph-canvas");

		/** @type {Number} */
		this.canvasWidth = DOM_svg_canvas.viewBox.baseVal.width;

		/** @type {Number} */
		this.canvasHeight = DOM_svg_canvas.viewBox.baseVal.height;
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
			const leftNode_id = DOM_edge.getAttribute("left-node");
        	const rightNode_id = DOM_edge.getAttribute("right-node");

			let leftNode = nodeMap.get(leftNode_id);
			let rightNode = nodeMap.get(rightNode_id);

			let edge = new Edge(DOM_edge, leftNode, rightNode);
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

			DOM_edge.setAttribute("x1", edge.leftNode.x);
			DOM_edge.setAttribute("y1", edge.leftNode.y);

			DOM_edge.setAttribute("x2", edge.rightNode.x);
			DOM_edge.setAttribute("y2", edge.rightNode.y);
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
	      	let leftNode = edge.leftNode;
		    let rightNode = edge.rightNode;

		    let dx = rightNode.x - leftNode.x;
		    let dy = rightNode.y - leftNode.y;
		    let distance = Math.sqrt(dx * dx + dy * dy) || 1;

		    // Hooke's Law spring force
		    let force = calculator_this.kAttraction * distance;
		    let fx = (dx / distance) * force;
		    let fy = (dy / distance) * force;

		    leftNode.x_velocity += fx;
		    leftNode.y_velocity += fy;
		    rightNode.x_velocity -= fx;
		    rightNode.y_velocity -= fy;
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
		const leftNode_id = DOM_edge.getAttribute("left-node");
    	const rightNode_id = DOM_edge.getAttribute("right-node");

		let leftNode = nodeMap.get(leftNode_id);
		let rightNode = nodeMap.get(rightNode_id);

		let edge = new Edge(DOM_edge, leftNode, rightNode);
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

    function animate() {
        graph.tick();
        requestAnimationFrame(animate);
    }

	animate();
}


test_Graph();