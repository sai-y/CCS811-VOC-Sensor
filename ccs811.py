import smbus

DEVICE_BUS = 1
DEVICE_ADDRESS = 0x5B
bus = smbus.SMBUS(DEVICE_BUS)
byte = bus.read_byte_data(0x00)