#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Blinker.Blinker import Blinker, BlinkerButton, BlinkerNumber, BlinkerAliGenie
from Blinker.BlinkerConfig import *
from Blinker.BlinkerDebug import *

auth = 'Your Device Secret Key'

BLINKER_DEBUG.debugAll()

Blinker.mode('BLINKER_WIFI')
Blinker.aliType('BLINKER_ALIGENIE_SENSOR')
Blinker.begin(auth)

button1 = BlinkerButton('btn-abc')
number1 = BlinkerNumber('num-abc')

counter = 0

def aligenieQuery(queryCode):
    ''' '''

    BLINKER_LOG('AliGenie Query codes: ', queryCode)

    if queryCode == BLINKER_CMD_QUERY_ALL_NUMBER :
        BLINKER_LOG('AliGenie Query All')
        BlinkerAliGenie.temp(20)
        BlinkerAliGenie.humi(20)
        BlinkerAliGenie.pm25(20)
        BlinkerAliGenie.print()
    else :        
        BlinkerAliGenie.temp(20)
        BlinkerAliGenie.humi(20)
        BlinkerAliGenie.pm25(20)
        BlinkerAliGenie.print()

def button1_callback(state):
    ''' '''

    BLINKER_LOG('get button state: ', state)

    button1.icon('icon_1')
    button1.color('#FFFFFF')
    button1.text('Your button name or describe')
    button1.print(state)


def data_callback(data):
    global counter
    
    BLINKER_LOG('Blinker readString: ', data)
    counter += 1
    number1.print(counter)

button1.attach(button1_callback)
Blinker.attachData(data_callback)

BlinkerAliGenie.attachQuery(aligenieQuery)

if __name__ == '__main__':

    while True:
        Blinker.run()
