import sys , os

print(os.path.abspath(os.path.join('source','sensor')))
sys.path.append(os.path.abspath(os.path.join('source','sensor')))
from proximity_decoy_sensor import get_proximity

print(get_proximity())