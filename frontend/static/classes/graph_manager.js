import { GraphZoom } from "./zoom.js";
import { Panner } from "./pan.js";
import { LayoutAdjustmentCalculator} from "./layout_adjustment_calculator.js"
import { LayoutConfigManager } from "./layout_config_manager.js";
import {Graph} from "./graph_subelements/graph.js";
import { LayoutCurvatureCalculator } from "./layout_curvature_calculator.js";

export class GraphManager{

	static instance = null; //There can only be ONE graph manager active, otherwise memory leak!

	constructor(){

        // Destroy the previous instance, if one exists.
        if (GraphManager.instance !== null) {
            GraphManager.instance.destroy();
        }

        // Register this instance as the current one. (Singleton pattern)
        GraphManager.instance = this;

		let DOM_div_graph_object = document.querySelector(".graph");

		/** @type {Graph} */
		this.graph = new Graph(DOM_div_graph_object);

		/** @type {LayoutAdjustmentCalculator} */
		this.layoutCalculator = new LayoutAdjustmentCalculator(this.graph); //Calculates, how the graph can look balanced!

		/** @type {LayoutCurvatureCalculator}*/
		this.curvatureCalculator = new LayoutCurvatureCalculator(this.graph); //Calculates, how the edges should curve!

		this.#onGraphUpdate();

		this.#createGraphSubcomponents();

		this.#animate_graph();
	}

	#createGraphSubcomponents(){

		/** @type {GraphZoom}*/
		this.graphZoom = new GraphZoom(this.graph.DOM_svg_canvas); //Makes zooming work!
		
		/** @type {LayoutConfigManager}*/
		this.layoutConfigManager = new LayoutConfigManager(this.layoutCalculator); //Makes the sliders work!
		
		/** @type {Panner} */
		this.panner = new Panner(this.graph.DOM_div_graph_object); //Makes panning work!
	}

	#onGraphUpdate(){
		this.curvatureCalculator.createEdgeCurvature();
	}


	//This function updates the graph in every interval.
	tick(){
		
		this.layoutCalculator.createNextState(); //This sets all of the NODE's DATA to the next frame's position
		this.graph.refresh();
	}

	//Handles actually calling the animation frames
	#animate_graph(){
	    
		let graph_manager_this = this;

	    function animate() {
	        graph_manager_this.tick();
	        requestAnimationFrame(animate);
	    }

		animate();
	}

    destroy() {

    	//Stop animating
        if (this.animationFrameId !== null) {
            cancelAnimationFrame(this.animationFrameId);
            this.animationFrameId = null;
        }

        // Other component cleanup.
        this.graphZoom.destroy();
        this.layoutConfigManager.destroy();
        this.panner.destroy();

        //Reset to null
        if (GraphManager.instance === this) {
        	GraphManager.instance = null;
    	}
    }
}