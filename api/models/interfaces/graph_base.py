"""Abstract graph model."""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Set
from .node_base import BaseNode
from .edge_base import BaseEdge


class BaseGraph(ABC):

    @abstractmethod
    def add_node(self, node: BaseNode) -> None:
        """Add a node to the graph."""
        pass

    @abstractmethod
    def get_node(self, node_id: str) -> Optional[BaseNode]:
        """Get a node by its ID."""
        pass

    @abstractmethod
    def remove_node(self, node_id: str) -> None:
        """Remove a node and all connected edges."""
        pass

    @abstractmethod
    def add_edge(self, edge: BaseEdge) -> None:
        """Add an edge to the graph."""
        pass

    @abstractmethod
    def get_edge(self, edge_id: str) -> Optional[BaseEdge]:
        """Get an edge by its ID."""
        pass

    @abstractmethod
    def remove_edge(self, edge_id: str) -> None:
        """Remove an edge from the graph."""
        pass

    @abstractmethod
    def get_all_nodes(self) -> List[BaseNode]:
        """Get all nodes in the graph."""
        pass

    @abstractmethod
    def get_all_edges(self) -> List[BaseEdge]:
        """Get all edges in the graph."""
        pass

    @abstractmethod
    def get_number_of_nodes(self) -> int:
        """Get the number of nodes in the graph."""
        pass

    @abstractmethod
    def get_number_of_edges(self) -> int:
        """Get the number of edges in the graph."""
        pass

    @abstractmethod
    def has_cycle(self) -> bool:
        """Check whether the graph contains a cycle."""
        pass

    @abstractmethod
    def get_subgraph_by_nodes(self, node_ids: Set[str]) -> 'Graph':
        """Get a subgraph containing the specified nodes."""
        pass

    @abstractmethod
    def __repr__(self) -> str:
        """String representation of the graph."""
        pass

    @abstractmethod
    def to_dict(self) -> Dict:
        """Convert the graph to a dictionary for serialization."""
        pass