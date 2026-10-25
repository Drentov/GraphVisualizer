import { GraphZoom } from "./zoom.js";
import { Panner } from "./pan.js";
import { LayoutAdjustmentCalculator} from "./layout_adjustment_calculator.js"
import { LayoutConfigManager } from "./layout_config_manager.js";
import {Graph} from "./graph.js";
import { LayoutCurvatureCalculator } from "./layout_curvature_calculator.js";

export class GraphManger{

	/**
	* @param {HTMLDivElement} DOM_div_graph_object
	*/

	constructor(DOM_div_graph_object){

		/** @type {Graph} */
		this.graph = new Graph(DOM_div_graph_object);

		/** @type {LayoutAdjustmentCalculator} */
		this.layoutCalculator = new LayoutAdjustmentCalculator(this.graph); //Calculates, how the graph can look balanced!

		/** @type {LayoutCurvatureCalculator}*/
		this.curvatureCalculator = new LayoutCurvatureCalculator(this.graph); //Calculates, how the edges should curve!

		this.#onGraphUpdate();

		this.#createGraphSubcomponents();
	}

	#createGraphSubcomponents(){
		new GraphZoom(this.graph.DOM_svg_canvas); //Makes zooming work!
		new LayoutConfigManager(this.layoutCalculator); //Makes the sliders work!
		new Panner(this.graph.DOM_div_graph_object); //Makes panning work!
	}

	#onGraphUpdate(){
		this.curvatureCalculator.createEdgeCurvature();
	}


	//This function updates the graph in every interval.
	tick(){
		
		this.layoutCalculator.createNextState(); //This sets all of the NODE's DATA to the next frame's position

		this.graph.refresh();
	}
}