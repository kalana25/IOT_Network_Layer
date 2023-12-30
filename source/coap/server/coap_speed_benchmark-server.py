import time,json
import threading
import logging
import asyncio
from aiocoap import *
import aiocoap
import aiocoap.resource as resource
from aiocoap.numbers.contentformat import ContentFormat
from sensor_resource.proximity import ProximitySensorResource


no_of_test_runs = 10
host_ip = "192.168.1.83"
port = 3030
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

        await aiocoap.Context.create_server_context(site=root,bind=(host_ip,port))
        print("Server context created")

        # Run forever
        await asyncio.get_running_loop().create_future()
        print("--Server end --")
        
        
class CoAPClient:
    def __init__(self,host_ip,port) -> None:
        self.host_ip = host_ip
        self.port = port
        self.uri = f'coap://{self.host_ip}:{self.port}/sensor/proximity'
        self.speed_calculator = SpeedCalculator()
    
    async def start_client(self):
        protocol = await Context.create_client_context()
        msg = Message(code=GET, uri=self.uri)
        for _ in range(no_of_test_runs):
            response = await protocol.request(msg).response
            end_time = time.time()
            response_str = response.payload.decode()
            if(response_str):
                start_time = json.loads(response_str)['start_time']
                if(end_time > start_time):
                    self.speed_calculator.push_sensor_data((end_time,start_time))
                    average_speed = self.speed_calculator.calculate_speed()
                    print("Average execution speed ",average_speed)
                else:
                    print ("---- Wrong ---- Wrong ---- Wrong ---- Wrong ----Wrong ---- ")
        # start calculating speed
        
class SpeedCalculator:
    def __init__(self) -> None:
        self.data_list = []
        
    def push_sensor_data(self,tuple):
        end_time, start_time = tuple
        self.data_list.append(end_time - start_time)
        
    def calculate_speed(self):
        # calculate average speed of the execution
        return sum(self.data_list)/len(self.data_list)

def start_server():
    server = CoAPServer()
    asyncio.run(server.start_server())    
        
if __name__ == "__main__":
    threads = []
    server_thread = threading.Thread(target=start_server)
    threads.append(server_thread)
    server_thread.start()
    try:
        time.sleep(1)
        print("Starting client...")
        client = CoAPClient(host_ip,port)
        asyncio.run(client.start_client())
    except KeyboardInterrupt:
        print("\nStopping clients...")
        for thread in threads:
            thread.join()
    