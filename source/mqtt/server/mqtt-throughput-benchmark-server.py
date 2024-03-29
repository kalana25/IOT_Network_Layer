import paho.mqtt.client as mqtt
import time, random, sys , os, threading,json

sys.path.append(os.path.abspath(os.path.join('source','sensor')))
from proximity_sensor import get_proximity

# Parameters
broker = "192.168.1.83"
port = 1883
topic = "iotproject/group788/prox"
topic_result = "iotproject/group788/benchmark/throughput"
num_clients = 80
num_test_cases = 150


class ThroughputCalculator:
  def __init__(self) -> None:
    # This represent messages sent to the broker successfully.
    self.success_messages = 0
  
  def increment_messages_count(self):
    self.success_messages += 1
    
  def set_total_message_count(self, no):
    self.total_messages = no
    
  def calculate_throughput(self):
    self.throughput = self.success_messages*100/self.total_messages
    return self.throughput

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
    return f'mqtt-benchmark-publisher {self.client_id}'
  
  def set_no_of_test_cases(self, no):
    self.no_of_messages = no
    self.throughput_calculator.set_total_message_count(no)
  
  def set_message(self):
     self.payload = get_proximity()
  
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
      
  def __init__(self, client_id, broker, port,topic):
    self.client_id = client_id
    self.broker = broker
    self.port = port
    self.topic = topic
    self.throughput_calculator = ThroughputCalculator()

# obj = Publisher(broker,port,topic)
# obj.set_no_of_test_cases(50)
# obj.run_client(1)

def calculate_summary():
  total_throughput =0
  average_throughput =0
  for pub in publisher_list:
    total_throughput += pub.throughput_calculator.throughput
  average_throughput = total_throughput/len(publisher_list)
  loss = 100 - average_throughput
  print("Average throughput = ",average_throughput)
  print("Average loss = ",loss)
  return average_throughput,loss
    
threads = []
publisher_list =[ Publisher(client_id,broker,port,topic) for client_id in range(num_clients)]
  
for pub in publisher_list:
  pub.set_no_of_test_cases(num_test_cases)
  thread = threading.Thread(target=pub.run_client)
  threads.append(thread)
  thread.start()
try:
  for thread in threads:
      thread.join()
  print("All publishers finished")
  avg_tp, loss = calculate_summary()
  # Now result will be publish to same broker
  summary_pub = ResultPublisher(broker,port,topic_result)
  summary_pub.set_message(json.dumps({'average_tp': avg_tp, 'loss': loss}))
  summary_pub.run_client()
  
except KeyboardInterrupt:
    print("\nStopping clients...")
    for thread in threads:
        thread.join()
