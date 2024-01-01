
import time,json
import threading
import logging
import asyncio
from aiocoap import *
import aiocoap
from aiocoap import Context, Message, GET
import aiocoap.resource as resource
from aiocoap.numbers.contentformat import ContentFormat
from sensor_resource.proximity import ProximitySensorResource
from support.result_publisher import ResultPublisher

no_of_test_runs = 200
host_ip = "192.168.1.83"
port = 3030

broker = ""
topic_result =""

class CoAPServer:
    def __init__(self) -> None:
        logging.basicConfig(level=logging.INFO)
        logging.getLogger("coap-server").setLevel(logging.DEBUG)
        
    async def start_server(self):
        print("--Server start --")
        root = resource.Site()
        root.add_resource(['.well-known', 'core'],
                resource.WKCResource(root.get_resources_as_linkheader))
        root.add_resource(['sensor','proximity'],ProximitySensorResource())

        self.server_context = await aiocoap.Context.create_server_context(site=root,bind=(host_ip,port))
        print("Server context created")

        # Run forever
        await asyncio.get_running_loop().create_future()
        print("--Server end --")
        
    async def stop_server(self):
        print("Stopping server")
        await self.server_context.shutdown()
        

class CoAPClient:
    def __init__(self,host_ip,port) -> None:
        self.host_ip = host_ip
        self.port = port
        self.uri = f'coap://{self.host_ip}:{self.port}/sensor/proximity'
        self.tp_calculator = ThroughputCalculator()
    
    def set_no_of_test_runs(self, no):
        self.no_of_test = no
        self.tp_calculator.set_total_messages(self.no_of_test)
        
    async def start_client(self):
        protocol = await Context.create_client_context()
        msg = Message(code= GET, uri=self.uri, mtype= 0)
        self.tp_calculator.set_start_time(asyncio.get_event_loop().time())
        for _ in range(no_of_test_runs):
            response = await protocol.request(msg).response
            if response.code.is_successful():
                self.tp_calculator.increment_success_message()
            response_str = response.payload.decode()
        self.tp_calculator.set_end_time(asyncio.get_event_loop().time())
        self.tp_calculator.calculate()
        print("Throughput = ",self.tp_calculator.throughput)
        
class ThroughputCalculator:
    def __init__(self) -> None:
        self.success_message = 0
        
    def set_start_time(self,s_time):
        self.start_time = s_time
        
    def set_end_time(self,e_time):
        self.end_time = e_time
        
    def increment_success_message(self):
        self.success_message += 1
        
    def set_total_messages(self,no):
        self.total_messages = no
        
    def calculate(self):
        time_elapse = self.end_time - self.start_time
        self.throughput = self.success_message * 100/self.total_messages
        return self.throughput


def start_server(server):
    asyncio.run(server.start_server())
    

if __name__ == "__main__":
    server = CoAPServer()
    server_thread = threading.Thread(target=start_server,args=[server])
    server_thread.start()
    time.sleep(0.1)
    print("Starting client...")
    client = CoAPClient(host_ip,port)
    client.set_no_of_test_runs(no_of_test_runs)
    asyncio.run(client.start_client())
    print("Finished client...")
    asyncio.run(server.stop_server())