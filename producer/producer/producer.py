import json

import click
import requests
from pykafka import KafkaClient
from pykafka.exceptions import LeaderNotAvailable
from pykafka.exceptions import SocketDisconnectedError

from .methods import lazy_load_json
from .methods import update_monitor_counter


@click.command()
@click.option("--topic", default="example", help="topic to produce messages to")
@click.option(
    "--kafkahost", default="localhost:9092", help="kafkahost to produce messages to"
)
@click.option(
    "--monitorhost",
    default="http://localhost:8501/update/producer",
    help="monitor url to push counts to",
)
@click.option("--file", default="producer/dataset/MOCK_DATA.json", help="json file")
def produce(topic: str, kafkahost: str, monitorhost: str, file: str):
    click.echo(f"connecting to kafkahost")
    client = KafkaClient(hosts=kafkahost)
    click.echo(f"fetching target topic from kafkahost")
    target_topic = client.topics[topic]
    click.echo(f"setup producer")
    producer = target_topic.get_producer()
    records_produced = 0

    click.echo(f"Producing records from '{file}' to {kafkahost}/{topic}")

    for record in lazy_load_json(file):
        try:
            import time

            producer.produce(json.dumps(record).encode("ascii"))
            time.sleep(0.05)
            records_produced = records_produced + 1

        except (SocketDisconnectedError, LeaderNotAvailable) as e:
            producer = topic.get_producer()
            producer.stop()
            producer.start()
            producer.produce(json.dumps(record).encode("ascii"))

        update_monitor_counter(monitor_url=monitorhost, increment_by=1)

    click.echo(
        f"Produced {records_produced} records from '{file}' to {kafkahost}/{topic}"
    )


if __name__ == "__main__":
    produce()
