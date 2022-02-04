import time
import asyncio
import json
import os.path
from datetime import date
from dataclasses import dataclass, field


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
        self.n_rounds = list(map(str, input('input list with number \n'
                                            'of rounds in each phase: "element 1" "element 2" etc. \n').strip().split()))[
                        :n]
        self.round_timers = list(map(int, input('input list with round timers in each phase: \n'
                                                ' element 1 element 2 etc. \n'
                                                'if round does not have a timer input 5985. \n').strip().split()))[:n]

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

    def mak_object(self):
        with open('settings.json', 'r') as file:
            self.settings = json.load(file)

    def split_settings(self):
        self.phase_list = self.settings['phase_list']
        self.n_phases = self.settings['#phases']
        for i in range(1, len(self.phase_list)):
            self.n_rounds.append(self.settings['#rounds'][int(i)])
        for i in range(1, len(self.phase_list)):
            self.round_timers.append(self.settings['round_timers'][i])


@dataclass
class TimeManagement:
    start: float

    def mek_object(self):
        self.start = time.time()

    def get_time(self):
        current_time = time.time()
        fixed_time = current_time - self.start
        return fixed_time

    def time_reset(self):
        self.start = time.time()


@dataclass
class Session:
    allowed_phases: list
    first_phase: str
    phase: str
    n_rounds: list
    phase_n: int = 1
    round: int = 1

    def make_object(self):
        loader = Loader({}, [], 1, [], [])
        loader.mak_object()
        loader.split_settings()
        self.allowed_phases = loader.phase_list
        self.n_rounds = loader.n_rounds
        self.first_phase = self.allowed_phases[1]
        self.phase = self.first_phase

    def phase_n_plus_one(self):
        self.phase_n = self.phase_n + 1

    def next_phase(self):
        self.phase = self.allowed_phases[self.phase_n]
        self.round = 1

    def next_round(self):
        self.round = self.round + 1



@dataclass
class Manager:
    subject: dict
    sub: int
    td: str
    session: Session = Session([], '', '', [], 1, 1)
    timer: TimeManagement = TimeManagement(1.1)

    def make_dict(self):
        self.session.make_object()
        today = date.today()
        self.subject = {
            'subject': input('Insert Subject ID'),
            'Date': today.strftime("%d/%m/%Y")
            'Timestamp': {
            }
        }
        self.sub = self.subject['subject']
        self.td = self.subject['Date']
        filename = f'{self.sub}_{self.td}.json'
        path = f'.//{filename}'
        if os.path.isfile(path):
            with open(filename, 'r') as check:
                data = json.load(check)
            if 'subject' in data:
                answer = int(input('A previous session with this subject and this date was detected. '
                                'Would you like to restart (1) or continue(2) the session?\n'))
                if answer == 1:
                    with open(filename, 'w') as file:
                        json.dump(self.subject, file)
                    print(f'The protocol will restart')
                elif answer == 2:
                    with open('current.txt', 'r') as current:
                        phase = json.load(current)
                    self.session.phase = phase['phase']
                    self.session.round = phase['round']
            else:
                with open(filename, 'w') as file:
                    json.dump(self.subject, file)

    def fill_dict(self):
        with open(f'{self.sub}_{self.td}.json', 'r+') as file:
            self.subject = json.load(file)
        phase = self.session.phase
        if phase in self.subject['Timestamp']:
            self.subject['Timestamp'][phase][self.session.round] = self.timer.get_time()
            with open(f'{self.sub}_{self.td}.json', 'w') as file:
                json.dump(self.subject, file)
        else:
            self.subject['Timestamp'][phase] = {self.session.round: self.timer.get_time()}
            with open(f'{self.sub}_{self.td}.json', 'w') as file:
                json.dump(self.subject, file)
        current_pr = {'phase': self.session.phase, 'round': self.session.round}
        with open('current.json', 'w') as current:
            json.dump(current_pr, current)
        print(f"{phase}, round {self.session.round}. \n")

    def start(self):
        self.make_dict()
        self.timer.mek_object()
        self.fill_dict()
        current = f'{self.session.phase}: {self.session.round}'
        print(current)

    def new_phase(self):
        self.timer.mek_object()
        self.session.next_phase()
        self.fill_dict()

    def end_phase(self):
        with open(f'{self.sub}_{self.td}.json', 'r+') as file:
            self.subject = json.load(file)
        self.subject['Timestamp'][self.session.phase][self.session.round] = self.timer.get_time()
        with open(f'{self.sub}_{self.td}.json', 'w') as file:
            json.dump(self.subject, file)

    def new_round(self):
        self.session.next_round()
        self.fill_dict()

    def end(self):
        with open(f'{self.sub}_{self.td}.json', r+) as file:
            self.subject = json.load(file)
        self.subject['Timestamp']['end'] = self.timer.get_time()
        with open(f'{self.sub}_{self.td}.json', 'w') as file:
            json.dump(self.subject, file)
        print("The process has ended. Please verify the file's integrity. \n")
