import adafruit_vcnl4010 	# Proximity sensor

# Imports for sensor
import busio
import board

i2c = busio.I2C(board.SCL, board.SDA)

prox_sensor = adafruit_vcnl4010.VCNL4010(i2c)	# Proximity

def get_proximity():
	proximity = prox_sensor.proximity # The higher the value, object closer to sensor
	print('Proximity: {0}'.format(proximity))
	return proximity