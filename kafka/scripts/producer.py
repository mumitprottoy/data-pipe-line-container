import requests
import json
import time
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError


# configs
FETCH_INTERVAL = 30  # seconds
KAFKA_BOOTSTRAP_SERVERS = ['kafka:9092']
ENCODING = 'utf-8'


# message loggers
log_fetch_init_msg = lambda endpoint_name: print(f"📥 Fetching from {endpoint_name}...")
log_interval_msg = lambda interval=FETCH_INTERVAL: print(f"⏱️ Waiting {interval} seconds...")
log_data_sending_success_msg = lambda endpoint_name, topic: print(f"📤 Sent data from {endpoint_name} → Kafka topic [{topic}]")
log_topic_creation_msg = lambda new_topics: print(f"✅ Created topics: {[t.name for t in new_topics]}")
log_fetching_error_msg = lambda endpoint_name, e: print(f"❌ Error fetching {endpoint_name}: {e}")
log_graceful_bye = lambda: print("\n👋 Goodbye! Script stopped by Keyboard interruption. Fetching stopped.")

# API endpoints
api_endpoints = {
    "initial-points": "https://datae.edtechops.xyz/api/initial-points/",
    "events": "https://datae.edtechops.xyz/api/events/",
    "point-chunks": "https://datae.edtechops.xyz/api/point-chunks/",
    "users": "https://datae.edtechops.xyz/api/users/"
}


# API endpoint → Topic map
topics = {
    "initial-points": "initial-points-topic",
    "events": "events-topic",
    "point-chunks": "point-chunks-topic",
    "users": "users-topic"
}


def create_topics_if_needed():
    new_topics = list()
    admin = KafkaAdminClient(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    existing = admin.list_topics()

    for topic in topics.values():
        if topic not in existing:
            new_topics.append(NewTopic(name=topic, num_partitions=1, replication_factor=1))

    if new_topics:
        try:
            admin.create_topics(new_topics=new_topics)
            log_topic_creation_msg(new_topics)
        except TopicAlreadyExistsError: pass


producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode(ENCODING)
)


def fetch_and_send_to_kafka(endpoint_name, url, topic):
    log_fetch_init_msg(endpoint_name)
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list):
            for item in data:
                producer.send(topic, value=item)
        else: producer.send(topic, value=data)
        log_data_sending_success_msg(endpoint_name, topic)
    except requests.exceptions.RequestException as e: log_fetching_error_msg(endpoint_name, e)


def main():
    try:
        create_topics_if_needed()
        while True:
            for endpoint, url in api_endpoints.items():
                fetch_and_send_to_kafka(endpoint, url, topics[endpoint])
            producer.flush()
            log_interval_msg()
            time.sleep(FETCH_INTERVAL)
    except KeyboardInterrupt: log_graceful_bye()

if __name__ == "__main__":
    main()
