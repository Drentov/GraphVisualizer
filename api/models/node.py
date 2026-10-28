"""
    Node model - representation of a node in the graph
"""
from typing import Any, Dict

from api.type_manager import TypeManager

class Node:

    def __init__(self, node_id: Any, **attributes):

        #PARAMETERS
        #id: Unique identification of a node
        #additional_attributes: any additional node attributes given as key-value pairs

        self.node_id = str(node_id) #internally id will be stored as a string, for convenience
        self.attributes: Dict[str, Any] = {}

        for key, value in attributes.items():

            data_type = TypeManager.detect_type(value)
            value_with_type = TypeManager.validate_and_convert(value, data_type)
            attributes[key] = value_with_type

