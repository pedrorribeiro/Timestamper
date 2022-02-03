import time
import asyncio
import json
from dataclasses import dataclass


@dataclass
class Maker:
    setting_list: dict
    phase_list: list
    n_phases: int
    n_rounds: list
    round_timers: list

    def make_object(self):
        n = int(input('Input the number of phases'))
        self.phase_list = list(map(str, input('input phase list: "element 1" "element 2" etc.').strip().split()))[:n]
        self.n_phases = n
        self.n_rounds = list(map(str, input('input list with number '
                                            'of rounds in each phase: "element 1" "element 2" etc.').strip().split()))[
                        :n]
        self.round_timers = list(map(int, input('input list with round timers in each phase:'
                                                ' element 1 element 2 etc. '
                                                'if round does not have a timer input 5985').strip().split()))[:n]

    def dict_maker(self):
        self.setting_list = {
            'phase_list': self.phase_list,
            '#phases': self.n_phases,
            '#rounds': self.n_rounds,
            'round_timers': self.round_timers
        }

    def upload_settings(self):
        with open('settings.json', 'w') as json_file:
            json.dump(self.setting_list, json_file)


@dataclass
class Loader:
    settings: dict
    phase_list: list
    n_phases: int
    n_rounds: list
    round_timers: list

    def make_object(self):
        with open('setting.json', 'r') as file:
            self.settings = json.load(file)

    def split_settings(self):
        self.phase_list = self.settings['phase_list']
        self.n_phases = self.settings['#phases']
        for i in self.phase_list:
            self.n_rounds.append(self.settings['#rounds'][i])
        for i in self.phase_list:
            self.round_timers.append(self.settings['round_timers'][i])


@dataclass
class TimeManagement:
    start: float

    def make_object(self):
        self.start = time.time()

    def get_time(self):
        current_time = time.time()
        fixed_time = current_time - self.start
        return fixed_time

    def time_reset(self):
        self.start = time.time()


@dataclass
class Session(Loader):
    allowed_phases: list
    first_phase: 'str'
    phase: str
    phase_n: int = 1
    round: int = 1

    def make_object(self):
        super().__init__()
        self.allowed_phases = self.phase_list
        self.first_phase = self.allowed_phases[1]
        self.phase = self.first_phase

    def next_phase(self):
        self.phase = self.allowed_phases[self.phase_n]
        self.round = 1

    def next_round(self):
        if self.round + 1 <= self.n_rounds[self.phase_n]:
            self.round = self.round + 1
        else:
            self.next_phase()
