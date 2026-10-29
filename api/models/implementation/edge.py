"""
    Edge model - representation of an edge between nodes.
"""
from copy import deepcopy
from typing import Any, Dict, Optional
from .node import Node
from ..interfaces.edge_base import BaseEdge
from ...type_manager import TypeManager, SupportedValue, SupportedValueOrDict


class Edge(BaseEdge):
    """
        Class for an edge between two nodes.
        An edge can be directed or undirected.
    """

    def __init__(
            self,
            edge_id: Any,
            source_node: Node,
            destination_node: Node,
            directed: bool = False,
            weight: Optional[int] = None,
            **attributes
    ):
        """
        Initialize an edge.

        Args:
            edge_id: Unique identifier of the edge (will be converted to str)
            source_node: Source node
            destination_node: Target node
            direction: Edge type (DIRECTED or UNDIRECTED)
            **attributes: Arbitrary edge attributes
        """
        # Ensure ID is always a string for consistency
        self.edge_id = str(edge_id)
        self.source_node = source_node
        self.destination_node = destination_node
        self.directed = directed
        self.attributes: Dict[str, SupportedValue] = {}

        if weight is not None:
            self.set_attribute("weight", weight)

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

    def get_source_node(self) -> Node:
        """Get source and target nodes"""
        return self.source_node

    def get_target_node(self) -> Node:
        return self.destination_node

    def get_other_node(self, node: Node) -> Optional[Node]:
        """If edge is undirected, get the other end of the edge"""
        if node == self.source_node:
            return self.destination_node
        elif node == self.destination_node:
            return self.source_node
        return None

    def is_directed(self) -> bool:
        """Check if edge is directed"""
        return self.directed

    def get_attribute(self, key: str) -> SupportedValue:
        """Get edge attribute value"""
        return self.attributes.get(key)

    def update_attribute(self, key: str, value: SupportedValue) -> None:
        """Update edge attribute"""
        self.set_attribute(key, value)

    def delete_attribute(self, key: str) -> None:
        """Delete edge attribute"""
        if key in self.attributes:
            del self.attributes[key]

    def get_all_attributes(self) -> Dict[str, SupportedValue]:
        """Get all edge attributes"""
        return deepcopy(self.attributes)

    def __repr__(self) -> str:
        """String representation of edge"""
        line = "->" if self.directed else "--"
        return f"Edge({self.source_node.node_id} {line} {self.destination_node.node_id})"

    def __eq__(self, other) -> bool:
        """Two edges are equal if they have the same ID"""
        if not isinstance(other, Edge):
            return False
        return self.edge_id == other.edge_id

    def to_dict(self) -> Dict[str, SupportedValueOrDict]:

        """
        Convert edge to dictionary for serialization, and HTML display.
        Caller is responsible for converting all attributes to its preferred type for storage/display
        Example: for converting all values to str, use TypeManager.validate_and_convert(value, str)
        """

        return {
            'id': self.edge_id,
            'source-node': self.source_node.node_id,
            'destination-node': self.destination_node.node_id,
            'directed': self.directed,
            'attributes': self.attributes,
        }
