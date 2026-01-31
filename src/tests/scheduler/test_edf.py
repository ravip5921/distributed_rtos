import unittest
from typing import List, Dict, Optional

from src.simulator.clock import SimClock
from src.simulator.task import Task
from src.scheduler.edf import EDFScheduler


class TestEDFScheduler(unittest.TestCase):
    """Unit tests for EDFScheduler."""

    def setUp(self) -> None:
        self.clock = SimClock()
        self.scheduler = EDFScheduler()

    def _assert_schedule(
        self,
        tasks: List[Task],
        available_nodes: List[int],
        expected_task_ids: List[Optional[int]],
        msg: Optional[str] = None,
    ) -> None:
        """
        Helper function to add tasks, run scheduler, and assert node assignments.

        Args:
            tasks: List of Task objects to add to the scheduler.
            available_nodes: List of node IDs to schedule tasks on.
            expected_task_ids: List of expected task IDs for each node.
            msg: Optional message for assertion failure.
        """
        for t in tasks:
            self.scheduler.add_task(t)

        schedule: Dict[int, Optional[Task]] = self.scheduler.schedule(
            self.clock.now(), available_nodes
        )

        assigned_ids: List[Optional[int]] = [
            task.task_id if (task := schedule[node_id]) is not None else None
            for node_id in available_nodes
        ]

        # Check lengths
        self.assertEqual(
            len(assigned_ids),
            len(expected_task_ids),
            msg or f"Assigned nodes {assigned_ids} != expected {expected_task_ids}",
        )

        # Check each assignment
        for assigned, expected, node_id in zip(assigned_ids, expected_task_ids, available_nodes):
            self.assertEqual(
                assigned,
                expected,
                msg or f"Node {node_id}: assigned task {assigned}, expected {expected}",
            )

    # ----- Tests -----

    def test_name(self) -> None:
        """Scheduler should report its name."""
        self.assertEqual(self.scheduler.name(), "EDF")

    def test_single_node(self) -> None:
        """EDF should schedule the task with the earliest deadline on a single node."""
        tasks = [
            Task(task_id=1, arrival_time=0, execution_time=3, deadline=10),
            Task(task_id=2, arrival_time=0, execution_time=2, deadline=5),
            Task(task_id=3, arrival_time=0, execution_time=1, deadline=7),
        ]
        self._assert_schedule(tasks, available_nodes=[0], expected_task_ids=[2])

    def test_multiple_nodes(self) -> None:
        """EDF should assign tasks with earliest deadlines to multiple nodes."""
        tasks = [
            Task(task_id=1, arrival_time=0, execution_time=3, deadline=10),
            Task(task_id=2, arrival_time=0, execution_time=2, deadline=5),
            Task(task_id=3, arrival_time=0, execution_time=1, deadline=7),
            Task(task_id=4, arrival_time=0, execution_time=4, deadline=3),
        ]
        # Node 0 gets earliest deadline (task 4), node 1 gets second earliest (task 2)
        self._assert_schedule(tasks, available_nodes=[0, 1], expected_task_ids=[4, 2])

    def test_empty_nodes(self) -> None:
        """Scheduler should return None for all nodes if no tasks are ready."""
        self._assert_schedule([], available_nodes=[0, 1], expected_task_ids=[None, None])

    def test_more_nodes_than_tasks(self) -> None:
        """Scheduler should leave extra nodes idle if tasks < nodes."""
        tasks = [
            Task(task_id=1, arrival_time=0, execution_time=2, deadline=5),
            Task(task_id=2, arrival_time=0, execution_time=3, deadline=10),
        ]
        self._assert_schedule(tasks, available_nodes=[0, 1, 2], expected_task_ids=[1, 2, None])
