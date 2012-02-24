from re import match
from time import time as now


__UNITS = {
        's': 'second',
        'min': 'minute',
        'h': 'hour',
        'd': 'day',
        'w': 'week',
        'm': 'month',
        'y': 'year',
    }


#TODO config this shit
def get_times():
    ret = (
        ('', 'Time'),
        ('10min', '10 minutes'),
        ('30min', '30 minutes'),
        ('1h', '1 hour'),
        ('2h', '2 hours'),
        ('4h', '4 hours'),
        ('12h', '12 hours'),
        ('1d', '1 day'),
        ('2d', '2 days'),
        ('1w', '1 week'),
        ('1m', '1 month'),
    )
    return ret


#TODO config this shit
def get_time_offsets():
    ret = (
        ('', 'Time'),
        ('10min', '10 minutes'),
        ('30min', '30 minutes'),
        ('1h', '1 hour'),
        ('2h', '2 hours'),
        ('4h', '4 hours'),
        ('12h', '12 hours'),
        ('1d', '1 day'),
        ('2d', '2 days'),
        ('1w', '1 week'),
        ('1m', '1 month'),
    )
    return ret


def display_time(time):
    t, u = parse_time(time)
    return t + ' ' + u + 's' if (t > 1)  else ''


def parse_time(time):
    time = str(time)
    if time[-1] == 's':
        time = time[:-1]
    m = match(r"(\d+)([a-z]+)", time.lower()).groups()
    return (m[0], __UNITS[m[1]])


def epoch_seconds_for_time(time):
    t, u = parse_time(time)

    unit_seconds = 0
    if u == 'h':
        unit_seconds = 3600
    if u == 'd':
        unit_seconds = 86400
    if u == 'w':
        unit_seconds = 86400 * 7
    if u == 'm':
        unit_seconds = 86400 * 30
    if u == 'y':
        unit_seconds = 86400 * 365
    return now() - (t * unit_seconds)
