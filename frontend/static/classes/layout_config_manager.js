import { LayoutAdjustmentCalculator } from "./layout_adjustment_calculator.js";

//Hooks the calculator_object's properties up with the UI sliders

export class LayoutConfigManager{
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

        this.handleRepulsion = this.handleRepulsion.bind(this);
        this.handleAttraction = this.handleAttraction.bind(this);
        this.handleDamping = this.handleDamping.bind(this);

        this.DOM_repulsion.addEventListener("input", this.handleRepulsion);
        this.DOM_attraction.addEventListener("input", this.handleAttraction);
        this.DOM_damping.addEventListener("input", this.handleDamping);
	}

	//All of these are used as callbacks with 'this' explicitly bound,
	//so as to not cause confusion!
    handleRepulsion() {
        this.calculator_object.kRepulsion = Number(this.DOM_repulsion.value);
    }

    handleAttraction() {
        this.calculator_object.kAttraction = Number(this.DOM_attraction.value);
    }

    handleDamping() {
        this.calculator_object.damping = Number(this.DOM_damping.value);
    }

    destroy() {
        this.DOM_repulsion.removeEventListener("input", this.handleRepulsion);
        this.DOM_attraction.removeEventListener("input", this.handleAttraction);
        this.DOM_damping.removeEventListener("input", this.handleDamping);
    }
}
