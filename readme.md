# kafka-spark-streaming

Push records from .json file to an Apache Kafka topic. Consume said Apache Kafka topics messages with Apache Spark Streaming.

## Installation

### prerequisites

If you're on MacOS set an environment variable like:
```bash
export DOCKER_KAFKA_HOST=$(ipconfig getifaddr en0)
```
that is afterwards used in `docker-compose.yml` to identify the `KAFKA_ADVERTISED_HOST_NAME`. Some similar workaround has to exist for Windows users.
For linux I assume you can just set it to `localhost` if you're only running on Kafka node. See [github.com/wurstmeister/kafka-docker/wiki/Connectivity](https://github.com/wurstmeister/kafka-docker/wiki/Connectivity).

```bash
docker-compose up -d
```

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
pytest --cov=producer --cov=consumer --cov=monitor -v
```

or

```bash
make test
```

to test the installation and all attached services.

#### bring up all necessary services

```bash
docker-compose up -d
```

Will bring up all services such as Zookeeper, Apache Kafka, an Apache Spark Master and one Apache Spark worker with 1 Core / 2048MB of memory.

#### follow the consumer output

```bash
docker-compose logs --follow consumer
```

This will let you check the consumer logs for incoming batches from Kafka. It will print some generic metrics such as:
- records per batch
- most represented country in batch
- least represented country in batch
- top3 email hosts in batch
- gender distribution in batch

#### start the producer

```bash
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

#### monitoring

You can follow producer and consumed messages on `http://localhost:8501/metrics`.