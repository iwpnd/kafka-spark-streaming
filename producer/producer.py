import json
from typing import Generator

import click
from pykafka import KafkaClient
from pykafka.exceptions import LeaderNotAvailable
from pykafka.exceptions import SocketDisconnectedError


def lazy_load_json(path: str) -> Generator:
    """
    """

    with open(path, "r") as file:
        for line in file:
            if line.startswith("[") and line.endswith(",\n"):
                line = json.loads(line[1:-2])
            elif line.endswith(",\n"):
                line = json.loads(line[:-2])
            elif line.endswith("]"):
                line = json.loads(line[:-1])

            yield line


@click.command()
@click.option("--topic", default="example", help="topic to produce messages to")
@click.option(
    "--kafkahost", default="localhost:9092", help="kafkahost to produce messages to"
)
@click.option("--file", default="MOCK_DATA.json", help="json file")
def produce(topic: str, kafkahost: str, file: str):
    client = KafkaClient(hosts=kafkahost)
    topic = client.topics[topic]
    producer = topic.get_producer()

    for record in lazy_load_json(file):
        try:
            producer.produce(json.dumps(record).encode("ascii"))
        except (SocketDisconnectedError, LeaderNotAvailable) as e:
            producer = topic.get_producer()
            producer.stop()
            producer.start()
            producer.produce(json.dumps(record).encode("ascii"))


if __name__ == "__main__":
    produce()
