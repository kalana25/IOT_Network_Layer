import adafruit_tcs34725 	# RGB sensor




# Using decimal to round the value for lux :)
from decimal import Decimal

# Imports for sensor
import busio
import board

i2c = busio.I2C(board.SCL, board.SDA)

rgb_sensor = adafruit_tcs34725.TCS34725(i2c)	# RGB sensor

def get_rgb():
	rgb_value = '{0},{1},{2}'.format(*rgb_sensor.color_rgb_bytes)
	return rgb_value