import smbus
import time

class CCS811(object):

	def __init__(self, device_bus=1, device_address=0x5B):
		self.device_bus = device_bus 
		self.device_address = device_address
		self.bus = smbus.SMBus(self.device_bus)

	def read_byte_data(self, address):
		return self.bus.read_byte_data(self.device_address, address)

	def write_byte_data(self, address, data):
		self.bus.write_byte_data(self.device_address, address, data)

	def write_byte(self, address):
		self.bus.process_call(self.device_address, address, 0)

if __name__ == "__main__":
	my_ccs811 = CCS811()
	byte = my_ccs811.read_byte_data(0x20)
	print(format(byte, '02x'))

	my_ccs811.write_byte(0xF4,)
	byte = my_ccs811.read_byte_data(0x00)
	print(format(byte, '02x'))
	
