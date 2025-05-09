import requests
import json
import time
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError

# Configuration
FETCH_INTERVAL = 10  # seconds
KAFKA_BOOTSTRAP_SERVERS = ['localhost:9092']

# API to Topic mapping
api_endpoints = {
    "initial-points": "https://datae.edtechops.xyz/api/initial-points/",
    "events": "https://datae.edtechops.xyz/api/events/",
    "point-chunks": "https://datae.edtechops.xyz/api/point-chunks/",
    "users": "https://datae.edtechops.xyz/api/users/"
}

topics = {
    "initial-points": "initial-points-topic",
    "events": "events-topic",
    "point-chunks": "point-chunks-topic",
    "users": "users-topic"
}

# Create Kafka topics if not exist
def create_topics_if_needed():
    admin = KafkaAdminClient(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    existing = admin.list_topics()

    new_topics = []
    for topic in topics.values():
        if topic not in existing:
            new_topics.append(NewTopic(name=topic, num_partitions=1, replication_factor=1))

    if new_topics:
        try:
            admin.create_topics(new_topics=new_topics)
            print(f"✅ Created topics: {[t.name for t in new_topics]}")
        except TopicAlreadyExistsError:
            print("⚠️ Topics already exist.")
    else:
        print("✅ All topics already exist.")

# Setup producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Fetch and send
def fetch_and_send_to_kafka(endpoint_name, url, topic):
    print(f"📥 Fetching from {endpoint_name}...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list):
            for item in data:
                producer.send(topic, value=item)
        else:
            producer.send(topic, value=data)

        print(f"📤 Sent data from {endpoint_name} → Kafka topic [{topic}]")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching {endpoint_name}: {e}")

# Main loop
def main():
    create_topics_if_needed()
    while True:
        for endpoint, url in api_endpoints.items():
            fetch_and_send_to_kafka(endpoint, url, topics[endpoint])
        producer.flush()
        print(f"⏱️ Waiting {FETCH_INTERVAL} seconds...\n")
        time.sleep(FETCH_INTERVAL)

if __name__ == "__main__":
    main()
