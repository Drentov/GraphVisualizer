"""Abstract base class for graph nodes."""

from abc import ABC, abstractmethod
from typing import Any, Dict

from ...type_manager import SupportedValue, SupportedType, SupportedValueOrDict


class BaseNode(ABC):

    @abstractmethod
    def set_attribute(self, key: str, value: SupportedValue) -> None:
        """Set a node attribute."""
        pass

    @abstractmethod
    def get_attribute(self, key: str) -> Any:
        """Retrieve an attribute by key."""
        pass

    @abstractmethod
    def update_attribute(self, key: str, value: Any) -> None:
        """Update an existing attribute."""
        pass

    @abstractmethod
    def delete_attribute(self, key: str) -> None:
        """Delete an attribute."""
        pass

    @abstractmethod
    def get_attribute_type(self, key: str) -> SupportedType:
        """Get the type of an attribute."""
        pass

    @abstractmethod
    def get_all_attributes(self) -> Dict[str, SupportedValue]:
        """Return a copy of all attributes."""
        pass

    @abstractmethod
    def has_attribute(self, query: str) -> bool:
        """Check whether an attribute name matches a query."""
        pass

    @abstractmethod
    def __repr__(self) -> str:
        """Return a string representation of the node."""
        pass

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        """Compare nodes by ID."""
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, SupportedValueOrDict]:
        """Convert entire node to dictionary"""
        pass
