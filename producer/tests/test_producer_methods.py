import json
import types

import requests_mock

from .helpers import utils
from producer.producer import methods


def test_lazy_load_json_generator(mock_data_file):
    test = methods.lazy_load_json(mock_data_file)
    assert isinstance(test, types.GeneratorType)


def test_lazy_load_json_valid(mock_data_file):
    record = methods.lazy_load_json(mock_data_file)
    object1 = next(record)
    assert object1["test1"]
    assert utils.is_json(object1)
    object2 = next(record)
    assert object2["test2"]
    assert utils.is_json(object2)
    object3 = next(record)
    assert object3["test3"]
    assert utils.is_json(object3)


def test_update_monitor_counter(monkeypatch):
    with requests_mock.Mocker() as m:
        m.register_uri(
            "POST",
            "https://localhost:8501/update/producer",
            json={
                "incremented_by": 1,
                "current_counter": 1,
                "status": "HTTP_201_CREATED",
                "timestamp_utc": "2020-04-17T09:43:42.370074",
            },
        )

        response = methods.update_monitor_counter(
            monitor_url="https://localhost:8501/update/producer", increment_by=1
        )

        assert all(
            [
                key in response
                for key in [
                    "incremented_by",
                    "current_counter",
                    "status",
                    "timestamp_utc",
                ]
            ]
        )
