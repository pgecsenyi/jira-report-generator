SECS_IN_HOUR = 60 * 60


def secs_to_hours(value):
    return '{0:.1f}'.format(value / SECS_IN_HOUR)
