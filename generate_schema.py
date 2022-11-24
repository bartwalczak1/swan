from datetime import datetime

from typing import Any
from models import Field


from common import URL, get_data, format_key


def check_if_date(date_string: str) -> bool:
    """Check if date is an actual date

    Args:
        date_string (str): date time in string format

    Returns:
        bool: true if string is valid datetime
    """
    try:
        datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S")
        return True
    except ValueError:
        return False


def type_validator(data_key: str, data_value: Any) -> str:
    """Find data type from passed key/value

    Args:
        data_key (str): data key from json object
        data_value (Any): data value from json object

    Returns:
        str: common type
    """
    if "longitude" in data_key or "latitude" in data_key:
        return "FLOAT"
    elif data_value is None:
        if "date" in data_key.lower() or "time" in data_key.lower():
            return "DATE"
        else:
            return None
    elif isinstance(data_value, int):
        return "INTEGER"
    elif isinstance(data_value, bool):
        return "BOOLEAN"
    elif check_if_date(data_value):
        return "DATE"
    elif data_value.lower() == "true" or data_value.lower() == "false":
        return "BOOLEAN"
    elif isinstance(data_value, str):
        return "TEXT"
    elif isinstance(data_value, float):
        return "FLOAT"
    else:
        return "OPTION"


def get_schema():
    """Get schema from json."""
    schema = []
    res = get_data()
    for row in res.json():
        for key, val in row.items():
            formatted = format_key(key)
            validated_type = type_validator(key, val)
            field = Field(display=key, name=formatted, type=validated_type, options=[])
            schema.append(field.dict())
    return schema
