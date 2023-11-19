import datetime
import logging

logger = logging.getLogger(__name__)


class InvalidReminderDate(Exception):
    pass


async def validate_text(text: str) -> None:
    """Validate the reminder text.

    Args:
        text (str): the text provided by the user in the reminder command.

    Raises:
        ValueError: Use of codeblocks in the reminder message.
        ValueError: Too long reminder message.
    """

    if "```" in text:
        raise ValueError("Nice try! but you can't use code blocks in your reminder message.")

    if len(text) > 100:
        raise ValueError("Reminder message is too long. Please keep it under 100 characters.")


def get_date(target_date: str) -> datetime.datetime:
    try:
        reminder_dt: datetime.datetime = datetime.datetime.strptime(target_date, "%Y-%m-%d %H:%M")
    except ValueError:
        raise ValueError("Invalid date format. Please use YYYY-mm-DD HH:MM")

    return reminder_dt
