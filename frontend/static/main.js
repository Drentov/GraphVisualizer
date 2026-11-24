import {test_Graph, test_Nodes, test_Edges, test_GraphManager} from "./tests/graph_test.js";
import { test_SimpleVisualizer } from "./tests/plugin_test.js";
import { GraphManager } from "./classes/graph_manager.js";

function main(){

	new GraphManager();
}

function testFrontendAll(){

	test_Nodes();
	test_Edges();
	test_Graph();
	test_GraphManager();
}

function testPlugins(){

	test_SimpleVisualizer();
}


main();
//testPlugins();
//testFrontendAll();