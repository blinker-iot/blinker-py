#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Blinker import Blinker, BlinkerButton, BlinkerNumber
from Blinker.BlinkerDebug import *

BLINKER_DEBUG.debugAll()

Blinker.mode("BLINKER_BLE")
Blinker.begin()

button1 = BlinkerButton("btn-abc")
number1 = BlinkerNumber("num-abc")

counter = 0

def button1_callback(state):
    """ """

    BLINKER_LOG('get button state: ', state)

    button1.icon('icon_1')
    button1.color('#FFFFFF')
    button1.text('Your button name or describe')
    button1.print("on")

def data_callback(data):
    global counter

    BLINKER_LOG("Blinker readString: ", data)
    counter += 1
    number1.print(counter)

def heartbeat_callback():
    global counter

    button1.icon('icon_1')
    button1.color('#FFFFFF')
    button1.text('Your button name or describe')
    button1.print("on")

    number1.print(counter)

button1.attach(button1_callback)
Blinker.attachData(data_callback)
Blinker.attachHeartbeat(heartbeat_callback)

if __name__ == '__main__':

    while True:
        Blinker.run()
