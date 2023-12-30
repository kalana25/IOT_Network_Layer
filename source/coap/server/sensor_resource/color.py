import sys , os, json, time
import aiocoap
import aiocoap.resource as resource

sys.path.append(os.path.abspath(os.path.join('source','sensor')))
from rgb_sensor import get_rgb

class ColorSensorResource(resource.Resource):
    async def render_get(self,request):
        rgb_data = get_rgb().encode('ascii')
        start_time = time.time()
        dic_object = { 'sensor_data': rgb_data, 'start_time': start_time }
        dic_string = json.dumps(dic_object)
        return aiocoap.Message(payload=dic_string)