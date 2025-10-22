from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4


@dataclass
class DomainEvent:
    """Base class for all domain events."""
    event_id: UUID = field(init=False)
    occurred_at: datetime = field(init=False)
    
    def __post_init__(self):
        self.event_id = uuid4()
        self.occurred_at = datetime.now(timezone.utc)
