from abc import ABC, abstractmethod
from typing import Callable, Type

from ...domain.entities.base import DomainEvent


class EventBus(ABC):
    """Port (interface) for event publishing and subscribing."""
    
    @abstractmethod
    def publish(self, event: DomainEvent) -> None:
        """Publish a domain event."""
        pass
    
    @abstractmethod
    def subscribe(self, event_type: Type[DomainEvent], handler: Callable) -> None:
        """Subscribe a handler to an event type."""
        pass
