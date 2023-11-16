import datetime


def get_remind_date(value: int, unit: str) -> datetime.datetime:
    """Converts arguments from /remindme to a datetime object.

    Args:
        value (int): The value of the reminder.
        unit (str): The unit of the reminder.

    Returns:
        datetime.datetime: The date of the reminder.
    """

    match unit:
        case "minutes":
            return datetime.datetime.utcnow() + datetime.timedelta(minutes=value)
        case "hours":
            return datetime.datetime.utcnow() + datetime.timedelta(hours=value)
        case "days":
            return datetime.datetime.utcnow() + datetime.timedelta(days=value)
        case _:
            return datetime.datetime.utcnow()
