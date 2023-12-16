import asyncio
from aiocoap import *

async def main():
    protocol = await Context.create_client_context()
    msg = Message(code=GET, uri="coap://192.168.1.78:3030/sensor/proximity")
    response = await protocol.request(msg).response
    print("-----")
    print(response.payload)

asyncio.run(main())