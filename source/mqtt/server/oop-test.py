import paho.mqtt.client as mqtt
import time, random, sys , os

sys.path.append(os.path.abspath(os.path.join('source','sensor')))
from proximity_decoy_sensor import get_proximity

# Parameters
broker = "192.168.1.83"
port = 1883
topic = "iotproject/group788/prox"
num_clients = 10


class ThroughputCalculator:
  def __init__(self) -> None:
    # This represent messages sent to the broker successfully.
    self.success_messages = 0
  
  def increment_messages_count(self):
    self.success_messages += 1
    
  def set_total_message_count(self, no):
    self.total_messages = no
    
  def calculate_throughput(self):
    percentage = self.success_messages*100/self.total_messages
    return percentage

class Publisher:
  
  def on_connect(self, client, userdata, flags, rc):
    if rc == 0:
        print("Connected to Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)
        
  def on_publish(self, client, userdata, mid):
    self.throughput_calculator.increment_messages_count()
    print(f"Message {mid} published")
  
  def __get_client_id(self):
    self.client_id = f'mqtt-benchmark-publisher {random.randint(0, 1000)}'
    return self.client_id
  
  def set_no_of_test_cases(self, no):
    self.no_of_messages = no
    self.throughput_calculator.set_total_message_count(no)
  
  def set_message(self):
    #  self.payload = get_proximity()
     self.payload = f'mqtt-benchmark-publisher {random.randint(0, 1000)}'
  
  def __config_client(self)-> None:
    self.client = self.__get_client()
    self.client.on_connect = self.on_connect
    self.client.on_publish = self.on_publish
  
  def __get_client(self):
    client_id = self.__get_client_id()
    user_data = client_id
    self.client = mqtt.Client(client_id,userdata= user_data)
    return self.client
  
  def run_client(self):
    try:
      self.__config_client()
      self.client.connect(self.broker, self.port)
      self.client.loop_start()
      for _ in range(self.no_of_messages):
        self.payload = self.set_message()
        self.client.publish(self.topic, self.payload)
        time.sleep(0.1)  # Adjust the delay between messages
      print('Throughput ', self.throughput_calculator.calculate_throughput())
    except KeyboardInterrupt:
      self.client.disconnect()
      self.client.loop_stop()
      
  def __init__(self, broker, port,topic):
    self.broker = broker
    self.port = port
    self.topic = topic
    self.throughput_calculator = ThroughputCalculator()

obj = Publisher(broker,port,topic)
obj.set_no_of_test_cases(50)
obj.run_client()


