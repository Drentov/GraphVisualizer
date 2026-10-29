from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from .node_base import BaseNode
from ...type_manager import SupportedValue, SupportedValueOrDict


class BaseEdge(ABC):
    """Abstract base class for an edge between two nodes."""

    @abstractmethod
    def set_attribute(self, key: str, value: SupportedValue) -> None:
        """Set edge attribute with type detection."""
        pass

    @abstractmethod
    def get_source_node(self) -> BaseNode:
        """Get source node."""
        pass

    @abstractmethod
    def get_target_node(self) -> BaseNode:
        """Get target node."""
        pass

    @abstractmethod
    def get_other_node(self, node: BaseNode) -> Optional[BaseNode]:
        """Get the other end of the edge."""
        pass

    @abstractmethod
    def is_directed(self) -> bool:
        """Check if edge is directed."""
        pass

    @abstractmethod
    def get_attribute(self, key: str) -> SupportedValue:
        """Get edge attribute value."""
        pass

    @abstractmethod
    def update_attribute(self, key: str, value: SupportedValue) -> None:
        """Update edge attribute."""
        pass

    @abstractmethod
    def delete_attribute(self, key: str) -> None:
        """Delete edge attribute."""
        pass

    @abstractmethod
    def get_all_attributes(self) -> Dict[str, SupportedValue]:
        """Get all edge attributes."""
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, SupportedValueOrDict]:
        """
        Convert edge to a dictionary for serialization and HTML display.
        """
        pass

    @abstractmethod
    def __repr__(self) -> str:
        """String representation of the edge."""
        pass

    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        """Check whether two edges are equal."""
        pass