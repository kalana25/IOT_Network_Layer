import datetime
import logging
import asyncio
import aiocoap
import aiocoap.resource as resource
from aiocoap.numbers.contentformat import ContentFormat
from sensor_resource.proximity import ProximitySensorResource


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

        await aiocoap.Context.create_server_context(site=root,bind=("192.168.0.106",3030))
        print("Server context created")

        # Run forever
        await asyncio.get_running_loop().create_future()
        print("--Server end --")
        
if __name__ == "__main__":
    server = CoAPServer()
    asyncio.run(server.start_server())