from result_sub import Subscriber
import random

broker = "192.168.1.83"	# Broker 
topic_result = "iotproject/group788/benchmark/throughput"
port = 1883


sub = Subscriber(random.randint(0,1000),broker,port,topic_result)
sub.run_client()