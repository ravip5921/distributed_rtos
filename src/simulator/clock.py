class SimClock:
    """
    Logical simulation clock.
    """

    def __init__(self, start_time: float = 0.0):
        self._time = start_time

    def now(self) -> float:
        """Return current simulation time."""
        return self._time

    def advance(self, delta: float):
        """
        Advance the simulation clock by delta time units.
        """
        if delta < 0:
            raise ValueError("Clock cannot go backwards")
        self._time += delta

    def set(self, t: float):
        """
        Force clock to a specific time.
        """
        if t < self._time:
            raise ValueError("Cannot rewind simulation clock")
        self._time = t
