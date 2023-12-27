
import logging, time, random, json
from paho.mqtt import client as mqtt_client

FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60

broker = "192.168.1.83"	

topic = "iotproject/group788/prox"
port = 1883
client_id = f'mqtt-benchmark-client{random.randint(0, 1000)}'

time_list = []
no_of_test_runs = 200

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)
        
def on_disconnect(client, userdata, rc):
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
    
def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    finish_time = time.time()
    time_list.append((finish_time,data['start_time']))
    # print("Received ",msg.payload.decode()," from ",msg.topic," Topic")
    
def calculate_execution_speed():
    difference =[]
    for time_tuple in time_list:
        end_time,start_time = time_tuple
        difference.append(end_time-start_time)
    average_speed = sum(difference)/len(difference)
    print("Average speed", average_speed, sep="\t")

# Set Connecting Client ID
client = mqtt_client.Client(client_id)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
time_with_connection = time.time()
client.connect(broker, port)
client.subscribe(topic)
client.loop_start()
while len(time_list) < no_of_test_runs:
    pass
calculate_execution_speed()
print("Stopping client")
client.loop_stop()