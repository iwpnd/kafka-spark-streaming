import re

from dateutil import parser


def normalize_date(date: str) -> str:
    parsed_date = parser.parse(date, dayfirst=True)

    return parsed_date.strftime("%d/%m/%Y")


def capitalize_input(input: str) -> str:
    parsed_input = input.capitalize()

    return parsed_input


def validate_email(email: str) -> str:
    if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
        email = "invalid"

    return email


def validate_ip(ip_address: str) -> str:
    if not re.match(
        r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
        ip_address,
    ):
        ip_address = "invalid"

    return ip_address
