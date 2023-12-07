import adafruit_tsl2591 	# High range lux sensor

# Using decimal to round the value for lux :)
from decimal import Decimal

# Imports for sensor
import busio
import board

i2c = busio.I2C(board.SCL, board.SDA)

lux_sensor = adafruit_tsl2591.TSL2591(i2c)		# High range lux sensor

def get_lux():
	lux = lux_sensor.lux
	lux_value = round(Decimal(lux), 3) 	# Rounds the lux value to 3 decimals, and prints it
	print('Total light: {0} lux'.format(lux_value))
	return lux_value