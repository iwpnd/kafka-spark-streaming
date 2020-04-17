import pytest

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
