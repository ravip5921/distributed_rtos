import unittest
from src.simulator.task import Task


class TestTask(unittest.TestCase):
    """Unit tests for Task dataclass."""

    def setUp(self) -> None:
        self.task = Task(task_id=1, arrival_time=0, execution_time=2, deadline=5)

    def test_initialization(self):
        """Task should initialize with correct default runtime state."""
        self.assertEqual(self.task.task_id, 1)
        self.assertEqual(self.task.arrival_time, 0)
        self.assertEqual(self.task.execution_time, 2)
        self.assertEqual(self.task.deadline, 5)
        self.assertIsNone(self.task.start_time)
        self.assertIsNone(self.task.finish_time)
        self.assertIsNone(self.task.assigned_node)
        self.assertIsNone(self.task.priority)

    def test_is_completed_false(self):
        """is_completed should return False if finish_time is None."""
        self.assertFalse(self.task.is_completed())

    def test_is_completed_true(self):
        """is_completed should return True if finish_time is set."""
        self.task.finish_time = 4
        self.assertTrue(self.task.is_completed())

    def test_missed_deadline_false(self):
        """missed_deadline should return False if finish_time <= deadline."""
        self.task.finish_time = 4
        self.assertFalse(self.task.missed_deadline())

    def test_missed_deadline_true(self):
        """missed_deadline should return True if finish_time > deadline."""
        self.task.finish_time = 6
        self.assertTrue(self.task.missed_deadline())

    def test_missed_deadline_none_finish(self):
        """missed_deadline should return False if finish_time is None."""
        self.assertFalse(self.task.missed_deadline())