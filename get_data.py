from common import format_key
import operator
from typing import Generator

ops = {
    "gt": operator.gt,
    "lt": operator.lt,
    "eq": operator.eq,
}


def format_keys(data: list) -> list:
    """Format data keys, replace with camel case format

    Args:
        data (list): raw data

    Returns:
        list: formatted data
    """
    formatted_data = []
    for i in data.json():
        a = {}
        for key, val in i.items():
            a[format_key(key)] = val
        formatted_data.append(a)
    return formatted_data


def get_filtered_data(data: dict, query: dict) -> Generator:
    """Return filtered data.

    Args:
        data (dict): data dict
        query (dict): query dict

    Yields:
        Generator: data row
    """
    for field_name in query.keys():
        if field_name not in data:
            continue
        for query_operator, value in query[field_name].items():
            if query_operator == "gt" and operator.gt(data.get(field_name), value):
                yield data
            elif query_operator == "lt" and operator.lt(data.get(field_name), value):
                yield data
            elif query_operator == "eq" and operator.eq(data.get(field_name), value):
                yield data
