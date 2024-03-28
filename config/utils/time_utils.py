import pytz


def convert_to_utc(local_time, user_timezone):
    """Конвертирует время из локального часового пояса пользователя в UTC."""
    naive_local_time = local_time.replace(tzinfo=None)
    user_tz = pytz.timezone(user_timezone)
    local_aware_time = user_tz.localize(naive_local_time)
    utc_time = local_aware_time.astimezone(pytz.utc)

    return utc_time


def convert_to_local_time(utc_time, user_timezone):
    """Конвертирует время из UTC в локальное пользователя"""
    user_tz = pytz.timezone(user_timezone)
    local_time = utc_time.astimezone(user_tz)
    return  local_time.replace(tzinfo=None)
