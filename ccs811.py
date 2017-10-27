from periphery import I2C, I2CError
import time
import blinkt
import requests
import configparser

URL = "https://maker.ifttt.com/trigger/voc_data/with/key/{key}"


class CCS811(object):

    def __init__(self, device_bus=1, device_address=0x5A):
        self.device_bus = device_bus
        self.device_address = device_address
        self.bus = I2C("/dev/i2c-1")

    def start_app(self):
        self.write_byte(0xF4)
        print(self.read_byte(0x00))
        self.write_byte_data(0x01, 0x10)

    def transfer(self, msgs):
        try:
            self.bus.transfer(self.device_address, msgs)
        except I2CError as error:
            print(str(error))
        return msgs

    def close(self):
        self.bus.close()

    def read_byte(self, address):
        msgs = [I2C.Message([address], read=False)]
        self.transfer(msgs)
        msgs = [I2C.Message([address], read=True)]
        ret_msg = self.transfer(msgs)

        return (ret_msg[0].data[0])

    def write_byte(self, address):
        msgs = [I2C.Message([address], read=False)]
        self.transfer(msgs)

    def reset(self):
        msgs = [I2C.Message([0xFF, 0x11, 0xE5, 0x72, 0x8A], read=False)]
        self.transfer(msgs)

    def write_byte_data(self, address, data):
        msgs = [I2C.Message([address, data], read=False)]
        self.transfer(msgs)

    def read_bytes(self, count):
        msgs = [I2C.Message([0] * count, read=True)]
        ret_msg = self.transfer(msgs)
        return ret_msg[0].data


def post_data(data):

    config = configparser.ConfigParser()
    config.read('/home/pi/key.ini')
    key = config.get('CREDENTIALS', 'key')
    payload = {'value1': data[0], 'value2': data[1]}
    print(URL.format(key=key))
    try:
        response = requests.post(URL.format(key=key), json=payload)
    except requests.exceptions.ConnectionError as error:
        print(str(error))
    if response.status_code == 200:
        return 1
    return 0


def FadeInOut(delay):
    # Reference:
    # https://github.com/dglaude/minecraftstatus-blinkt/blob/master/mc_blinkt_fade.py
    for b in range(31):
        blinkt.set_brightness(b/31.0)
        blinkt.show()
        time.sleep(delay)
    for b in range(31):
        blinkt.set_brightness((31-b)/31.0)
        blinkt.show()
        time.sleep(delay)

if __name__ == "__main__":
    my_ccs811 = CCS811(device_address=0x5B)
    my_ccs811.reset()

    blinkt.set_clear_on_exit(value=True)
    
    print(my_ccs811.read_byte(0x00))
    print(my_ccs811.read_byte(0x20))

    my_ccs811.start_app()

    my_ccs811.read_byte(0x00)
    measurement_time = time.time()
    print(post_data([1, 2]))

    while True:
        if my_ccs811.read_byte(0x00) == 152:
            my_ccs811.write_byte(0x02)
            data = my_ccs811.read_bytes(8)

            eco2 = data[0] << 8 | data[1]
            voc = data[2] << 8 | data[3]
            print(eco2, voc)
            if voc < 16: 
                blinkt.set_all(0, 255, 0)
                FadeInOut(0.05)
            elif voc < 60:
                blinkt.set_all(255, 255, 0)
                FadeInOut(0.05)
            else:
                blinkt.set_all(255, 0, 0)
                FadeInOut(0.05)

            if (time.time() - measurement_time) > 900:
                measurement_time = time.time()
                post_data([eco2, voc])
        else:
            if my_ccs811.read_byte(0x00) & 0x01:
                my_ccs811.close()
                my_ccs811 = CCS811()
                my_ccs811.reset()
                time.sleep(1)
                my_ccs811.start_app()
