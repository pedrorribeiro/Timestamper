import time
import asyncio
from dataclasses import dataclass


@dataclass
class TimeManagement:
    start: float

    def __init__(self):
        self.start = time.time()

    def get_time(self):
        current_time = time.time()
        fixed_time = current_time - self.start
        return fixed_time


@dataclass
class Session(TimeManagement):
    allowed_phases: list
    phase: str
    round: int = 0

    def __init__(self):
        super().__init__()
        self.allowed_phases =
