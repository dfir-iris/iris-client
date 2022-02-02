import datetime
from random import randrange


def random_date():
    d1 = datetime.datetime.strptime('1/1/2008 1:30 PM', '%m/%d/%Y %I:%M %p')
    d2 = datetime.datetime.strptime('1/1/2022 4:50 AM', '%m/%d/%Y %I:%M %p')
    delta = d2 - d1
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return d1 + datetime.timedelta(seconds=random_second)