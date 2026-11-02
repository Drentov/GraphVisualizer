from abc import ABC, abstractmethod
from ..models.graph import Graph


class VisualizerInterface(ABC):
    """
    Abstract base class for Visualizer plugins.
    Defines a common interface for all Visualizer implementations to use.
    """


    @abstractmethod
    def to_visual_form(self, graph: Graph) -> str:

        #Convert a graph into an HTML representation.
        #INPUT: a graph object
        #OUTPUT: string (html) representation of said graph
        #The caller is responsible for sending said string to the frontend

        pass