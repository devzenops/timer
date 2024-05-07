"""module respnsible for CLI interaction"""

import sys
import time


class Console:

    def _move_cursor(self, vertical: int, horizontal: int):
        sys.stdout.write(f"\033[{vertical}A")

        for _ in range(horizontal):
            sys.stdout.write("\033[1000D")

    def dynamic_output(self, periods):
        """this method creates dynamic time bar and time countdown in console"""
        flag_float_minute = False
        length = 100
        final = ""
        reset = "\x1b[0m"
        summ = sum([x.time for x in periods])
        proportion = length / summ
        if proportion < 1:
            per_dig = 0
            one = 0
            while one < 1:
                one += proportion
                per_dig += 1
            flag_float_minute = True
        else:
            proportion = round(proportion)

        if not flag_float_minute:
            for period in periods:
                if period.type == "work":
                    final += "\x1b[1;41m"
                    for i in range(period.time - 1, -1, -1):
                        for string in period.minute_count(i):
                            print(final, reset, "\n", string, reset, end="")
                            self._move_cursor(1, 1)
                            time.sleep(1)
                        final += " " * proportion
                    final += "\x1b[0m|"
                elif period.type == "relax":
                    final += "\x1b[1;42m"
                    for i in range(period.time - 1, -1, -1):
                        for string in period.minute_count(i):
                            print(final, reset, "\n", string, reset, end="")
                            self._move_cursor(1, 1)
                            time.sleep(1)
                        final += " " * proportion
                    final += "\x1b[0m|"

        else:
            for period in periods:
                counter = 0
                if period.type == "work":
                    final += "\x1b[1;41m"
                    for i in range(period.time - 1, -1, -1):
                        counter += 1
                        for string in period.minute_count(i):
                            print(final, reset, "\n", string, reset, end="")
                            self._move_cursor(1, 1)
                            time.sleep(1)
                        if counter == per_dig:
                            final += " "
                            counter = 0
                    final += reset + "|"
                elif period.type == "relax":
                    final += "\x1b[1;42m"
                    for i in range(period.time - 1, -1, -1):
                        counter += 1
                        for string in period.minute_count(i):
                            print(final, reset, "\n", string, reset, end="")
                            self._move_cursor(1, 1)
                            time.sleep(1)
                        if counter == per_dig:
                            final += " "
                            counter = 0
                    final += reset + "|"

    def visualize_stats_activity(self, activity_list: list, period: str):
        """outputs activity based statistics to the console"""
        print(f"Your activity stats during {period} period")
        for (
            key,
            value,
        ) in activity_list:
            print(key, ":\t", f"{value} minutes")

    def visualize_stats_per_days(
        self, activity_dict: dict, period: str, detailed: bool
    ):
        """outputs data based statistics to the console"""

        print(activity_dict)
        if detailed:
            print(f"Here's your detailed stats during {period} period")
            for key, value in activity_dict.items():
                print(f"--------{key}---------")
                for day_key, day_value in value:
                    print("\t", day_key, ":\t", f"{day_value} minutes")

        else:
            print(f"Here's your  stats during {period} period")
            for key, value in activity_dict.items():
                print("\t", key, ":\t", f"{value} minutes")
