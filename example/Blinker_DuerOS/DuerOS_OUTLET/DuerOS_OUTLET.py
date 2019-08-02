#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Blinker.Blinker import Blinker, BlinkerButton, BlinkerNumber, BlinkerDuerOS
from Blinker.BlinkerConfig import *
from Blinker.BlinkerDebug import *

auth = 'Your Device Secret Key'

BLINKER_DEBUG.debugAll()

Blinker.mode('BLINKER_WIFI')
Blinker.duerType('BLINKER_DUEROS_OUTLET')
Blinker.begin(auth)

button1 = BlinkerButton('btn-abc')
number1 = BlinkerNumber('num-abc')

counter = 0
oState = 'on'

def duerPowerState(state):
    ''' '''

    BLINKER_LOG('need set power state: ', state)

    BlinkerDuerOS.powerState(state)
    BlinkerDuerOS.print()

def duerQuery(queryCode):
    ''' '''

    BLINKER_LOG('DuerOS Query codes: ', queryCode)

    if queryCode == BLINKER_CMD_QUERY_TIME_NUMBER :
        BLINKER_LOG("DuerOS Query time")
        BlinkerDuerOS.time(millis())
        BlinkerDuerOS.print()
    else :
        BlinkerDuerOS.time(millis())
        BlinkerDuerOS.print()

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

BlinkerDuerOS.attachPowerState(duerPowerState)
BlinkerDuerOS.attachQuery(duerQuery)

if __name__ == '__main__':

    while True:
        Blinker.run()
