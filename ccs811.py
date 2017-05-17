import smbus

DEVICE_BUS = 1
DEVICE_ADDRESS = 0x5B
bus = smbus.SMBus(DEVICE_BUS)
byte = bus.read_byte_data(DEVICE_BUS, 0x00)