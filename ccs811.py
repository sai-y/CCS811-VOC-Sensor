from periphery import I2C
import time

class CCS811(object):

	def __init__(self, device_bus=1, device_address=0x5B):
		self.device_bus = device_bus 
		self.device_address = device_address
		self.bus = I2C("/dev/i2c-1")

	def read_register(self, address):
		msgs = [I2C.Message([address], read=True)]
		self.bus.transfer(self.device_address, msgs)
		return msgs[0].data[0]

	def start_command(self, data):
		msg = [I2C.Message([0xF4])]
		self.bus.transfer(self.device_address, msg)

	def write_byte(self, address):
		msgs = [I2C.Message([address], read=False)]
		self.bus.transfer(self.device_address, msgs)

	def write_quick(self, address):
		self.bus.write_quick(self.device_address)

	def write_block_data(self, address, vals):
		self.bus.write_i2c_block_data(self.device_address, address, vals)

if __name__ == "__main__":
	my_ccs811 = CCS811()
	#my_ccs811.write_block_data(0xFF, [ 0x11, 0xE5, 0x72, 0x8A])
	time.sleep(1)
	print(my_ccs811.read_register(0x00))
	#print(byte)

	#my_ccs811.write_byte(0xF4)
	#my_ccs811.read_byte_data(0x00)
	#my_ccs811.write_byte(0xF4, 0x00)
	#byte = my_ccs811.read_byte_data(0x00)
	#print(format(byte, '02x'))
	
