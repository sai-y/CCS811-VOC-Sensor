from periphery import I2C
import time

class CCS811(object):

	def __init__(self, device_bus=1, device_address=0x5B):
		self.device_bus = device_bus 
		self.device_address = device_address
		self.bus = I2C("/dev/i2c-1")

	def read_byte(self, address):
		msgs = [I2C.Message([address], read=False)]
		self.bus.transfer(self.device_address, msgs)

		msgs = [I2C.Message([address], read=True)]
		self.bus.transfer(self.device_address, msgs)
		
		return (msgs[0].data[0])

	def write_byte(self, address):
		msgs = [I2C.Message([address], read=False)]
		self.bus.transfer(self.device_address, msgs)

	def reset(self):
		msgs = [I2C.Message([0xFF, 0x11, 0xE5, 0x72, 0x8A], read=False)]
		self.bus.transfer(self.device_address, msgs)

	def write_byte_data(self, address, data):
		msgs = [I2C.Message([address, data], read=False)]
		self.bus.transfer(self.device_address, msgs)

	def read_bytes(self, count):
		msgs = [I2C.Message([0] * count, read=True)]
		self.bus.transfer(self.device_address, msgs)
		return (msgs[0].data)

if __name__ == "__main__":
	my_ccs811 = CCS811()
	my_ccs811.reset()
	
	time.sleep(1)
	
	print(my_ccs811.read_byte(0x00))
	print(my_ccs811.read_byte(0x20))

	my_ccs811.write_byte(0xF4)
	print(my_ccs811.read_byte(0x00))
	
	my_ccs811.write_byte_data(0x01, 0x10)
	print(my_ccs811.read_byte(0x00))
	
	time.sleep(1)
	
	my_ccs811.read_byte(0x00)
	
	while True:
		if my_ccs811.read_byte(0x00) == 152:
			my_ccs811.write_byte(0x02)
			time.sleep(1.625)
			data = my_ccs811.read_bytes(8)
			print(data)
			eco2 = data[0] << 8 | data[1]
			voc = data[2] << 8 | data[3]
			print(eco2, voc)
		else:
			my_ccs811.reset()
			print(my_ccs811.read_byte(0x00))
		time.sleep(2)
	
