import paho.mqtt.client as mqtt
import time, random, sys , os
import json

sys.path.append(os.path.abspath(os.path.join('source','sensor')))
from proximity_decoy_sensor import get_proximity


broker = "192.168.1.83"	# Broker 
pub_topic = "iotproject/group788/prox"       # send messages to this topic
port = 1883
no_of_test_runs = 200


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
        
pub = Publisher(random.randint(0, 1000),broker,port,pub_topic)
pub.set_no_of_test_cases(no_of_test_runs)
pub.run_client()
