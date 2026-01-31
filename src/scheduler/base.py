from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from src.simulator.task import Task


class Scheduler(ABC):
    """
    Abstract base class for all schedulers.
    """

    def __init__(self):
        # Tasks that have arrived but are not yet completed
        self.ready_queue: List[Task] = []

    @abstractmethod
    def name(self) -> str:
        """
        Return the name of the scheduler (e.g., EDF, RM).
        """
        pass  # pragma: no cover

    def add_task(self, task: Task):
        """
        Add a newly arrived task to the scheduler.
        """
        self.ready_queue.append(task)

    @abstractmethod
    def schedule(
        self,
        current_time: float,
        available_nodes: List[int]
    ) -> Dict[int, Optional[Task]]:
        """
        Decide which task runs on which node.

        Returns:
            A mapping:
                node_id -> Task (or None if node stays idle)
        """
        pass  # pragma: no cover

    def on_task_complete(self, task: Task):
        """
        Notify scheduler that a task has completed.
        """
        if task in self.ready_queue:
            self.ready_queue.remove(task)

    def has_pending_tasks(self) -> bool:
        """
        Check if there are unfinished tasks.
        """
        return len(self.ready_queue) > 0
