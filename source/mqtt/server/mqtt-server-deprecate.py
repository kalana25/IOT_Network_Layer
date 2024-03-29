# This program is old version. works fine but Publisher and Subscriber has implmented in same program in oop version.
# Everyother thing is working fine.

import time
import json
import datetime
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

import sys , os
sys.path.append(os.path.abspath(os.path.join('source','sensor')))
from proximity_sensor import get_proximity


# Set MQTT broker and topic
broker = "192.168.1.78"	# Broker 
pub_topic = "iotproject/group788/prox"       # send messages to this topic
port = 1883
no_of_test_runs = 200


# Event handlers
def on_connect(client, userdata, flags, rc):
	if rc==0:
		print("Connection established. Code: "+str(rc))
	else:
		print("Connection failed. Code: " + str(rc))
		
def on_publish(client, userdata, mid):
    print("Published: " + str(mid))
	
def on_disconnect(client, userdata, rc):
	if rc != 0:
		print ("Unexpected disonnection. Code: ", str(rc))
	else:
		print("Disconnected. Code: " + str(rc))
	
def on_log(client, userdata, level, buf):		# Message is in buf
    print("MQTT Log: " + str(buf))

	
# Connect functions for MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish
client.on_log = on_log

# Connect to MQTT 
print("Attempting to connect to broker " + broker)

# This is the initial time take to make connection. This is considered for the 1st packet.
time_with_connection = time.time()

client.connect(broker,port)	# Broker address, port and keepalive (maximum period in seconds allowed between communications with the broker)
client.loop_start()


# for count in range(no_of_test_runs):
#     if count == 0:
#         payload = {
# 			'sensor_val': get_proximity(),
# 			'start_time': time_with_connection
# 		}
#     else:
#         payload = {
# 			'sensor_val': get_proximity(),
# 			'start_time': time.time()
# 		}
#     payload_str = json.dumps(payload)
#     client.publish(pub_topic, payload_str)
#     time.sleep(0.1)
while True:
	client.publish(pub_topic, get_proximity())
	time.sleep(0.1)
 
client.disconnect()