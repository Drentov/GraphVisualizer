import { Graph } from "./graph_subelements/graph.js";
import { Edge } from "./graph_subelements/egde.js";

export class LayoutCurvatureCalculator{

	/**
	* @param {Graph} graph 
	*/
	constructor(graph){

		this.graph = graph;
	}


	createEdgeCurvature(){

		this.graph.forcePairs.forEach(function(forcePair){

			let edgeList = forcePair.associatedEdges;

			//if an even number, one can remain as a straight line!
			let needToSkipFirstOdd = (edgeList.length % 2) === 1; 

			let i = 1

			while (i < edgeList.length) {
				
				if(needToSkipFirstOdd){
					needToSkipFirstOdd = false;
					i++;
				}

				let edge1 = edgeList[i-1];
				let edge2 = edgeList[i];

				edge1.curveOffset = 
					(forcePair.isNotInverted(edge1)) ? i * Edge.curveIncreaseOffsetAmount : -i * Edge.curveIncreaseOffsetAmount;
				
				edge2.curveOffset = 
					(forcePair.isNotInverted(edge2)) ? -i * Edge.curveIncreaseOffsetAmount : i * Edge.curveIncreaseOffsetAmount;
			
				i+=2;
			}
		});
	}
}