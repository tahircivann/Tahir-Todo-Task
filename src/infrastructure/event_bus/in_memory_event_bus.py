from typing import Dict, List, Callable, Type
import logging

from ...application.ports.event_bus import EventBus
from ...domain.entities.base import DomainEvent

logger = logging.getLogger(__name__)


class InMemoryEventBus(EventBus):
    """Simple in-memory event bus for development."""
    
    def __init__(self):
        self._handlers: Dict[Type[DomainEvent], List[Callable]] = {}
    
    def publish(self, event: DomainEvent) -> None:
        """Publish event to all registered handlers."""
        event_type = type(event)
        
        logger.info(f"Publishing event: {event_type.__name__}")
        
        if event_type in self._handlers:
            for handler in self._handlers[event_type]:
                try:
                    handler(event)
                except Exception as e:
                    logger.error(f"Error handling {event_type.__name__}: {e}")
    
    def subscribe(self, event_type: Type[DomainEvent], handler: Callable) -> None:
        """Register a handler for an event type."""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        
        self._handlers[event_type].append(handler)
        logger.info(f"Subscribed handler to {event_type.__name__}")