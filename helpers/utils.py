
from datetime import datetime
import re


def format_datetime(datetime_obj: datetime, format_pattern="%Y-%m-%d"):
    """Format datetime object and return formatted date

    Args:
        datetime_obj (datetime): datetime Object
        format_pattern (str, optional): Format pattern to be applied. Defaults to "%Y-%m-%d".

    Returns:
        str: Formatted datetime string
    """
    return datetime_obj.strftime(format_pattern)


def parse_datetime(datetime_str: str, format_pattern="%Y-%m-%d"):
    """Parse datetime str and return datetime_object

    Args:
        datetime_obj (datetime): datetime Object
        format_pattern (str, optional): Format pattern to be applied. Defaults to "%Y-%m-%d".

    Returns:
        datetimestr: datetime object
    """
    return datetime.strptime(datetime_str, format_pattern)


def get_number_from_text(text):
    """Get only Number from text

    Args:
        text (str): Text String

    Returns:
        int: Number from text 
    """    
    return int(re.sub("[^0-9]", "", text))
