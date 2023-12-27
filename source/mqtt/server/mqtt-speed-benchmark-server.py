import paho.mqtt.client as mqtt
from paho.mqtt import client as mqtt_client
import time, random, sys , os,logging
import json

sys.path.append(os.path.abspath(os.path.join('source','sensor')))
from proximity_sensor import get_proximity

FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60

broker = "192.168.1.83"	# Broker 
pub_sub_topic = "iotproject/group788/prox"       # send messages to this topic
port = 1883
no_of_test_runs = 200

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

    def set_no_of_test_cases(self, no):
        self.no_of_messages = no
        
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
        print(f"Initiating the server")
        pub.run_client()
  
    def on_message(self, client, userdata, msg):
        data = json.loads(msg.payload.decode())
        finish_time = time.time()
        self.time_list.append((finish_time,data['start_time']))
        # print("Received ",msg.payload.decode()," from ",msg.topic," Topic")
        
    def run_client(self):
        try:
            self.__config_client()
            time_with_connection = time.time()
            self.client.connect(self.broker, self.port)
            self.client.subscribe(self.topic)
            self.client.loop_start()
            while len(self.time_list) < no_of_test_runs:
                pass
            self.calculate_execution_speed()
            print("Stopping client")
            self.client.loop_stop()
        except KeyboardInterrupt:
            self.client.disconnect()
            self.client.loop_stop()  

    def calculate_execution_speed(self):
        difference =[]
        for time_tuple in self.time_list:
            end_time,start_time = time_tuple
            difference.append(end_time-start_time)
        average_speed = sum(difference)/len(difference)
        print("Average speed", average_speed, sep="\t")

class Publisher:
    
    def on_connect(self,client, userdata, flags, rc):
        if rc==0:
            print("Connection established. Code: "+str(rc))
        else:
            print("Connection failed. Code: " + str(rc))
    
    def on_publish(self,client, userdata, mid):
        print("Published: " + str(mid))
        
    def on_disconnect(self,client, userdata, rc):
        if rc != 0:
            print ("Unexpected disonnection. Code: ", str(rc))
        else:
            print("Disconnected. Code: " + str(rc))
            
    def on_log(self,client, userdata, level, buf):		# Message is in buf
        print("MQTT Log: " + str(buf))
    
    def __get_client_id(self):
        return f'mqtt-speed-bench-pub {self.client_id}'
    
    def set_no_of_test_cases(self, no):
        self.no_of_messages = no
        
    def set_message(self):
        self.payload = get_proximity()
        
    def __config_client(self)-> None:
        self.client = self.__get_client()
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.on_disconnect = self.on_disconnect
        self.client.on_log = self.on_log
        
    def __get_client(self):
        client_id = self.__get_client_id()
        user_data = client_id
        self.client = mqtt.Client(client_id,userdata= user_data)
        return self.client
    
    def run_client(self):
        try:
            self.__config_client()
            
            # Connect to MQTT 
            print("Attempting to connect to broker " + self.broker)
            # This is the initial time take to make connection. This is considered for the 1st packet.
            time_with_connection = time.time()

            self.client.connect(self.broker, self.port)
            self.client.loop_start()

            for count in range(self.no_of_messages):
                if count == 0:
                    payload = {
                        'sensor_val': get_proximity(),
                        'start_time': time_with_connection
                    }
                else:
                    payload = {
                        'sensor_val': get_proximity(),
                        'start_time': time.time()
                    }
                payload_str = json.dumps(payload)
                self.client.publish(self.topic, payload_str)
                time.sleep(0.1)
            self.client.disconnect()
            self.client.loop_stop()
            
        except KeyboardInterrupt:
            self.client.disconnect()
            self.client.loop_stop()
            
    def __init__(self, client_id, broker, port,topic):
        self.client_id = client_id
        self.broker = broker
        self.port = port
        self.topic = topic
        
# pub.run_client()
pub = Publisher(random.randint(0, 1000),broker,port,pub_sub_topic)
pub.set_no_of_test_cases(no_of_test_runs)

sub = Subscriber(random.randint(0,1000),broker,port,pub_sub_topic)
sub.set_no_of_test_cases(no_of_test_runs)
sub.run_client()
