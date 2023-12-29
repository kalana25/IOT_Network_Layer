import sys , os
import aiocoap
import aiocoap.resource as resource

sys.path.append(os.path.abspath(os.path.join('source','sensor')))
from rgb_sensor import get_rgb

class ColorSensorResource(resource.Resource):
    async def render_get(self,request):
        prox_data = get_rgb().encode('ascii')
        return aiocoap.Message(payload=prox_data)