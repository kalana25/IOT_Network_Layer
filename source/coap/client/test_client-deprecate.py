# do not use this anymore since clinet and server has to run separately. functionality works well. 
# client and server both integrate on benchmark versions in a single program.

import asyncio
from aiocoap import *

no_of_messages = 1000

async def main():
    protocol = await Context.create_client_context()
    msg = Message(code=GET, uri="coap://192.168.1.83:3030/sensor/proximity")
    for _ in range(no_of_messages):
        response = await protocol.request(msg).response
        print("-----")
        print(response.payload)

asyncio.run(main())