import {test_Graph, test_Nodes, test_Edges} from "./tests/graph_test.js";
import {LayoutAdjustmentCalculator} from "./classes/layout_adjustment_calculator.js"
import {Graph} from "./classes/graph.js";

function main(){

	let layout_calculator = new LayoutAdjustmentCalculator();
	let DOM_graph = document.querySelector(".graph");
	let graph = new Graph(DOM_graph, layout_calculator);

    function animate() {
        graph.tick();
        requestAnimationFrame(animate);
    }

	animate();
}

function testAll(){

	test_Edges();
	test_Nodes();
	test_Graph();
}

main();
//testAll();