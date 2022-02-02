import time
import asyncio
import json
from dataclasses import dataclass


@dataclass
class Loader:
    settings: dict
    phase_list: list
    n_phases: int
    n_rounds: list
    round_timers: list

    def __innit__(self):
        self.settings = json.load('settings.json')

    def split_settings(self):
        self.phase_list = self.settings['phase_list']
        self.n_phases = self.settings['#phases']
        for i in self.n_phases:
            self.n_rounds.append(self.settings['#rounds'][i])
        for i in self.n_phases:
            self.round_timers.append(self.settings['round_timers'][i])

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
