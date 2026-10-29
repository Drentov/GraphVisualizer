"""
    Edge model - representation of an edge between nodes.
"""
from typing import Any, Dict, Optional
from .node import  Node
from ...type_manager import TypeManager, SupportedValue

class Edge:
    """
        Class for an edge between two nodes.
        An edge can be directed or undirected.
    """

    def __init__(
            self,
            edge_id: Any,
            source_node: Node,
            target_node: Node,
            directed: bool,
            weight: Optional[int] = None,
            **attributes
    ):
        """
        Initialize an edge.

        Args:
            edge_id: Unique identifier of the edge (will be converted to str)
            source_node: Source node
            target_node: Target node
            direction: Edge type (DIRECTED or UNDIRECTED)
            **attributes: Arbitrary edge attributes
        """
        # Ensure ID is always a string for consistency
        self.edge_id = str(edge_id)
        self.source_node = source_node
        self.target_node = target_node
        self.directed = directed
        self.weight = weight
        self.attributes: Dict[str, SupportedValue] = {}

        # Add attributes with type detection
        for key, value in attributes.items():
            self.set_attribute(key, value)


    def set_attribute(self, key: str, value: SupportedValue) -> None:
        """
        Set edge attribute with type detection.
        """

        # This satisfies the requirement that data is not stored only as string
        detected_type = TypeManager.detect_type(value)
        converted_value = TypeManager.validate_and_convert(value, detected_type)

        self.attributes[key] = converted_value

