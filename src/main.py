# from src.simulator.clock import SimClock
# from src.simulator.task import Task

# clock = SimClock()

# t1 = Task(task_id=1, arrival_time=0, execution_time=3, deadline=10)
# t2 = Task(task_id=2, arrival_time=0, execution_time=2, deadline=5)

# tasks = [t1, t2]
# tasks.sort()

# for t in tasks:
#     print(f"Task {t.task_id} deadline {t.deadline}")


# from src.scheduler.base import Scheduler

# print(Scheduler.__abstractmethods__)

from dataclasses import dataclass

import heapq
import random
from typing import List, Dict, Optional, Tuple
from src.simulator.clock import SimClock
from src.simulator.task import Task
from src.simulator.node import Node
from src.scheduler.edf import EDFScheduler


# Event types
ARRIVAL = "arrival"
COMPLETION = "completion"


@dataclass(order=True)
class Event:
    time: float
    type: str
    task: Task


def main() -> None:
    # -------------------------
    # Simulation setup
    # -------------------------
    clock = SimClock()
    scheduler = EDFScheduler()

    # Nodes
    nodes: List[Node] = [Node(node_id=i, clock=clock) for i in range(2)]

    # Randomized task arrivals
    tasks: List[Task] = []
    for i in range(1, 6):
        arrival = random.uniform(0, 5)
        execution = random.uniform(1, 4)
        deadline = arrival + random.uniform(3, 8)
        task = Task(task_id=i, arrival_time=arrival, execution_time=execution, deadline=deadline)
        tasks.append(task)

    # Event queue (min-heap by time)
    events: List[Event] = [Event(task.arrival_time, ARRIVAL, task) for task in tasks]
    heapq.heapify(events)

    print(f"Simulation start\n")

    # -------------------------
    # Simulation loop
    # -------------------------
    while events or any(not node.is_idle() for node in nodes) or scheduler.ready_queue:
        # Next event time
        next_event_time = events[0].time if events else float('inf')

        # Advance nodes until next event
        for node in nodes:
            if not node.is_idle():
                node.run_until(next_event_time)

        clock.set(next_event_time)

        # Process all events at this time
        while events and events[0].time <= clock.now():
            event = heapq.heappop(events)
            if event.type == ARRIVAL:
                print(f"Time {clock.now():.2f}: Task {event.task.task_id} arrives (deadline {event.task.deadline:.2f})")
                scheduler.add_task(event.task)

        # Assign ready tasks to idle nodes (handle preemption)
        for node in nodes:
            if node.is_idle() and scheduler.ready_queue:
                task = scheduler.ready_queue.pop(0)
                node.assign_task(task)

    # -------------------------
    # Print summary
    # -------------------------
    print("\nSimulation end\n")
    print("Task execution summary:")
    for task in tasks:
        status = "OK" if not task.missed_deadline() else "MISS"
        print(
            f"Task {task.task_id}: start={task.start_time:.2f}, "
            f"finish={task.finish_time:.2f}, deadline={task.deadline:.2f}, status={status}"
        )


if __name__ == "__main__":
    main()
