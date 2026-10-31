"""
    Node model - representation of a node in the graph
"""
from copy import deepcopy
from typing import Any, Dict, Optional
from ...type_manager import TypeManager, SupportedValue, SupportedValueOrDict, SupportedType


class Node:

    def __init__(self, node_id: Any, **attributes):

        #PARAMETERS
        #id: Unique identification of a node
        #additional_attributes: any additional node attributes given as key-value pairs

        self.node_id = str(node_id) #internally id will be stored as a string, for convenience
        self.attributes: Dict[str, SupportedValue] = {}

        for key, value in attributes.items():
            data_type = TypeManager.detect_type(value)
            value_with_type = TypeManager.validate_and_convert(value, data_type)
            self.attributes[key] = value_with_type


    def set_attribute(self, key: str, value: SupportedValue) -> None:
        """
        Set node attribute with type detection.
        """
        #This satisfies the requirement that data is not stored only as string
        detected_type = TypeManager.detect_type(value)
        converted_value = TypeManager.validate_and_convert(value, detected_type)

        self.attributes[key] = converted_value

    def get_attribute(self, key: str) -> Optional[SupportedValue]:
        return self.attributes.get(key)

    def update_attribute(self, key: str, value: Any) -> None:
        self.set_attribute(key, value)

    def delete_attribute(self, key: str) -> None:
        if key in self.attributes:
            del self.attributes[key]

    def get_attribute_type(self, key: str) -> SupportedType:

        if key not in self.attributes:
            raise KeyError("The given attribute does not exist, so it lacks a type!")

        return type(self.attributes[key])

    def get_all_attributes(self) -> Dict[str, SupportedValue]:
        """Returns a copy, ensuring that the original will not get modified!"""
        return deepcopy(self.attributes)

    def has_attribute(self, query: str) -> bool:
        """
        Check if query attribute even exists.
        Case-insensitive search.
        """
        if not query:
            return False

        query_lower = query.lower()

        # Search in attribute names
        if any(query_lower in key.lower() for key in self.attributes.keys()):
            return True

        return False

    def __repr__(self) -> str:
        attrs = ", ".join(f"{k}={v}" for k, v in self.attributes.items())
        return f"Node({self.node_id}, {attrs})"

    def __eq__(self, other) -> bool:
        """Two nodes are equal if they have the same ID"""
        if not isinstance(other, Node):
            return False
        return self.node_id == other.node_id

    def to_dict(self) -> Dict[str, SupportedValueOrDict]:

        """
        Convert node to dictionary for serialization, and HTML display.
        Caller is responsible for converting all attributes to its preferred type for storage/display
        Example: for converting all values to str, use TypeManager.validate_and_convert(value, str)
        """

        return {
            'id': self.node_id,
            'attributes': self.attributes,
        }

