import paho.mqtt.client as mqtt
from paho.mqtt import client as mqtt_client
import time, random, sys , os,logging
import json

FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60

class Subscriber:
    def __init__(self, client_id, broker,port,sub_topic) -> None:
        self.time_list = []
        self.client_id = client_id
        self.broker = broker
        self.port = port
        self.topic = sub_topic
    
    def __get_client_id(self):
        return f'mqtt-speed-bench-sub {self.client_id}'
    
    def __get_client(self):
        client_id = self.__get_client_id()
        user_data = client_id
        self.client = mqtt.Client(client_id,userdata= user_data)
        return self.client
    
    def __config_client(self)-> None:
        self.client = self.__get_client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        self.client.on_subscribe = self.on_subscribe
        
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    
    def on_disconnect(self, client, userdata, rc):
        logging.info("Disconnected with result code: %s", rc)
        reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
        while reconnect_count < MAX_RECONNECT_COUNT:
            logging.info("Reconnecting in %d seconds...", reconnect_delay)
            time.sleep(reconnect_delay)

            try:
                client.reconnect()
                logging.info("Reconnected successfully!")
                return
            except Exception as err:
                logging.error("%s. Reconnect failed. Retrying...", err)

            reconnect_delay *= RECONNECT_RATE
            reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
            reconnect_count += 1
        logging.info("Reconnect failed after %s attempts. Exiting...", reconnect_count)

    def on_subscribe(self, client, userdata, mid, granted_qos):
        print(f"Subscribed to topic: {self.topic}")
  
    def on_message(self, client, userdata, msg):
        data = json.loads(msg.payload.decode())
        print('Data = ',data)
        
    def run_client(self):
        try:
            self.__config_client()
            self.client.connect(self.broker, self.port)
            self.client.subscribe(self.topic)
            self.client.loop_start()
            while True:
                time.sleep(1)
            print("Stopping client")
            self.client.loop_stop()
        except KeyboardInterrupt:
            self.client.disconnect()
            self.client.loop_stop()  
