#    Spark
import json
import os

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

os.environ[
    "PYSPARK_SUBMIT_ARGS"
] = "--packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.4.5 pyspark-shell"


if __name__ == "__main__":

    sc = SparkContext(master="spark://localhost:7077", appName="test")
    ssc = StreamingContext(sc, 10)

    kvs = KafkaUtils.createStream(ssc, "zookeeper:2181", "test-group", {"example": 1})

    parsed = kvs.map(lambda v: json.loads(v[1]))
    parsed.count().map(lambda x: "Records in this batch: %s" % x).pprint()

    ssc.start()
    ssc.awaitTermination()
