import unittest
from typing import List, Dict, Optional

from src.simulator.task import Task
from src.scheduler.base import Scheduler


class DummyScheduler(Scheduler):
    """
    Minimal concrete subclass of Scheduler for testing purposes.
    Implements abstract methods trivially.
    """

    def name(self) -> str:
        return "Dummy"

    def schedule(
        self, current_time: float, available_nodes: List[int]
    ) -> Dict[int, Optional[Task]]:
        # Just assign first task to first node if exists
        schedule: Dict[int, Optional[Task]] = {}
        for i, node in enumerate(available_nodes):
            if i < len(self.ready_queue):
                schedule[node] = self.ready_queue[i]
            else:
                schedule[node] = None
        return schedule


class TestSchedulerBase(unittest.TestCase):
    """Unit tests for Scheduler base class."""

    def setUp(self) -> None:
        self.sched = DummyScheduler()
        self.task1 = Task(task_id=1, arrival_time=0, execution_time=1, deadline=10)
        self.task2 = Task(task_id=2, arrival_time=0, execution_time=2, deadline=5)

    def test_name_method(self) -> None:
        """Scheduler should return the correct name."""
        self.assertEqual(self.sched.name(), "Dummy")

    def test_add_task(self) -> None:
        """Adding tasks should populate the ready queue."""
        self.assertFalse(self.sched.has_pending_tasks())
        self.sched.add_task(self.task1)
        self.assertTrue(self.sched.has_pending_tasks())
        self.assertIn(self.task1, self.sched.ready_queue)

    def test_on_task_complete(self) -> None:
        """Completed tasks should be removed from the ready queue."""
        self.sched.add_task(self.task1)
        self.sched.add_task(self.task2)
        self.assertEqual(len(self.sched.ready_queue), 2)
        self.sched.on_task_complete(self.task1)
        self.assertNotIn(self.task1, self.sched.ready_queue)
        self.assertIn(self.task2, self.sched.ready_queue)

        # Completing a task not in queue should not raise
        self.sched.on_task_complete(self.task1)  # no error
        self.assertEqual(len(self.sched.ready_queue), 1)

    def test_has_pending_tasks(self) -> None:
        """has_pending_tasks reflects ready_queue status correctly."""
        self.assertFalse(self.sched.has_pending_tasks())
        self.sched.add_task(self.task1)
        self.assertTrue(self.sched.has_pending_tasks())
        self.sched.on_task_complete(self.task1)
        self.assertFalse(self.sched.has_pending_tasks())

    def test_schedule_assignments(self) -> None:
        """Dummy schedule returns expected node-task mapping."""
        self.sched.add_task(self.task1)
        self.sched.add_task(self.task2)
        available_nodes = [0, 1, 2]
        schedule = self.sched.schedule(0.0, available_nodes)

        # Should assign first task to first node, second task to second node, last node idle
        task0 = schedule[0]
        task1 = schedule[1]

        assert task0 is not None
        assert task1 is not None

        self.assertEqual(task0.task_id, self.task1.task_id)
        self.assertEqual(task1.task_id, self.task2.task_id)
        self.assertIsNone(schedule[2])