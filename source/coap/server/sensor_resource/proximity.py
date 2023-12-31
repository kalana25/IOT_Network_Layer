import sys , os, time, json
import aiocoap
import aiocoap.resource as resource

sys.path.append(os.path.abspath(os.path.join('source','sensor')))
from proximity_decoy_sensor import get_proximity

class ProximitySensorResource(resource.Resource):
    async def render_get(self,request):
        prox_data = get_proximity()
        start_time = time.time()
        dic_object = { 'sensor_data': prox_data, 'start_time': start_time }
        return aiocoap.Message(payload=json.dumps(dic_object).encode('ascii'))