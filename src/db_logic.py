"""module responsible for writing and getting data"""

import sqlite3
from datetime import date, timedelta


class DBHandler:
    """class responsible for database operations"""
    table_name = "my_database.db"
    basic_db = """
            CREATE TABLE IF NOT EXISTS Activities (
            name TEXT NOT NULL,
            length REAL NOT NULL,
            date TEXT NOT NULL
            )
            """

    def __init__(self):
        self.connection = sqlite3.connect(self.table_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.basic_db)

    def add_activity(self, name, length):
        """adds activity to database"""
        current_date = date.today()
        self.cursor.execute(
            f"INSERT INTO Activities VALUES ('{name}', '{length}','{current_date}')"
        )
        self.connection.commit()

    def get_all(self):
        """gets all the containing data from the database"""
        self.cursor.execute("SELECT * FROM Activities")
        return self.cursor.fetchall()

    def get_by_activity(self, activity: str):
        """gets all the data base on the activity name"""
        self.cursor.execute(
            "SELECT * FROM Activities WHERE name=?", (activity.lower(),)
        )
        return self.cursor.fetchall()

    def get_by_date(self, user_date: str):
        """gets all the data based on the date"""
        self.cursor.execute("SELECT * FROM Activities WHERE date =?", (user_date,))
        return self.cursor.fetchall()

    def get_specific_period(self, start_date: str, finish_date: str):
        """gets all the data based on the period between 2 dates"""
        self.cursor.execute(
            "SELECT * FROM Activities WHERE date >=? AND date <=?",
            (start_date, finish_date),
        )
        return self.cursor.fetchall()

    def get_last_week(self):
        """gets all the data form the last week (current data minus 7 days)"""
        current_date = date.today()
        week_ago_date = current_date - timedelta(days=7)
        return self.get_specific_period(str(week_ago_date), str(current_date))
