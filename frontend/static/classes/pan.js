class PanControls {

    // Class responsible for creating the HTML buttons!

    /**
     * @param {HTMLDivElement} DOM_div_graph
     */
    constructor(DOM_div_graph) {

        this.DOM_div_graph = DOM_div_graph;

        // Create the container.
        this.DOM_div_controls = document.createElement("div");
        this.DOM_div_controls.classList.add("pan-controls");

        /** @type {String[]}	*/
        const button_classes_list = [
        	"pan-up",
        	"pan-left",
        	"pan-down",
        	"pan-right"
        ];

        // Create the buttons.
        this.DOM_button_up = this.#createButton(button_classes_list[0], "↑");
        this.DOM_button_left = this.#createButton(button_classes_list[1], "←");
        this.DOM_button_down = this.#createButton(button_classes_list[2], "↓");
        this.DOM_button_right = this.#createButton(button_classes_list[3], "→");

        // Add the buttons to the container.
        this.DOM_div_controls.append(
            this.DOM_button_up,
            this.DOM_button_left,
            this.DOM_button_down,
            this.DOM_button_right
        );

        // Add the controls to the graph.
        this.DOM_div_graph.appendChild(this.DOM_div_controls);
    
        this.buttonDirectionList = [
	        ["." + button_classes_list[0],  0, 1],
	        ["." + button_classes_list[2],  0, -1],
	        ["." + button_classes_list[1],  1, 0],
	        ["." + button_classes_list[3],  -1, 0]
    	];
    }

    #createButton(className, text) {

        const button = document.createElement("button");

        button.classList.add(className);
        button.type = "button";
        button.textContent = text;

        return button;
    }

    destroy() {
        this.DOM_div_controls.remove();  //Destroys the entire button pane!
    }
}



export class Panner{

    /**
	* @param {HTMLDivElement} graph
    */
    constructor(DOM_div_graph) {

    	/** @type {HTMLDivElement} */ 
    	this.DOM_div_graph = DOM_div_graph;

    	/** @type {SVGSVGElement} */
    	this.canvas = DOM_div_graph.querySelector(".graph-canvas");

        /** @type {SVGGElement} */
        this.content = this.canvas.querySelector(".pan-content");
        
        this.panSpeed = 5; // SVG units per frame

		this.panDirectionX = 0;
		this.panDirectionY = 0;

		this.animationFrame = null;
		this.lastFrameTime = null;

        /** @type {[EventTarget, string, EventListener][]} */
        this.eventListeners = []; //Stored for later removal!


        /** @type {Number} */
        this.offsetX = 0;

        /** @type {Number} */
        this.offsetY = 0;

        /** @type {PanControls} */
        this.PanControls = new PanControls(DOM_div_graph);

        this.#setupEventListeners();
    }

    #setupEventListeners(){

    	for (const [selector, dx, dy] of this.PanControls.buttonDirectionList){

    		const button = this.DOM_div_graph.querySelector(selector);

    		const pointerDown = (event) => {

    			event.preventDefault();

    			this.panDirectionX = dx;
    			this.panDirectionY = dy;

    			button.setPointerCapture(event.pointerId);

    			this.lastFrameTime = null;

    			if (this.animationFrame == null){

    				this.animationFrame = requestAnimationFrame(
    					(time) => this.#panLoop(time)
					);
    			}
    		};

    		const pointerUp = () => this.#stopPanning();
            const pointerCancel = () => this.#stopPanning();
            const lostPointerCapture = () => this.#stopPanning();

            button.addEventListener("pointerdown", pointerDown);
            button.addEventListener("pointerup", pointerUp);
            button.addEventListener("pointercancel", pointerCancel);
            button.addEventListener("lostpointercapture", lostPointerCapture);
    	
            // Store the references for later removal.
            this.eventListeners.push(
                [button, "pointerdown", pointerDown],
                [button, "pointerup", pointerUp],
                [button, "pointercancel", pointerCancel],
                [button, "lostpointercapture", lostPointerCapture]
            );
        }

        const windowBlur = () => this.#stopPanning();
        window.addEventListener("blur", windowBlur);

        // Store the references for later removal.
        this.eventListeners.push(
            [window, "blur", windowBlur]
        );
    }

	#panLoop(time) {

	    if (this.lastFrameTime !== null) {

	        const deltaTime = (time - this.lastFrameTime) / 16.67; //60fps

	        this.pan(
	            this.panDirectionX * this.panSpeed * deltaTime,
	            this.panDirectionY * this.panSpeed * deltaTime
	        );
	    }

	    this.lastFrameTime = time;

	    if (this.panDirectionX !== 0 || this.panDirectionY !== 0) {
	        this.animationFrame = requestAnimationFrame(
	            (time) => this.#panLoop(time)
	        );
	    } else {
	        this.animationFrame = null;
	        this.lastFrameTime = null;
	    }
	}

    #stopPanning() {

	    this.panDirectionX = 0;
	    this.panDirectionY = 0;
	}


    //To move the graph content.
    /**
    * @param {number} dx
    * @param {number} dy
    */
    pan(dx, dy) {

        this.offsetX += dx;
        this.offsetY += dy;

        this.content.setAttribute(
            "transform",
            `translate(${this.offsetX}, ${this.offsetY})`
        );
    }


    destroy() {

        // Stop the animation loop.
        if (this.animationFrame !== null) {
            cancelAnimationFrame(this.animationFrame);
            this.animationFrame = null;
        }

        // Stop any ongoing panning.
        this.#stopPanning();

        // Remove all registered event listeners.
        for (const [element, event, handler] of this.eventListeners) {
            element.removeEventListener(event, handler);
        }

        //Clear the list.
        this.eventListeners = [];

        // Remove the dynamically created controls.
        this.PanControls.destroy();
    }
}