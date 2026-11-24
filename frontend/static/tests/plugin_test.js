import { GraphManager } from "../classes/graph_manager.js";

function test_SimpleVisualizer(){

    fetch("/get_simple_html")
        .then(response => response.text())
        .then(html => {
            //console.log(html)
            document.querySelector("main").innerHTML = html;
            new GraphManager();
        }
    );
}

export {test_SimpleVisualizer};