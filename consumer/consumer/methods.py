import json
import re

import requests
from dateutil import parser
from pyspark import SparkContext
from pyspark.rdd import RDD


def normalize_date(date: str) -> str:
    """ normalize different date inputs (dayfirst!)
        to %d/%m/%Y

        Arguments:
            date (str): date to normalize

        Returns:
            str
    """
    parsed_date = parser.parse(date, dayfirst=True)

    return parsed_date.strftime("%d/%m/%Y")


def capitalize_input(input: str) -> str:
    """ capitalize an input str

        Arguments:
            input (str): input to capitalize

        Returns:
            str
    """
    parsed_input = input.capitalize()

    return parsed_input


def validate_email(email: str) -> str:
    """ validate an input email address

        Arguments:
            email (str): email to validate

        Returns:
            email or invalid (str)
    """
    if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
        email = "invalid"

    return email


def validate_ip(ip_address: str) -> str:
    """ validate an input ip_address

        Arguments:
            ip_address (str): ip_address to validate

        Returns:
            ip_address or invalid (str)
    """
    if not re.match(
        r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
        ip_address,
    ):
        ip_address = "invalid"

    return ip_address


def get_host(email: str) -> str:
    """ Get host from email

        Arguments:
            email (str): email to get host from

        Returns:
            str
    """
    try:
        host = re.findall(r"@(.*)$", email)[0]

        if "." not in host:
            host = "invalid"

    except IndexError:
        host = "invalid"

    return host


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


def get_least_represented_country(country_counts: RDD, sc: SparkContext) -> RDD:
    """ Get least represented country in batch

        Arguments:
            country_counts (RDD): rdd with country counts
            sc (SparkContext): SparkContext

        Returns:
            RDD
    """
    country_counts_sorted_asc = country_counts.transform(
        (lambda rdd: rdd.sortBy(lambda x: (x[1])))
    )
    least_represented_country = country_counts_sorted_asc.transform(
        lambda rdd: sc.parallelize(rdd.take(1))
    )
    least_represented_country = least_represented_country.map(
        lambda x: f"Least represented country in batch: {x[0]} ({x[1]})"
    )

    return least_represented_country


def get_most_represented_country(country_counts: RDD, sc: SparkContext) -> RDD:
    """ Get most represented country in batch

        Arguments:
            country_counts (RDD): rdd with country counts
            sc (SparkContext): SparkContext

        Returns:
            RDD
    """

    country_counts_sorted_desc = country_counts.transform(
        (lambda rdd: rdd.sortBy(lambda x: (-x[1])))
    )
    most_represented_country = country_counts_sorted_desc.transform(
        lambda rdd: sc.parallelize(rdd.take(1))
    )
    most_represented_country = most_represented_country.map(
        lambda x: f"Most represented country in batch: {x[0]} ({x[1]})"
    )

    return most_represented_country


def get_gender_count(gender_counts: RDD, sc: SparkContext) -> RDD:
    """ Get gender distribution in current batch

        Arguments:
            gender_counts (RDD): rdd with gender counts
            sc (SparkContext): SparkContext

        Returns:
            RDD
    """
    gender_distribution = gender_counts.transform(
        lambda rdd: rdd.sortBy(lambda x: -x[1])
    ).map(lambda x: f"{x[0]}'s this batch:\t{x[1]}")

    return gender_distribution
