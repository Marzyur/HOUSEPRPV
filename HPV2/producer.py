from kafka import KafkaProducer
import csv
import time

# Kafka connection settings
kafka_bootstrap_servers = 'localhost:9092'
kafka_topic = 'my_topic'

# Create Kafka producer
producer = KafkaProducer(bootstrap_servers=kafka_bootstrap_servers)

# Read and send CSV data to Kafka
with open('test.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip header
    for row in reader:
        time.sleep(2)
        message = ','.join(row).encode('utf-8')
        producer.send(kafka_topic, value=message)
        # print(f'Sent: {message.decode()}')

# Close Kafka producer
producer.close()
