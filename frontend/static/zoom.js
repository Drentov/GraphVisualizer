export class GraphZoom {

    /**
    * @param {SVGSVGElement} svg
    */

	constructor(svg){

		/** @type {SVGSVGElement}*/
		this.svg = svg;

		/** @type {SVGSVGElement} */
		this.content = svg.querySelector(".graph-content");



		/** @type {Number}*/
		this.scale = 1;

		/** @type {Number}*/
		this.translateX = 0;

		/** @type {Number}*/
		this.translateY = 0;



		/** @type {Number}*/
        this.minScale = 0.25;
        
        /** @type {Number}*/
        this.maxScale = 4;

        /** @type {Number}*/
        this.zoomFactor = 1.1;


	
		//Zooming is controlled by the mouse wheel
		this.svg.addEventListener("wheel", (event) =>{
			this.handleWheel(event);
		}, {passive: false});
	}

    /**
    * @param {WheelEvent} event
    */
	handleWheel(event){

		// Do not scroll the page when the pointer is over the canvas.
		event.preventDefault();

		// Convert the mouse position to SVG coordinates.
		const point = this.svg.createSVGPoint();
		point.x = event.clientX;
		point.y = event.clientY;

		const mouse = point.matrixTransform(
			this.svg.getScreenCTM().inverse()
		);

		// Scroll up = zoom in. Scroll down = zoom out.
		const factor = 
			event.deltaY < 0 ? this.zoomFactor : 1 / this.zoomFactor
        
        const newScale = Math.max(
            this.minScale,
            Math.min(this.maxScale, this.scale * factor)
        );

        // Calculate the actual factor after applying zoom limits.
        const actualFactor = newScale / this.scale;

		
        // Keep the graph point under the mouse stationary.
        this.translateX = mouse.x - (mouse.x - this.translateX) * actualFactor;
        this.translateY = mouse.y - (mouse.y - this.translateY) * actualFactor;
        this.scale = newScale;

        this.updateTransform();
	}

    updateTransform() {

        this.content.setAttribute(
            "transform",
            `translate(${this.translateX} ${this.translateY}) scale(${this.scale})`
        );
    }	
}