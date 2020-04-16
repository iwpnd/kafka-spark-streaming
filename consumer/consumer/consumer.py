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
    count_in_batch = (
        parsed.count().map(lambda x: "Records in this batch: %s" % x).pprint()
    )
    count_windowed = kafka_stream.countByWindow(30, 10).map(
        lambda x: ("Records total (30 seconds rolling count): %s" % x)
    )

    #
    country_dstream = parsed.map(lambda record: record["country"])
    country_counts = country_dstream.countByValue()
    country_counts_sorted = country_counts.transform(
        (lambda record: record.sortBy(lambda x: (-x[1])))
    )
    nlargest5_country_counts = country_counts_sorted.transform(
        lambda rdd: sc.parallelize(rdd.take(5))
    )
    nlargest5_country_counts.pprint()

    ssc.start()
    ssc.awaitTermination()
