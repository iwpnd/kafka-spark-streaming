import json


def is_json(myjson):
    try:
        test = json.dumps(myjson)
        json.loads(test)
    except ValueError:
        return False
    return True
