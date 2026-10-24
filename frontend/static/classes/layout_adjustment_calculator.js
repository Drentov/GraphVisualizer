//Calculates the forces that order the graph into a nice shape

export class LayoutAdjustmentCalculator{

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