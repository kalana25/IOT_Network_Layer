import paho.mqtt.client as mqtt
import time

# Define callback functions
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

# Replace 'your_broker_address' and 'your_topic' with your MQTT broker address and topic
broker_address = "test.mosquitto.org"
topic = "iotproject/group788/prox"

# Create an MQTT client
client = mqtt.Client()

# Set the callback functions
client.on_connect = on_connect

# Connect to the MQTT broker
client.connect(broker_address, 1883, 60)

# Publish messages
while True:
    message = "Hello, message"
    client.publish(topic, message)
    print(f"Published: {message}")
    time.sleep(1)
