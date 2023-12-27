import asyncio
import random
import string
import json
import time
import concurrent.futures
import paho.mqtt.client as mqtt
import subprocess

def start_mqtt_bench(broker_address, num_messages, num_clients):
    command = [
        "mqtt-bench",
        "--broker", broker_address,
        "--messages", str(num_messages),
        "--clients", str(num_clients),
    ]

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for the mqtt-bench process to finish
    process.wait()

    # Capture the output of the mqtt-bench process
    output, error = process.communicate()

    if process.returncode == 0:
        print("MQTT Throughput Test Completed Successfully")
        print(output.decode("utf-8"))
    else:
        print("MQTT Throughput Test Failed")
        print("Error:", error.decode("utf-8"))

if __name__ == "__main__":
    broker_address = "192.168.1.83"
    num_messages = 1000
    num_clients = 10
    start_mqtt_bench(broker_address, num_messages, num_clients)