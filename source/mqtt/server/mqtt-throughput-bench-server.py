import logging, time, random, json, asyncio, sys, os
from paho.mqtt import client as mqtt_client

broker = "192.168.1.78"	
pub_topic = "iotproject/group788/prox"
port = 1883
no_of_test_runs = 100
no_of_clients = 10

sys.path.append(os.path.abspath(os.path.join('source','sensor')))
from proximity_decoy_sensor import get_proximity

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)
        
def on_publish(client, userdata, mid):
    print(f"Message {mid} published")

async def create_and_run_client(client_id):
    client = mqtt_client.Client(f'mqtt-benchmark-client{client_id}')
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.connect_async(broker,port)
    client.loop_start()
    
    for count in range(no_of_test_runs):
        sensor_val = get_proximity()
        infor = client.publish(pub_topic, sensor_val)
        delivery_success = infor.is_published()
        await asyncio.sleep(0.1)
    client.disconnect()


async def main():
    print("--main start--")
    await create_and_run_client(1)
    print("--main end--")
    
asyncio.run(main())
