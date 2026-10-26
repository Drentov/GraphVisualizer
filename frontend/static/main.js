import {test_Graph, test_Nodes, test_Edges, test_GraphManager} from "./tests/graph_test.js";
import { GraphManger } from "./classes/graph_manager.js";

function main(){

	let DOM_graph = document.querySelector(".graph");
	let graph_manager = new GraphManger(DOM_graph);

    function animate() {
        graph_manager.tick();
        requestAnimationFrame(animate);
    }

	animate();
}

function testAll(){

	test_Nodes();
	test_Edges();
	test_Graph();
	test_GraphManager();
}

main();
//testAll();