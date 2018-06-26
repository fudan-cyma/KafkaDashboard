from pyspark.streaming.kafka import KafkaUtils
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
import sys
import json

sc = SparkContext.getOrCreate()
sc.stop()
sc = SparkContext(appName = "PythonStreamingReciever")
ssc = StreamingContext(sc, 5)

kafkaStream = KafkaUtils.createStream(ssc, 'localhost:2181', 'spark-streaming',  {'province':1})
lines = kafkaStream.map(lambda x:x[1])
counts = lines.flatMap(lambda line:line.split(" ")).map(lambda word:(word,1)).reduceByKey(lambda a,b:a+b)
counts.pprint()

from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers = 'localhost:9092')


def process(rdd):
    print(rdd)
    message = json.dumps(rdd.map(lambda x:[str(x[0]),str(x[1])]).collect())

    producer.send('result',  message.encode('utf-8'))

counts.foreachRDD(process)
ssc.start()

ssc.awaitTermination()

