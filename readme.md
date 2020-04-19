<p align="left">
<a href="https://github.com/iwpnd/kafka-spark-streaming/actions" target="_blank">
    <img src="https://github.com/iwpnd/kafka-spark-streaming/workflows/build/badge.svg?branch=master" alt="Build Status">
</a>
</p>

# kafka-spark-streaming

Push records from .json file to an Apache Kafka topic. Consume said Apache Kafka topics messages with Apache Spark Streaming.

## Installation

### prerequisites

If you're on MacOS set an environment variable like:
```bash
export DOCKER_KAFKA_HOST=$(ipconfig getifaddr en0)
```
or add `DOCKER_KAFKA_HOST` to `~/.zshenv` and `source ~/.zshenv`.

`DOCKER_KAFKA_HOST` is used in `docker-compose.yml` to identify the `KAFKA_ADVERTISED_HOST_NAME`. Some similar workaround has to exist for Windows users that also rely on a VM to run Docker.
For linux I assume you can just set it to `localhost` if you're only running on Kafka node. See [github.com/wurstmeister/kafka-docker/wiki/Connectivity](https://github.com/wurstmeister/kafka-docker/wiki/Connectivity).

### installation / usage

clone the repository and install the repository:
```bash
git clone https://github.com/iwpnd/kafka-spark-streaming.git
cd kafka-spark-streaming
make install
```

This will create a `venv` dir with a virtual environment inside of `kafka-spark-streaming` dir.


#### testing
```bash
# source venv/bin/activate
pytest . -v
```

or

```bash
make test
```

to test the installation and all the attached services.

#### bring up all the the necessary services

```bash
docker-compose up -d
```

Will bring up all services such as Zookeeper, Apache Kafka, an Apache Spark Master and one Apache Spark worker.
You can check your:
Apache Spark cluster metrics at: `http://localhost:8088/`
Monitor docs at: `http://localhost:8501/docs`

#### check logs of consumer service

```bash
docker-compose logs --follow consumer
```

This will let you check the consumer logs for incoming batches from Kafka (interval=10seconds). It will print some generic metrics such as:
- number of records per batch
- most represented country in batch
- least represented country in batch
- top3 email hosts in batch
- gender distribution in batch
- push counts to monitor at `http://localhost:8501/update/consumer`

**NOTE**: There are 5 (unless you scale your workers) services running to perform all this. You might not see the immediate output in `docker-compose logs --follow consumer` depending on your machine. You can follow the process by refreshing `http://localhost:8501/metrics`. Once the logs have caught up, you can check the metrics of every batch.

#### start the producer

```bash
# source venv/bin/activate
python producer/main.py
```

optional:
```bash
Usage: main.py [OPTIONS]

Options:
  --topic TEXT        topic to produce messages to
  --kafkahost TEXT    kafkahost to produce messages to
  --monitorhost TEXT  monitor url to push counts to
  --file TEXT         json file
  --help              Show this message and exit.
```

This will print something along the lines of:
```bash
Producing records from 'producer/dataset/MOCK_DATA.json' to localhost:9092/example
```
and in the background will push the counts of produced messages to `http://localhost:8501/update/producer`.

#### monitoring

You can follow producer and consumed messages on `http://localhost:8501/metrics`.
