#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Blinker.Blinker import Blinker, BlinkerButton, BlinkerNumber, BlinkerMiot
from Blinker.BlinkerConfig import *
from Blinker.BlinkerDebug import *

auth = 'Your Device Secret Key' #

BLINKER_DEBUG.debugAll()

Blinker.mode('BLINKER_WIFI')
Blinker.miType('BLINKER_MIOT_SENSOR') # BLINKER_MIOT_LIGHT 灯, BLINKER_MIOT_OUTLET 插座, BLINKER_MIOT_MULTI_OUTLET 多口插座, BLINKER_MIOT_SENSOR 传感器
Blinker.begin(auth)

button1 = BlinkerButton('btn-abc')
number1 = BlinkerNumber('num-abc')
wsState = 'on'

counter = 0

def miotPowerState(state):
    ''' '''

    BLINKER_LOG('need set power state: ', state)
    wsState = state  and 'on' or 'off'
    BlinkerMiot.powerState(wsState)
    BlinkerMiot.print()
    
def miQuery(queryCode):
    ''' '''

    BLINKER_LOG('MIOT Query codes: ', queryCode)

    if queryCode == BLINKER_CMD_QUERY_ALL_NUMBER :
        BLINKER_LOG('MIOT Query All')
        BlinkerMiot.powerState(wsState)
        BlinkerMiot.aqi(19)
        BlinkerMiot.temp(20)
        BlinkerMiot.humi(21)
        BlinkerMiot.pm25(22)
        BlinkerMiot.co2(23)
        BlinkerMiot.print()
    elif queryCode == BLINKER_CMD_QUERY_POWERSTATE_NUMBER :
        BLINKER_LOG('Miot Query Power State')
        BlinkerMiot.powerState(wsState)
        BlinkerMiot.print()
    else :
        BlinkerMiot.powerState(wsState)
        BlinkerMiot.aqi(24)
        BlinkerMiot.temp(25)
        BlinkerMiot.humi(26)
        BlinkerMiot.pm25(27)
        BlinkerMiot.co2(28)
        BlinkerMiot.print()

def button1_callback(state):
    ''' '''

    BLINKER_LOG('get button state: ', state)

    button1.icon('icon_1')
    button1.color('#FFFFFF')
    button1.text(u'设备返回的text')
    button1.print(state)


def data_callback(data):
    global counter

    BLINKER_LOG('Blinker readString: ', data)
    counter += 1
    number1.print(counter)

button1.attach(button1_callback)
Blinker.attachData(data_callback)

BlinkerMiot.attachQuery(miQuery)
BlinkerMiot.attachPowerState(miotPowerState)

if __name__ == '__main__':

    while True:
        Blinker.run()