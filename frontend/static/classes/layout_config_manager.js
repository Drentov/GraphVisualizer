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
