import sys
import time

from db_logic import DBHandler
from stats import Stats


class Console:

    def move_cursor(self, vertical: int, horizontal: int):
        sys.stdout.write(f"\033[{vertical}A")

        for _ in range(horizontal):
            sys.stdout.write(f"\033[1000D")

    def dynamic_output(self, periods):
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
                            self.move_cursor(1, 1)
                            time.sleep(1)
                        final += " " * proportion
                    final += "\x1b[0m|"
                elif period.type == "relax":
                    final += "\x1b[1;42m"
                    for i in range(period.time - 1, -1, -1):
                        for string in period.minute_count(i):
                            print(final, reset, "\n", string, reset, end="")
                            self.move_cursor(1, 1)
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
                            self.move_cursor(1, 1)
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
                            self.move_cursor(1, 1)
                            time.sleep(1)
                        if counter == per_dig:
                            final += " "
                            counter = 0
                    final += reset + "|"

    def visualize_stats_activity(self, activity_list: list, period: str):
        print(f"Your activity stats during {period} period")
        for (
            key,
            value,
        ) in activity_list:
            print(key, ":\t", f"{value} minutes")

    def visualize_stats_per_days(
        self, activity_dict: dict, period: str, detailed: bool
    ):

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


if __name__ == "__main__":

    test = Console()
    stats = Stats()
    db = DBHandler()
    test.visualize_stats_per_days(
        stats.get_stats_per_day(
            db.get_specific_period("2024-04-21", "2024-04-30"), detailed=True
        ),
        "lol",
        detailed=True,
    )
