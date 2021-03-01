#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Blinker import Blinker, BlinkerSlider
from Blinker.BlinkerDebug import *

BLINKER_DEBUG.debugAll()

Blinker.mode("BLINKER_BLE")
Blinker.begin()

slider1 = BlinkerSlider("SliderKey")

def slider1_callback(value):
    """ """

    BLINKER_LOG('Slider read: ', value)

def data_callback(data):
    BLINKER_LOG("Blinker readString: ", data)

    slider1.color('#FFFFFF')
    slider1.print(random.randint(0,255))

slider1.attach(slider1_callback)
Blinker.attachData(data_callback)

if __name__ == '__main__':

    while True:
        Blinker.run()
