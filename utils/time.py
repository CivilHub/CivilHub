from datetime import timedelta
from random import randint


def random_date(start, end):
    return start + timedelta(
        seconds=randint(0, int((end - start).total_seconds())))
