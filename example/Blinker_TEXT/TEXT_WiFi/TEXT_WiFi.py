# -*- coding: utf-8 -*-

"""
"""

__author__ = 'stao'

from Blinker import Blinker, BlinkerText
from Blinker import BLINKER_LOG, BLINKER_WIFI
from Blinker import millis

TEXT_1 = "tex-pmi"

Blinker.mode(BLINKER_WIFI)
Blinker.begin()

text1 = BlinkerText(TEXT_1)

if __name__ == '__main__':
    while True:
        Blinker.run()

        if Blinker.available() is True:
            BLINKER_LOG('Blinker.readString(): ', Blinker.readString())
            Blinker.print(Blinker.times())
            Blinker.vibrate()

            BlinkerTime = millis()
            Blinker.print(BlinkerTime)
            Blinker.print("millis", millis())

            text1.print("os time", BlinkerTime)
