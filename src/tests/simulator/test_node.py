import unittest
from src.simulator.clock import SimClock
from src.simulator.task import Task
from src.simulator.node import Node


class TestNodePreemptive(unittest.TestCase):
    """Unit tests for Node class with preemptive support."""

    def setUp(self):
        self.clock = SimClock()
        self.node = Node(node_id=0, clock=self.clock)

    def test_initial_state(self):
        """Node should start idle with no task."""
        self.assertTrue(self.node.is_idle())
        self.assertIsNone(self.node.current_task)

    def test_assign_task_sets_properties(self):
        """Assigning a task sets start_time, assigned_node, remaining_time."""
        t = Task(task_id=1, arrival_time=0, execution_time=3, deadline=5)
        preempted = self.node.assign_task(t)
        self.assertIsNone(preempted)
        self.assertFalse(self.node.is_idle())
        self.assertEqual(t.start_time, 0.0)
        self.assertEqual(t.assigned_node, 0)
        self.assertEqual(t.remaining_time, 3.0)

    def test_run_until_completes_task(self):
        """run_until should complete task if enough time is given."""
        t = Task(task_id=1, arrival_time=0, execution_time=4, deadline=10)
        self.node.assign_task(t)
        preempted = self.node.run_until(target_time=10.0)
        self.assertIsNone(preempted)
        self.assertTrue(self.node.is_idle())
        self.assertEqual(t.finish_time, 4.0)
        self.assertEqual(self.clock.now(), 4.0)

    def test_run_until_partial_execution(self):
        """run_until should partially execute task if target_time reached."""
        t = Task(task_id=1, arrival_time=0, execution_time=5, deadline=10)
        self.node.assign_task(t)
        preempted = self.node.run_until(target_time=2.0)
        self.assertIs(preempted, t)
        self.assertFalse(self.node.is_idle())
        
        remaining = t.remaining_time
        assert remaining is not None
        self.assertEqual(round(remaining), 3)
        
        self.assertEqual(self.clock.now(), 2.0)

    def test_preemption_by_assign_task(self):
        """Assigning earlier-deadline task should preempt running task."""
        t1 = Task(task_id=1, arrival_time=0, execution_time=5, deadline=10)
        t2 = Task(task_id=2, arrival_time=0, execution_time=2, deadline=5)
        self.node.assign_task(t1)
        self.clock.advance(2.0)  # t1 runs 2 units
        preempted = self.node.assign_task(t2)
        self.assertIs(preempted, t1)
        self.assertEqual(t1.remaining_time, 3.0)
        self.assertEqual(self.node.current_task, t2)
        self.assertEqual(t2.start_time, 2.0)

    def test_assign_task_lower_priority_no_preempt(self):
        """Assigning task with later deadline does not preempt current task."""
        t1 = Task(task_id=1, arrival_time=0, execution_time=3, deadline=5)
        t2 = Task(task_id=2, arrival_time=0, execution_time=2, deadline=10)
        self.node.assign_task(t1)
        preempted = self.node.assign_task(t2)
        self.assertIs(preempted, t2)  # t2 returned back because cannot preempt
        self.assertEqual(self.node.current_task, t1)
        self.assertEqual(t1.remaining_time, 3.0)
        self.assertTrue(self.node.current_task is t1)

    def test_run_until_no_task(self):
        """run_until on idle node should do nothing."""
        preempted = self.node.run_until(target_time=5.0)
        self.assertIsNone(preempted)
        self.assertTrue(self.node.is_idle())
        self.assertEqual(self.clock.now(), 0.0)

    def test_multiple_sequential_tasks(self):
        """Node executes multiple tasks sequentially."""
        t1 = Task(task_id=1, arrival_time=0, execution_time=2, deadline=5)
        t2 = Task(task_id=2, arrival_time=0, execution_time=3, deadline=6)

        self.node.assign_task(t1)
        self.node.run_until(10.0)
        self.assertTrue(self.node.is_idle())
        self.assertEqual(t1.finish_time, 2.0)
        self.assertEqual(self.clock.now(), 2.0)

        self.node.assign_task(t2)
        self.node.run_until(10.0)
        self.assertTrue(self.node.is_idle())
        self.assertEqual(t2.start_time, 2.0)
        self.assertEqual(t2.finish_time, 5.0)
        self.assertEqual(self.clock.now(), 5.0)