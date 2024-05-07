"""module responsible for forming statistics"""

class Stats:
    """class resonsible for forming statistics"""

    def get_stats_activity(self, activity_list: list):
        """forms the database data based on activity and sorts it"""
        result_dict = {}
        for key, value, _ in activity_list:
            if key not in result_dict:
                result_dict[key] = value
            else:
                result_dict[key] += value
        tuples = list(result_dict.items())
        tuples.sort(key=lambda x: x[1], reverse=True)
        return tuples

    def get_stats_per_day(self, activity_list: list, detailed: bool):
        """forms the database data based on data and sorts it"""
        dates_dict = {}
        for key, value, date in activity_list:
            if date not in dates_dict:
                dates_dict[date] = []
            dates_dict[date].append((key, value, date))
        result_dict = {}
        if not detailed:
            for key, value in dates_dict.items():
                result_dict[key] = sum([x[1] for x in value])
        else:
            for key, value in dates_dict.items():
                result_dict[key] = self.get_stats_activity(value)

        return result_dict
