import pytest

from consumer.consumer.models import Record


@pytest.mark.parametrize(
    "data, expectation",
    [
        pytest.param(
            {
                "id": 2,
                "first_name": "Loy",
                "last_name": "drain",
                "email": "ldrain1@earthlink",
                "gender": "male",
                "ip_address": "218.176.26",
                "date": "23.02.2019",
                "country": "Philippines",
            },
            {
                "id": 2,
                "first_name": "Loy",
                "last_name": "Drain",
                "email": "invalid",
                "email_host": "invalid",
                "gender": "Male",
                "ip_address": "invalid",
                "date": "23/02/2019",
                "country": "Philippines",
            },
        )
    ],
)
def test_model_record(data, expectation):
    record = Record(**data)

    assert record.dict() == expectation
