from result_pub import ResultPublisher
import json

broker = "192.168.1.83"
port = 1883
topic_result = "iotproject/group788/benchmark/throughput"

summary_pub = ResultPublisher(broker,port,topic_result)
# summary_pub.set_message(json.dumps({'average_tp': avg_tp, 'loss': loss}))
summary_pub.set_message(json.dumps({'average_tp': 90, 'loss': 10}))
summary_pub.run_client()