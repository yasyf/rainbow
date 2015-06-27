import datetime


def week_of_the_month(date: datetime.date):
    return (date.day() - 1) // 7 + 1
