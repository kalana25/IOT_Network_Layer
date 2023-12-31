import random,time
import paho.mqtt.client as mqtt

class ResultPublisher:
  def on_connect(self, client, userdata, flags, rc):
    if rc == 0:
        print("Connected to Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)

  def on_publish(self, client, userdata, mid):
    print(f"------Benchmark result {mid} published------")
  
  def __get_client_id(self):
    self.client_id = f'mqtt-benchmark-publisher {random.randint(0,1000)}'
  
  def __get_client(self):
    client_id = self.__get_client_id()
    user_data = client_id
    self.client = mqtt.Client(client_id,userdata= user_data)
    return self.client
  
  def set_message(self,data):
     self.payload = data
   
  def run_client(self):
    try:
      self.__config_client()
      self.client.connect(self.broker, self.port)
      self.client.loop_start()
      self.client.publish(self.topic, self.payload)
      time.sleep(0.1)  # Adjust the delay between messages
      self.client.disconnect()
      self.client.loop_stop()
    except KeyboardInterrupt:
      self.client.disconnect()
      self.client.loop_stop()
  
  def __config_client(self)-> None:
    self.client = self.__get_client()
    self.client.on_connect = self.on_connect
    self.client.on_publish = self.on_publish
   
  def __init__(self, broker, port,topic):
    self.broker = broker
    self.port = port
    self.topic = topic
