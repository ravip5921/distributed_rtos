from dataclasses import dataclass, field
from typing import Optional

@dataclass(order=True)
class Task:
    """
    Represents a real-time task in the system.
    """
    deadline: float
    arrival_time: float = field(compare=False)
    execution_time: float = field(compare=False)
    task_id: int = field(compare=False)
    priority: Optional[int] = field(default=None, compare=False)

    # Runtime state
    start_time: Optional[float] = field(default=None, compare=False)
    finish_time: Optional[float] = field(default=None, compare=False)
    assigned_node: Optional[int] = field(default=None, compare=False)
    remaining_time: Optional[float] = field(default=None, compare=False)

    def is_completed(self) -> bool:
        return self.finish_time is not None

    def missed_deadline(self) -> bool:
        return (
            self.finish_time is not None and
            self.finish_time > self.deadline
        )
    def __post_init__(self):
        self.remaining_time = self.execution_time