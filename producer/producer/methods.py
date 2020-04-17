import json
from typing import Generator

import requests


def lazy_load_json(path: str) -> Generator:
    """ Lazy load MOCK_DATA.json

        Lazy load MOCK_DATA.json line by line and parsing to string to json

        Arguments:
            path (str): path to MOCK_DATA.json

        Returns:
            Generator
    """

    with open(path, "r") as file:
        for line in file:
            if line.startswith("[") and line.endswith(",\n"):
                line = json.loads(line[1:-2])
            elif line.endswith(",\n"):
                line = json.loads(line[:-2])
            elif line.endswith("]\n"):
                line = json.loads(line[:-2])

            yield line


def update_monitor_counter(monitor_url: str, increment_by: int) -> dict:
    """ Update monitor counter

        Post increment_by to monitor_url and update respective counter

        Arguments:
            monitor_url (str): monitor endpoint url
            increment_by (int): increment counter by value

        Returns:
            dict
    """

    if increment_by > 0:

        payload = {"increment_by": increment_by}
        response = requests.post(monitor_url, data=json.dumps(payload))

        return response.json()
