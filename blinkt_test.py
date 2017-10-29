#!/usr/bin/python

import blinkt
from time import sleep

while True:
    blinkt.set_all(255, 0 , 0)
    sleep(1)
    blinkt.set_all(0, 255, 0)
    sleep(1)
    blinkt.set_all(0, 0, 255)
    sleep(1)