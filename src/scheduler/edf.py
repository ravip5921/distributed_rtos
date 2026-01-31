from typing import List, Dict, Optional
from src.scheduler.base import Scheduler
from src.simulator.task import Task


class EDFScheduler(Scheduler):
    """
    Earliest Deadline First (EDF) scheduler.
    Non-preemptive version.
    """

    def name(self) -> str:
        return "EDF"

    def schedule(
        self,
        current_time: float,
        available_nodes: List[int]
    ) -> Dict[int, Optional[Task]]:
        """
        Assign tasks with earliest deadlines to available nodes.
        """

        # Sort ready tasks by deadline (earliest first)
        self.ready_queue.sort(key=lambda t: t.deadline)

        schedule: Dict[int, Optional[Task]] = {}

        for node_id in available_nodes:
            if self.ready_queue:
                task = self.ready_queue.pop(0)
                task.start_time = current_time
                task.assigned_node = node_id
                schedule[node_id] = task
            else:
                schedule[node_id] = None

        return schedule
