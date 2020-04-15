import json
from typing import Generator


def lazy_load_json(path: str) -> Generator:
    """
    """

    with open(path, "r") as file:
        for line in file:
            if line.startswith("[") and line.endswith(",\n"):
                line = json.loads(line[1:-2])
            elif line.endswith(",\n"):
                line = json.loads(line[:-2])
            elif line.endswith("]"):
                line = json.loads(line[:-1])

            yield line
