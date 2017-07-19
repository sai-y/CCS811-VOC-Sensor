from periphery import I2C
import time

class CCS811(object):

	def __init__(self, device_bus=1, device_address=0x5B):
		self.device_bus = device_bus 
		self.device_address = device_address
		self.bus = I2C("/dev/i2c-1")

	def read_byte_data(self, address):
		msgs = [I2C.Message([address], read=True)]
		self.bus.transfer(self.device_address, msgs)
		print(msgs[0].data,'02x')

	def write_byte(self, address, data):
		self.bus.write_byte_data(self.device_address, address, data)

	def write_quick(self, address):
		self.bus.write_quick(self.device_address)

	def write_block_data(self, address, vals):
		self.bus.write_i2c_block_data(self.device_address, address, vals)

if __name__ == "__main__":
	my_ccs811 = CCS811()
	#my_ccs811.write_block_data(0xFF, [ 0x11, 0xE5, 0x72, 0x8A])
	time.sleep(1)
	byte = my_ccs811.read_byte_data(0x20)
	#print(byte)

	#my_ccs811.write_byte(0xF4, 0x00)
	#my_ccs811.write_byte(0xF4, 0x00)
	#byte = my_ccs811.read_byte_data(0x00)
	#print(format(byte, '02x'))
	
