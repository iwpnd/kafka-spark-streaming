from pydantic import BaseModel
from pydantic import validator

from . import methods


class Record(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    gender: str
    ip_address: str
    date: str
    country: str

    _date_val = validator("date", allow_reuse=True)(methods.normalize_date)
    _capitalize_val = validator(
        "first_name", "last_name", "country", "gender", allow_reuse=True
    )(methods.capitalize_input)

    _email_val = validator("email", allow_reuse=True)(methods.validate_email)
    _ip_val = validator("ip_address", allow_reuse=True)(methods.validate_ip)