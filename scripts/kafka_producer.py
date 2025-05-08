import requests
from kafka import KafkaProducer
import json
import time


FETCH_INTERVAL = 10 # seconds

producer = KafkaProducer(
    bootstrap_servers=['localhost:9093'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)



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


def fetch_and_send_to_kafka(endpoint_name, url, topic):
    print(f"Fetching data from {endpoint_name} API...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        for item in data:
            producer.send(topic, value=item)
        
        print(f"Sent data from {endpoint_name} to Kafka topic {topic}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {endpoint_name}: {e}")


def main():
    while True:
        for endpoint_name, url in api_endpoints.items():
            topic = topics[endpoint_name]
            fetch_and_send_to_kafka(endpoint_name, url, topic)
        
        time.sleep(FETCH_INTERVAL)


if __name__ == "__main__":
    main()
