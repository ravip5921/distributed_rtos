import unittest
from src.simulator.clock import SimClock


class TestSimClock(unittest.TestCase):
    """Unit tests for SimClock."""

    def test_default_initialization(self):
        """Clock should start at 0.0 by default."""
        clock = SimClock()
        self.assertEqual(clock.now(), 0.0)

    def test_custom_initialization(self):
        """Clock should start at specified start_time."""
        clock = SimClock(start_time=5.5)
        self.assertEqual(clock.now(), 5.5)

    def test_advance_normal(self):
        """Clock should advance by delta correctly."""
        clock = SimClock()
        clock.advance(2.5)
        self.assertEqual(clock.now(), 2.5)
        clock.advance(1.5)
        self.assertEqual(clock.now(), 4.0)

    def test_advance_negative_raises(self):
        """Advancing by negative delta should raise ValueError."""
        clock = SimClock()
        with self.assertRaises(ValueError):
            clock.advance(-1.0)

    def test_set_normal(self):
        """Clock should set to a new time >= current."""
        clock = SimClock()
        clock.set(5.0)
        self.assertEqual(clock.now(), 5.0)
        clock.set(10.0)
        self.assertEqual(clock.now(), 10.0)

    def test_set_rewind_raises(self):
        """Setting clock to time less than current should raise ValueError."""
        clock = SimClock(start_time=5.0)
        with self.assertRaises(ValueError):
            clock.set(4.0)


