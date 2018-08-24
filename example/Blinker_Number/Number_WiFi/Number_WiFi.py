# -*- coding: utf-8 -*-

"""
"""

__author__ = 'stao'

from Blinker import Blinker, BlinkerNumber
from Blinker import BLINKER_LOG, BLINKER_WIFI
from Blinker import millis

NUMBER_1 = "NUMKey"

Blinker.setMode(BLINKER_WIFI)
Blinker.begin()

number1 = BlinkerNumber(NUMBER_1)

if __name__ == '__main__':

    while True:
        Blinker.run()

        if Blinker.available() is True:
            BLINKER_LOG('Blinker.readString(): ', Blinker.readString())
            Blinker.print(Blinker.times())
            Blinker.vibrate()
            Blinker.print('millis', millis())

            number1.icon("icon_1")
            number1.color("#FFFFFF")
            number1.unit("ms")
            number1.print(millis())

        Blinker.delay(2000)
