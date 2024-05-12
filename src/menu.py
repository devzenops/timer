"""Module providing user interaction"""

import re
import sys
import argparse


from .timer import Timer
from .console_logic import Console


console = Console()


def wait_yes_no_response() -> bool:
    """handles yes/no user inputs"""
    result = False
    answer = input().lower()
    while answer.lower() not in ["yes", "no", "not", "\n"]:
        print("please, type 'yes' or 'no'")
        answer = input().lower()

    if answer in ["no", "not"]:
        result = False
    else:
        result = True
    return result


def wait_valid_data():
    """handles data validation"""
    answer = input()
    while not re.match(r"\d{4}-\d{2}-\d{2}", answer):
        print("Your date is not valid, make sure you use YYYY-MM-DD format")
        answer = input()

    return answer


def start_menu():
    """describes the menu interaction logic"""
    parser = argparse.ArgumentParser(description="Pomodoro Timer")

    parser.add_argument("-r", "--run", action="store_true", help="Starts the timer")
    parser.add_argument(
        "input_time",
        nargs="?",
        default=None,
        help="A time period input in format {hours}:{minutes}",
    )
    parser.add_argument(
        "-m", "--modify", action="store_true", help="Starts the modified timer"
    )
    parser.add_argument(
        "-s",
        "--stats",
        choices=["last_week", "date", "period"],
        help="Displays the statistics",
    )
    parser.add_argument(
        "-sm",
        "--stats_mode",
        choices=["date", "activity"],
        help="Choose the parametrs to display data",
    )

    args = parser.parse_args()
    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])
    if args.run:
        success = False
        try:
            user_time = args.input_time
            new_timer = Timer(user_time)
            success = True
        except Exception:
            print(
                "Incorrect input - make sure your input fits this template: {hours}:{minutes}"
            )
        if args.modify and success:
            print(
                """Basic settings:
            
            -Work time : 25 minutes
            
            - Relax time: 5 minutes
            
            -BigBreak time : 15 minutes
            
            -Activity : Basic"""
            )
            print("do you want to change basic settings?[Yes/no]")
            response = wait_yes_no_response()
            if response:
                new_timer.change_settings()
        if success:
            new_timer.start()

    if args.stats == "last_week":
        new_timer = Timer("0:0")
        if args.stats_mode == "date":
            data = new_timer.db.get_last_week()
            console.visualize_stats_per_days(
                new_timer.stats.get_stats_per_day(data, detailed=True),
                "last week",
                detailed=True,
            )

        elif args.stats_mode == "activity":
            data = new_timer.db.get_last_week()
            console.visualize_stats_activity(
                new_timer.stats.get_stats_activity(data), "last week"
            )

        else:
            data = new_timer.db.get_last_week()
            console.visualize_stats_activity(
                new_timer.stats.get_stats_activity(data), "last week"
            )

    if args.stats == "date":
        new_timer = Timer("0:0")
        print("Insert the date in YYYY-MM-DD format")
        date = wait_valid_data()
        data = new_timer.db.get_by_date(date)
        console.visualize_stats_activity(new_timer.stats.get_stats_activity(data), date)

    if args.stats == "period":
        new_timer = Timer("0:0")
        print("Insert the start date in YYYY-MM-DD format")
        start_date = wait_valid_data()
        print("Insert the finish date in YYYY-MM-DD format")
        finish_date = wait_valid_data()
        concat_date = f"{start_date} --- {finish_date}"
        data = new_timer.db.get_specific_period(start_date, finish_date)

        if args.stats_mode == "date":
            console.visualize_stats_per_days(
                new_timer.stats.get_stats_per_day(data, detailed=True),
                concat_date,
                detailed=True,
            )
        elif args.stats_mode == "activity":
            console.visualize_stats_activity(
                new_timer.stats.get_stats_activity(data), concat_date
            )
        else:
            console.visualize_stats_activity(
                new_timer.stats.get_stats_activity(data), concat_date
            )

