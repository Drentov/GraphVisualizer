"""
    Graph model - complete graph model.
    Support for directed/undirected, cyclic/acyclic graphs.
"""
from copy import deepcopy
from typing import Dict, List, Any, Optional, Set
from .node import Node
from .edge import Edge

class Graph:

    def __init__(self, graph_id: Any):
        """
        Args:
            graph_id: Unique identifier of the graph
        """
        self.graph_id = str(graph_id) #stored as a string
        self.nodes: Dict[str, Node] = {}  # node_id -> Node
        self.edges: Dict[str, Edge] = {}  # edge_id -> Edge
        self._adjacency_pairs: Dict[str, List[Edge]] = {}  # node_id -> [Edges] #similar in use as connectionsMap in JS

    def add_node(self, node: Node) -> None:

        """Add a node to the graph"""

        if node.node_id in self.nodes:
            raise ValueError(f"Node with id {node.node_id} already exists!")

        self.nodes[node.node_id] = node
        self._adjacency_pairs[node.node_id] = []

    def get_node(self, node_id: str) -> Optional[Node]:
        return self.nodes.get(node_id)

    def remove_node(self, node_id: str) -> None:
        """Remove a node and all connected edges."""

        if node_id not in self.nodes:
            raise ValueError(f"Node {node_id} not in graph")

        # 1. Identify edges to delete
        edges_to_delete = set()

        edge_list = self._adjacency_pairs.get(node_id, [])
        for edge in edge_list:
            edges_to_delete.add(edge.edge_id)

        # 2. Delete edges
        for edge_id in edges_to_delete:
            self.remove_edge(edge_id)

        # 3. Delete node
        del self.nodes[node_id]
        if node_id in self._adjacency_pairs:
            del self._adjacency_pairs[node_id]

    def add_edge(self, edge: Edge) -> None:

        """Add an edge to the graph"""

        if edge.source_node.node_id not in self.nodes:
            raise ValueError(f"Source node {edge.source_node.node_id} not in graph!")
        if edge.destination_node.node_id not in self.nodes:
            raise ValueError(f"Destination node {edge.destination_node.node_id} not in graph!")

        if edge.edge_id in self.edges:
            raise ValueError(f"Edge with id {edge.edge_id} already added to graph!")

        self.edges[edge.edge_id] = edge

        # Add to adjacency list for BOTH nodes (optimization for faster access)
        self._adjacency_pairs[edge.source_node.node_id].append(edge)

        if edge.source_node.node_id != edge.destination_node.node_id:
            self._adjacency_pairs[edge.destination_node.node_id].append(edge)

    def get_edge(self, edge_id: str) -> Optional[Edge]:
        return self.edges.get(edge_id)

    def remove_edge(self, edge_id: str) -> None:
        """Remove an edge from the graph"""
        if edge_id not in self.edges:
            return  # Safe delete is often better than raising ValueError

        edge = self.edges[edge_id]
        source_id = edge.source_node.node_id
        destination_id = edge.destination_node.node_id

        # Remove from source adjacency pairs
        if source_id in self._adjacency_pairs:
            self._adjacency_pairs[source_id] = [edge for edge in self._adjacency_pairs[source_id] if edge.edge_id != edge_id]

        # Remove from target adjacency pairs
        if destination_id in self._adjacency_pairs:
            self._adjacency_pairs[destination_id] = [e for e in self._adjacency_pairs[destination_id] if e.edge_id != edge_id]

        del self.edges[edge_id]

    def get_all_nodes(self) -> List[Node]:
        return list(self.nodes.values())

    def get_all_edges(self) -> List[Edge]:
        return list(self.edges.values())

    def get_number_of_nodes(self) -> int:
        return len(self.nodes)

    def get_number_of_edges(self) -> int:
        return len(self.edges)

    def has_cycle(self) -> bool:
        """
        Check if the graph has a cycle.
        Supports mixed (directed/undirected) graphs.
        """

        visited_node_ids_set = set()
        in_exploration_ids_set = set()

        def depth_first_search(search_node_id: str, parent_edge: Optional[Edge]) -> bool:

            visited_node_ids_set.add(search_node_id)
            in_exploration_ids_set.add(search_node_id)

            node = self.nodes[search_node_id]

            for edge in self._get_traversable_edges(node):

                if edge is parent_edge:
                    continue

                neighbor = edge.get_other_node(node)

                if not neighbor and edge.source_node == edge.destination_node:
                    neighbor = node  # Self loop (circular looping edge)

                neighbor_id = neighbor.node_id

                if neighbor_id not in visited_node_ids_set:
                    if depth_first_search(neighbor_id, edge):
                        return True

                elif neighbor_id in in_exploration_ids_set:
                    return True

            in_exploration_ids_set.remove(search_node_id)
            return False

        for node_id in self.nodes:
            if node_id not in visited_node_ids_set:
                if depth_first_search(node_id, None):
                    return True

        return False

    def _get_traversable_edges(self, node: Node) -> List[Edge]:
        """
        Returns all edges that can be traversed from the given node:
        1. Directed edges originating from this node.
        2. Undirected edges connected to this node.
        """

        result = []

        for edge in self._adjacency_pairs.get(node.node_id, []):

            if edge.source_node == node:
                result.append(edge)

            elif not edge.directed and edge.destination_node == node:
                result.append(edge)

        return result

    def get_subgraph_by_nodes(self, node_ids: Set[str]) -> 'Graph':

        """
        Create a subgraph (deep copy) with specified nodes.
        """
        subgraph = Graph(f"{self.graph_id}_subgraph")

        # We use deepcopy so changes to the subgraph don't affect the main graph
        for node_id in node_ids:
            if node_id in self.nodes:
                subgraph.add_node(deepcopy(self.nodes[node_id]))

        # Add edges only if BOTH nodes exist in the subgraph
        for edge in self.edges.values():
            if edge.source_node.node_id in node_ids and edge.destination_node.node_id in node_ids:

                # We must find the newly created instances of nodes in the subgraph
                new_source = subgraph.get_node(edge.source_node.node_id)
                new_target = subgraph.get_node(edge.destination_node.node_id)

                new_edge = Edge(
                    edge.edge_id,
                    new_source,
                    new_target,
                    edge.directed,
                    **edge.attributes
                )

                subgraph.add_edge(new_edge)

        return subgraph

    def __repr__(self) -> str:
        return f"Graph({self.graph_id}, nodes={list(self.nodes)}, edges={list(self.edges)})"

    def to_dict(self) -> Dict:
        return {
            'id': self.graph_id,
            'nodes': [node.to_dict() for node in self.nodes.values()],
            'edges': [edge.to_dict() for edge in self.edges.values()]
        }



