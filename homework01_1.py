from calendar import weekday
from datetime import datetime, timedelta
from collections import defaultdict


def get_birthdays_per_week(users):
    birthdays_by_weekday = defaultdict(list)

    today = datetime.today().date()

    for user in users:
        name = user["name"]
        birthday = user["birthday"].date()
        birthday_this_year = birthday.replace(year=today.year)

        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)

        delta_days = (birthday_this_year - today).days

        if delta_days < 7:
            birthday_weekday = (today + timedelta(days=delta_days)).strftime("%A")
            birthdays_by_weekday[birthday_weekday].append(name)

    for weekday, names in birthdays_by_weekday.items():

        if weekday != "Sunday":
            print(f"{weekday}: {', '.join(names)}")
        else:
            print(f"{'Monday'}: {', '.join(names)}")


users = [
    {"name": "Bill Gates", "birthday": datetime(1955, 2, 27)},
    {"name": "Gil Bates", "birthday": datetime(1956, 1, 22)},
    {"name": "John Smith", "birthday": datetime(1942, 2, 28)},
    {"name": "Joe Lam", "birthday": datetime(1966, 3, 3)},
    {"name": "Jan Koum", "birthday": datetime(1976, 2, 29)},
]

get_birthdays_per_week(users)
