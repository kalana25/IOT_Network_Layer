import sys , os, json, time
import aiocoap
import aiocoap.resource as resource

sys.path.append(os.path.abspath(os.path.join('source','sensor')))
from light_sensor import get_lux

class LightSensorResource(resource.Resource):
    async def render_get(self,request):
        lux_data = get_lux().encode('ascii')
        start_time = time.time()
        dic_object = { 'sensor_data': get_lux, 'start_time': start_time }
        dic_string = json.dumps(dic_object)
        return aiocoap.Message(payload=dic_string)