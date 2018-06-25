import csv
import time
from kafka import KafkaProducer


producer = KafkaProducer(bootstrap_servers = 'localhost:9092')
csvfile = open("/home/chloe/data/user_log.csv", "r")
reader = csv.reader(csvfile)

for line in reader:
    province = line[10]
    if province == 'province':
        continue
    time.sleep(0.1)
    #print(line[10])
    producer.send('province', line[10].encode('utf8'))





