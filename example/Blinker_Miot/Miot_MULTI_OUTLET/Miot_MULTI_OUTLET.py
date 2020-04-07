#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Blinker.Blinker import Blinker, BlinkerButton, BlinkerNumber, BlinkerMiot
from Blinker.BlinkerConfig import *
from Blinker.BlinkerDebug import *

auth = 'Your Device Secret Key'

BLINKER_DEBUG.debugAll()

Blinker.mode('BLINKER_WIFI')
Blinker.miType('BLINKER_MIOT_MULTI_OUTLET')
Blinker.begin(auth)

button1 = BlinkerButton('btn-abc')
number1 = BlinkerNumber('num-abc')

counter = 0
wsState = ['off', 'off', 'off', 'off', 'off']

def miotPowerState(state, num):
    ''' '''

    BLINKER_LOG("need set outlet: ", num, ", power state: ", state)

    global wsState
    wsState[num] = state

    if num == 0 and state == 'false':
        for i in len(wsState):
            wsState[i] = state

    BlinkerMiot.powerState(state, num)
    BlinkerMiot.print()

def miotQuery(queryCode, num):
    ''' '''

    BLINKER_LOG("Miot Query outlet: ", num,", codes: ", queryCode)

    global wsState
    state = 'off'
    
    for i, val in enumerate(wsState) :
        if i == num :
            state = val

    if queryCode == BLINKER_CMD_QUERY_ALL_NUMBER :
        BLINKER_LOG('Miot Query All')
        BlinkerMiot.powerState(state, num)
        BlinkerMiot.print()
    elif queryCode == BLINKER_CMD_QUERY_POWERSTATE_NUMBER :
        BlinkerMiot.powerState(state, num)
        BlinkerMiot.print()
    else :
        BlinkerMiot.powerState(state, num)
        BlinkerMiot.print()

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

BlinkerMiot.attachPowerState(miotPowerState)
BlinkerMiot.attachQuery(miotQuery)

if __name__ == '__main__':

    while True:
        Blinker.run()

