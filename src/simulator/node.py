from typing import Optional
from src.simulator.clock import SimClock
from src.simulator.task import Task


class Node:
    """
    Simulated worker node for preemptive EDF.
    """

    def __init__(self, node_id: int, clock: SimClock):
        self.node_id = node_id
        self.clock = clock
        self.current_task: Optional[Task] = None

    def is_idle(self) -> bool:
        return self.current_task is None

    def assign_task(self, task: Task) -> Optional[Task]:
        """
        Assign a task to this node. Preempts current task if needed.
        Returns preempted task (if any).
        """
        preempted_task: Optional[Task] = None

        if self.current_task is not None:
            # Check if new task has earlier deadline → preempt
            if task.deadline < self.current_task.deadline:
                if self.current_task.start_time is None or self.current_task.remaining_time is None:
                    raise RuntimeError("Current task not properly initialized")   # pragma: no cover

                # Save remaining time
                self.current_task.remaining_time -= self.clock.now() - self.current_task.start_time
                preempted_task = self.current_task
                print(f"[Node {self.node_id}] Preempting task {self.current_task.task_id} "
                      f"({self.current_task.remaining_time:.2f} left) for task {task.task_id}")
            else:
                # Cannot preempt, return task back to scheduler
                return task

        # Assign new task
        if task.start_time is None:
            task.start_time = self.clock.now()
        task.assigned_node = self.node_id
        self.current_task = task
        return preempted_task

    def run_until(self, target_time: float) -> Optional[Task]:
        """
        Run current task until target_time or until it finishes.
        Returns preempted task if it didn't finish.
        """
        if self.current_task is None:
            return None

        if self.current_task.remaining_time is None or self.current_task.start_time is None:
            raise RuntimeError("Task not properly initialized")   # pragma: no cover
        
        exec_time = min(self.current_task.remaining_time, target_time - self.clock.now())
        if exec_time < 0:
            exec_time = 0.0   # pragma: no cover

        self.clock.advance(exec_time)
        self.current_task.remaining_time -= exec_time

        # If task finished
        if self.current_task.remaining_time <= 0:
            self.current_task.finish_time = self.clock.now()
            print(f"[Node {self.node_id}] Task {self.current_task.task_id} finished "
                  f"at {self.current_task.finish_time:.2f}")
            self.current_task = None
            return None

        # Task still running → preempted by clock/event
        print(f"[Node {self.node_id}] Task {self.current_task.task_id} ran until {self.clock.now():.2f} "
              f"({self.current_task.remaining_time:.2f} left)")
        return self.current_task
