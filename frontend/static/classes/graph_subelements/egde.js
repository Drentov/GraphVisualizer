import { Node } from "./node.js";

export class Edge{

	/** @type {Number} */
	static curveIncreaseOffsetAmount = 80;

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

		/** @type {String} */
		this.id = DOM_path_object.id;

		/** @type {Number} */
		this.curveOffset = 0;

		/** @type {number | null} */ //Optional weight parameter
		this.weight = DOM_path_object.hasAttribute("weight")
		    ? Number(DOM_path_object.getAttribute("weight"))
		    : null;

		this.DOM_edge_weight_text = this.#createDOMWeightElement();

		/** @type {Boolean} */
		this.directed = this.DOM_path_object.getAttribute("directed") === "true";
	}

	#createDOMWeightElement() {

	    if (this.weight === null || Number.isNaN(this.weight)) {
	        return null;
	    }

	    const label = document.createElementNS(
	        "http://www.w3.org/2000/svg",
	        "text"
	    );

	    label.classList.add("edge-weight");
	    label.textContent = this.weight;

	    let midpoint = this.#findBezierCurvedLineMidpoint();

	    label.setAttribute("x", midpoint.x);
	    label.setAttribute("y", midpoint.y);

	    this.DOM_path_object.parentElement.append(label); //Adding it to the DOM!

	    return label;
	}

	updateDOMWeightElement(){

		if(this.DOM_edge_weight_text === null){
			//Check in case weight was set to a valid number, then generate a text field for it!
			this.DOM_edge_weight_text = this.#createDOMWeightElement();
			if(this.DOM_edge_weight_text === null) return; 
		}


		//If text element already exists, update it's position!

		const midpoint = this.#findBezierCurvedLineMidpoint();
	    this.DOM_edge_weight_text.setAttribute("x", midpoint.x);
	    this.DOM_edge_weight_text.setAttribute("y", midpoint.y);
	}

	/**
 	* @returns {{x: number, y: number}} the curved line's midpoint!
 	*/
	#findBezierCurvedLineMidpoint(){

	    const point1 = {
	        x: this.sourceNode.x,
	        y: this.sourceNode.y
	    };

	    const point2 = {
	        x: this.destinationNode.x,
	        y: this.destinationNode.y
	    };

	    const controlPoints = this.getCurveControlPointCoordinates();

	    //One control point case
	    if(controlPoints.length === 1){

	        const controlPoint = controlPoints[0];

	        return {
	            x: point1.x * 0.25 + controlPoint.x * 0.5 + point2.x * 0.25,
	            y: point1.y * 0.25 + controlPoint.y * 0.5 + point2.y * 0.25
	        };
	    }

	    //Two control points case
	    const firstControlPoint = controlPoints[0];
	    const secondControlPoint = controlPoints[1];

	    return {
	        x: point1.x * 0.125
	            + firstControlPoint.x * 0.375
	            + secondControlPoint.x * 0.375
	            + point2.x * 0.125,

	        y: point1.y * 0.125
	            + firstControlPoint.y * 0.375
	            + secondControlPoint.y * 0.375
	            + point2.y * 0.125
	    };
	}

	/**
 	* @returns {[{x: number, y: number}] | [{x: number, y: number}, {x: number, y: number}]}
 	* The "bezier" curve's control point.
 	* There can be one or two of them!
 	*/
	getCurveControlPointCoordinates(){

		const x1 = this.sourceNode.x;
		const y1 = this.sourceNode.y;
		const x2 = this.destinationNode.x;
		const y2 = this.destinationNode.y;


		//Special case, when there is a self loop:
		if(this.sourceNode == this.destinationNode){

			const offset = this.curveOffset / 2;

			const firstControlTuple = {
			    x: this.sourceNode.x - 100 - offset,
			    y: this.sourceNode.y - 100 - offset
			};

			const secondControlTuple = {
			    x: this.sourceNode.x + 100 + offset,
			    y: this.sourceNode.y - 100 - offset
			};

			return [firstControlTuple, secondControlTuple];
		}


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

	    let controlTuple = {
	    	x: controlX,
	    	y: controlY
	    }

	    return [controlTuple];
	}


	toString(){
		return "LEFT: \n" +
				"---------------------\n" +
				this.sourceNode.toString()  +
				"RIGHT: \n" +
				"---------------------\n" +
				this.destinationNode.toString() +
				"\n" +
				"edge ID: " + this.id + "\n" +
				"weight: " + this.weight + "\n" + 
				"directed: " + this.directed + "\n" +
				"\n";
	}	
}