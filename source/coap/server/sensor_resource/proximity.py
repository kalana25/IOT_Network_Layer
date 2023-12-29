import sys , os
import aiocoap
import aiocoap.resource as resource

sys.path.append(os.path.abspath(os.path.join('source','sensor')))
from proximity_decoy_sensor import get_proximity

class ProximitySensorResource(resource.Resource):
    async def render_get(self,request):
        prox_data = get_proximity().encode('ascii')
        return aiocoap.Message(payload=prox_data)