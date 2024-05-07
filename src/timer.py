"""module, containig main timer logic"""

import time

from db_logic import DBHandler
from console_logic import Console
from stats import Stats


class Time:
    """Class, representing time period - basic"""

    def __init__(self, time: int):
        self.time = time

    def minute_count(self, minute):
        string = ""
        for seconds in range(59, 0, -1):
            zero = ""
            if seconds < 10:
                zero = "0"
            string = f"\r{minute}:{zero}{seconds}"
            yield string


class Work(Time):
    """Class, representing time period - work"""

    type = "work"
    intro = "The working part is about to start"
    head = "WORK"


class Relax(Time):
    """Class, representing time period - relax"""

    type = "relax"
    intro = "The relaxing part is about to start"
    head = "RELAX"


class BigBreak(Time):
    """Class, representing time period - bigbreak (comes after 4 period)"""

    type = "break"
    intro = "The big break is about to start"
    head = "HYPER RELAX"


class Timer:
    """Class, representing timer"""

    def __init__(
        self, input_time: str, activity="Basic", work_time=25, relax_time=5, bigbreak=15
    ):
        try:
            tmp_time = tuple([x for x in map(int, input_time.split(":"))])  # validation
            self.input_time = tmp_time
        except ValueError as e:
            raise ValueError(
                "make sure your input fits this template: {hours}:{minutes}"
            ) from e
        self.activity = activity
        self.work_time = work_time
        self.relax_time = relax_time
        self.bigbreak = bigbreak
        self._split_time()
        self.stats = Stats()
        self.console = Console()
        self.db = DBHandler()

    def _convert_time(self):
        whole_time = self.input_time[0] * 60 + self.input_time[1]
        return whole_time

    def __validate_change_settings(self, attr: str, input_str: str, result_str: str):
        success = False
        while not success:
            try:
                temp = input(input_str)
                if attr != "activity":
                    valid_temp = int(temp)
                    setattr(self, attr, valid_temp)
                    success = True
                else:
                    setattr(self, attr, temp)
                    success = True

                print(result_str.format(temp))
            except:
                print("Invalid input - try again")

    def change_settings(self):
        """starts the process of applying custom settings"""
        self.__validate_change_settings(
            "work_time",
            "Insert the desired work period length (in minutes): ",
            "work period length is {0} minutes",
        )
        self.__validate_change_settings(
            "relax_time",
            "Insert the desired relax period length (in minutes): ",
            "work relax length is {0} minutes",
        )
        self.__validate_change_settings(
            "bigbreak",
            "Insert the desired big break period length (in minutes): ",
            "big break length is {0} minutes",
        )
        self.__validate_change_settings(
            "activity", "Insert target activity:  ", "Your target activity is {0}"
        )

        self._split_time()

    def _split_time(self):
        mod_time = self._convert_time()
        poms_number = mod_time // (self.work_time + self.relax_time)
        poms_list = []
        for i in range(poms_number):
            poms_list.append(Work(self.work_time))
            poms_list.append(Relax(self.relax_time))
            if (i + 1) % 4 == 0:
                poms_list.append(BigBreak(self.bigbreak))
        self.pomodoros = poms_list
        return self.pomodoros

    def start(self):
        """starts the pomodoro timer"""
        if self._convert_time() > (self.work_time + self.relax_time):
            print(
                f"Your session will consist of {len([x for x in self.pomodoros if x.type == 'work'])} work periods and {len([x for x in self.pomodoros if x.type == 'relax'])} relax periods"
            )
            time.sleep(4)
            self.console.dynamic_output(self.pomodoros)
            self.db.add_activity(
                self.activity,
                self.work_time * len([x for x in self.pomodoros if x.type == "work"]),
            )
            print("\nCongratulations! your focus period is over")
        else:
            print(
                "Your overall focus preiod can't be smaller than its parts. Type longer period or modify parts with -m flag"
            )
