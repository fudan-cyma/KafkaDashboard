# KafkaDashboard

This is a dashboard example using Kafka and Spark Streaming to aggregate logs and update results.

## Prerequisites:
1. Spark: 2.2.1
2. Kafka: 1.1.0
3. Kafka-python: 1.4.2
4. Flask: 0.12.2
5. Flask-SocketIO: 2.9.6
6. Highcharts: 6.1.0

## Usage:
1. Clone the git repository,
	```
    git clone  https://github.com/fudan-cyma/KafkaDashboard.git
    cd KafkaDashboard
   ```
2. Run producer,
   ```
   python ./scripts/producer.py
   ```
3. Run streaming client,
   ```
	/usr/local/spark/bin/spark-submit --jars /usr/local/spark/jars/spark-streaming-kafka-0-8-assembly_2.11-2.2.1.jar 	./scripts/streaming.py 
   ```
4. Run the web server,
   ```
   python consumer.py
   ```
5. Enter the dashboard address,
   ```
   127.0.0.1:5000
   ```
   Scrrenshot:
   ![screenshot](https://github.com/fudan-cyma/KafkaDashboard/blob/master/Screenshot.png?raw=true)