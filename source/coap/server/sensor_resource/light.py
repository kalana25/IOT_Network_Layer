import sys , os
import aiocoap
import aiocoap.resource as resource

sys.path.append(os.path.abspath(os.path.join('source','sensor')))
from light_sensor import get_lux

class LightSensorResource(resource.Resource):
    async def render_get(self,request):
        prox_data = get_lux().encode('ascii')
        return aiocoap.Message(payload=prox_data)