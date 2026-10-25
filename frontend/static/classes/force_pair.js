//The purpose of this class is to help calculate
//the attraction force that will keep the graph in shape!
//Sicne there can be duplicates, we must not
//actually count every edge for attraction, rather, 
//we calculate the attraction force on every forcePair

export class ForcePair{

	/**
	* @param {Node} sideA;
	* @param {Node} sideB;
	*/

	constructor(sideA, sideB){

		/** @type {Node} */
		this.sideA = sideA;

		/** @type {Node} */
		this.sideB = sideB;

		/** @type {Edge[]} */
		this.associatedEdges = []; //All edges between the same 2 Nodes
	}

	/**
	* @param {Edge} edge
	*/
	associate(edge){
		this.associatedEdges.push(edge);
	}

	/**
	* @param {Edge} edge
	*/
	isNotInverted(edge){
		return (this.sideA === edge.sourceNode) && (this.sideB === edge.destinationNode);
	}
}