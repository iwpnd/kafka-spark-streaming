#    Spark
import json
import os

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

from .methods import get_gender_count
from .methods import get_least_represented_country
from .methods import get_most_represented_country
from .methods import update_monitor_counter
from .models import Record

os.environ[
    "PYSPARK_SUBMIT_ARGS"
] = "--packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.4.5 pyspark-shell"


def consume() -> None:

    sc = SparkContext(master="spark://localhost:7077", appName="kafka-record-consumer")
    ssc = StreamingContext(sc, 10)

    kafka_stream = KafkaUtils.createStream(
        ssc, "zookeeper:2181", "test-group", {"example": 1}
    )

    parsed = kafka_stream.map(lambda v: Record(**json.loads(v[1])).dict())

    # records in batch
    count_in_batch = parsed.count().map(lambda x: f"Records in this batch: {x}")
    count_in_batch.pprint()

    # count countries
    country_dstream = parsed.map(lambda record: record["country"])
    country_counts = country_dstream.countByValue()

    most_represented_country = get_most_represented_country(
        country_counts=country_counts, sc=sc
    )
    least_represented_country = get_least_represented_country(
        country_counts=country_counts, sc=sc
    )

    country_representation = most_represented_country.union(least_represented_country)
    country_representation.pprint()

    # count gender
    gender_dstream = parsed.map(lambda record: record["gender"])
    gender_counts = gender_dstream.countByValue()
    gender_distribution = get_gender_count(gender_counts=gender_counts, sc=sc)
    gender_distribution.pprint()

    # monitoring
    monitor_count = parsed.count().map(
        lambda x: update_monitor_counter(
            monitor_url="http://monitor:8501/update/consumer", increment_by=int(x)
        )
    )
    monitor_count.pprint()

    ssc.start()
    ssc.awaitTermination()
