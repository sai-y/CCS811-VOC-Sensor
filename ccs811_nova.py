from ccs811 import CCS811
from Hologram.HologramCloud import HologramCloud
import time

hologram = HologramCloud(dict(), network='cellular' )

def post_data(data):
    try:
        hologram.sendMessage(
            data,
            topics=['VOC'],
            timeout=3
        )
    except:
        print("Error!")
    return 0


if __name__ == "__main__":
    my_ccs811 = CCS811()
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

            eco2 = str(data[0] << 8 | data[1])
            voc = str(data[2] << 8 | data[3])
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

            if (time.time() - measurement_time) > 90:
                measurement_time = time.time()
                post_data(eco2 + ", " + voc)
        else:
            if my_ccs811.read_byte(0x00) & 0x01:
                my_ccs811.close()
                my_ccs811 = CCS811()
                my_ccs811.reset()
                time.sleep(1)
                my_ccs811.start_app()
