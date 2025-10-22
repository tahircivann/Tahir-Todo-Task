class DomainException(Exception):
    """Base exception for all domain-level errors."""
    pass


class InvalidDeadlineError(DomainException):
    """Raised when a deadline constraint is violated."""
    pass


class ProjectCompletionError(DomainException):
    """Raised when attempting to complete a project with incomplete tasks."""
    pass


class TaskNotFoundError(DomainException):
    """Raised when a task is not found."""
    pass


class ProjectNotFoundError(DomainException):
    """Raised when a project is not found."""
    pass


class TaskAlreadyLinkedError(DomainException):
    """Raised when attempting to link a task that's already linked."""
    pass