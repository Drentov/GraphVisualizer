export class Node{

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
		this.id = DOM_g_object.id;

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