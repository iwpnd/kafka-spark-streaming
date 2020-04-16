#    Spark
import json
import os

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

from .models import Record

os.environ[
    "PYSPARK_SUBMIT_ARGS"
] = "--packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.4.5 pyspark-shell"


def consume():

    sc = SparkContext(master="spark://localhost:7077", appName="test")
    ssc = StreamingContext(sc, 10)

    kafka_stream = KafkaUtils.createStream(
        ssc, "zookeeper:2181", "test-group", {"example": 1}
    )

    parsed = kafka_stream.map(lambda v: Record(**json.loads(v[1])).dict())
    count_in_batch = parsed.count().map(lambda x: f"Records in this batch: {x}")

    country_dstream = parsed.map(lambda record: record["country"])
    country_counts = country_dstream.countByValue()

    country_counts_sorted_desc = country_counts.transform(
        (lambda record: record.sortBy(lambda x: (-x[1])))
    )
    most_represented_country = country_counts_sorted_desc.transform(
        lambda rdd: sc.parallelize(rdd.take(1))
    )
    most_represented_country = most_represented_country.map(
        lambda x: f"Most represented country in batch: {x[0]} ({x[1]})"
    )

    country_counts_sorted_asc = country_counts.transform(
        (lambda record: record.sortBy(lambda x: (x[1])))
    )
    least_represented_country = country_counts_sorted_asc.transform(
        lambda rdd: sc.parallelize(rdd.take(1))
    )
    least_represented_country = least_represented_country.map(
        lambda x: f"Least represented country in batch: {x[0]} ({x[1]})"
    )

    output = count_in_batch.union(most_represented_country)
    output = output.union(least_represented_country)
    output.pprint()

    ssc.start()
    ssc.awaitTermination()
