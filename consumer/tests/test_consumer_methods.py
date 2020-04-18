import pytest
import requests_mock

from consumer.consumer import methods


@pytest.mark.parametrize(
    "date, expectation",
    [
        pytest.param("2019-01-10", "01/10/2019"),
        pytest.param("10-01-2019", "10/01/2019"),
        pytest.param("10-Jan-2019", "10/01/2019"),
    ],
)
def test_normalize_date(date, expectation):
    parsed_date = methods.normalize_date(date)

    assert parsed_date == expectation


@pytest.mark.parametrize(
    "name, expectation",
    [
        pytest.param("bEnjamin", "Benjamin"),
        pytest.param("benjamin", "Benjamin"),
        pytest.param("BENJAMIN", "Benjamin"),
    ],
)
def test_capitalize_input(name, expectation):
    parsed_input = methods.capitalize_input(name)

    assert parsed_input == expectation


@pytest.mark.parametrize(
    "email, expectation",
    [
        pytest.param("ben@iwpnd", "invalid"),
        pytest.param("ben@iwpnd.pw", "ben@iwpnd.pw"),
        pytest.param("beniwpnd.pw", "invalid"),
    ],
)
def test_validate_email(email, expectation):
    parsed_email = methods.validate_email(email)

    assert parsed_email == expectation


@pytest.mark.parametrize(
    "email, expectation",
    [
        pytest.param("ben@iwpnd", "invalid"),
        pytest.param("ben@iwpnd.pw", "iwpnd.pw"),
        pytest.param("beniwpnd.pw", "invalid"),
    ],
)
def test_validate_email_host(email, expectation):
    parsed_email = methods.get_host(email)

    assert parsed_email == expectation


@pytest.mark.parametrize(
    "ip, expectation",
    [
        pytest.param("1.1.1.1", "1.1.1.1"),
        pytest.param("1.1.1", "invalid"),
        pytest.param("256.1.1.1", "invalid"),
    ],
)
def test_validate_ip(ip, expectation):
    parsed_ip = methods.validate_ip(ip)

    assert parsed_ip == expectation


def test_update_monitor_counter(monkeypatch):
    with requests_mock.Mocker() as m:
        m.register_uri(
            "POST",
            "https://localhost:8501/update/consumer",
            json={
                "incremented_by": 1,
                "current_counter": 1,
                "status": "HTTP_201_CREATED",
                "timestamp_utc": "2020-04-17T09:43:42.370074",
            },
        )

        response = methods.update_monitor_counter(
            monitor_url="https://localhost:8501/update/consumer", increment_by=1
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


def test_update_monitor_counter_empty(monkeypatch):
    with requests_mock.Mocker() as m:
        m.register_uri(
            "POST", "https://localhost:8501/update/consumer", status_code=422
        )

        response = methods.update_monitor_counter(
            monitor_url="https://localhost:8501/update/consumer", increment_by=0
        )

        assert not response
