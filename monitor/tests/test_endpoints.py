import json

import pytest


def test_counter_producer_success(test_app):

    test_payload = {"increment_by": 1}

    response = test_app.post("/update/producer", data=json.dumps(test_payload))

    assert response.status_code == 201
    assert all(
        [
            key in response.json()
            for key in ["incremented_by", "current_counter", "status", "timestamp_utc"]
        ]
    )
    assert response.json()["status"] == "HTTP_201_CREATED"
    assert response.json()["current_counter"] == 1


@pytest.mark.parametrize(
    "payload, expectation",
    [
        pytest.param({"increment_by": "String"}, 422),
        pytest.param({"increment_by": 0}, 422),
    ],
)
def test_counter_producer_fails(payload, expectation, test_app):

    response = test_app.post("/update/producer", data=json.dumps(payload))

    assert response.status_code == expectation


def test_counter_consumer_success(test_app):

    test_payload = {"increment_by": 1}

    response = test_app.post("/update/consumer", data=json.dumps(test_payload))

    assert response.status_code == 201
    assert all(
        [
            key in response.json()
            for key in ["incremented_by", "current_counter", "status", "timestamp_utc"]
        ]
    )
    assert response.json()["status"] == "HTTP_201_CREATED"
    assert response.json()["current_counter"] == 1


@pytest.mark.parametrize(
    "payload, expectation",
    [
        pytest.param({"increment_by": "String"}, 422),
        pytest.param({"increment_by": 0}, 422),
    ],
)
def test_counter_consumer_fails(payload, expectation, test_app):

    response = test_app.post("/update/consumer", data=json.dumps(payload))

    assert response.status_code == expectation


def test_metrics(test_app):
    response = test_app.get("/metrics")

    assert response.status_code == 200
    assert response.json()
    assert all(
        [
            key in response.json()
            for key in ["produced_records", "consumed_records", "timestamp_utc"]
        ]
    )
