#!/usr/bin/python

import blinkt
from time import sleep

while True:
    blinkt.set_all(255, 0 , 0)
    blinskt.show()
    sleep(1)
    blinkt.set_all(0, 255, 0)
    blinkt.show()
    sleep(1)