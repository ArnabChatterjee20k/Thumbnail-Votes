from datetime import datetime


def generate_random_name():
    return str(int(round(datetime.now().timestamp(), 0)))
