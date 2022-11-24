import requests
from re import sub
import sys
import logging

URL = "https://app-media.noloco.app/noloco/dublin-bikes.json"

logger = logging.getLogger(__name__)

def get_data(url: str = URL) -> requests.Response:
    """Get data from a given endpoint
    For now if status is anything but 200, sys.exit(1)

    Args:
        url (str, optional): source url. Defaults to URL.

    Returns:
        requests.Response: complete Response obj
    """
    res = requests.get(url)
    if res.status_code != 200:
        logger.info(f'''
            "msg": "Something went wrong!"
            "status": {res.status_code}
            "response": {res.text}
            ''')
        sys.exit(1)
        
    return res


def format_key(key: str) -> str:
    """Format key to a camel case

    Args:
        key (str): key in string format, ie : 'sample-key'

    Returns:
        str: camel case key, ie: 'sampleKey'
    """
    _key = sub(r"(_|-|\(|\))+", " ", key).title().replace(" ", "")
    return "".join([_key[0].lower(), _key[1:]])
