# -*- coding: utf-8 -*-

"""
"""

__author__ = 'stao'

from Blinker import Blinker, BUILTIN_SWITCH
from Blinker import BLINKER_LOG, BLINKER_WIFI, BLINKER_CMD_ON
from Blinker import millis

Blinker.setMode(BLINKER_WIFI)
Blinker.begin()


def switch_callback(state):
    BLINKER_LOG("get switch state: ", state)

    if state == BLINKER_CMD_ON:
        BUILTIN_SWITCH.print("on")
    else:
        BUILTIN_SWITCH.print("off")


BUILTIN_SWITCH.attach(switch_callback)

if __name__ == '__main__':
    while True:
        Blinker.run()

        if Blinker.available() is True:
            BLINKER_LOG('Blinker.readString(): ', Blinker.readString())

            Blinker.vibrate()

            BlinkerTime = millis()
            Blinker.print(BlinkerTime)
            Blinker.print("millis", BlinkerTime)

        Blinker.delay(2000)
