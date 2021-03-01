#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Blinker.Blinker import Blinker, BlinkerButton, BlinkerNumber, BlinkerDuerOS
from Blinker.BlinkerConfig import *
from Blinker.BlinkerDebug import *

auth = 'Your Device Secret Key'

BLINKER_DEBUG.debugAll()

Blinker.mode('BLINKER_WIFI')
Blinker.duerType('BLINKER_DUEROS_SENSOR')
Blinker.begin(auth)

button1 = BlinkerButton('btn-abc')
number1 = BlinkerNumber('num-abc')

counter = 0

def duerQuery(queryCode):
    ''' '''

    BLINKER_LOG('DuerOS Query codes: ', queryCode)

    if queryCode == BLINKER_CMD_QUERY_AQI_NUMBER :
        BLINKER_LOG("DuerOS Query AQI")
        BlinkerDuerOS.aqi(20)
        BlinkerDuerOS.print()
    elif queryCode == BLINKER_CMD_QUERY_CO2_NUMBER :
        BLINKER_LOG("DuerOS Query CO2")
        BlinkerDuerOS.co2(20)
        BlinkerDuerOS.print()
    elif queryCode == BLINKER_CMD_QUERY_PM10_NUMBER :
        BLINKER_LOG("DuerOS Query CO2")
        BlinkerDuerOS.pm10(20)
        BlinkerDuerOS.print()
    elif queryCode == BLINKER_CMD_QUERY_PM25_NUMBER :
        BLINKER_LOG("DuerOS Query CO2")
        BlinkerDuerOS.pm25(20)
        BlinkerDuerOS.print()
    elif queryCode == BLINKER_CMD_QUERY_HUMI_NUMBER :
        BLINKER_LOG("DuerOS Query CO2")
        BlinkerDuerOS.humi(20)
        BlinkerDuerOS.print()
    elif queryCode == BLINKER_CMD_QUERY_TEMP_NUMBER :
        BLINKER_LOG("DuerOS Query CO2")
        BlinkerDuerOS.temp(20)
        BlinkerDuerOS.print()
    elif queryCode == BLINKER_CMD_QUERY_TIME_NUMBER :
        BLINKER_LOG("DuerOS Query CO2")
        BlinkerDuerOS.time(millis())
        BlinkerDuerOS.print()
    else :        
        BlinkerDuerOS.temp(20)
        BlinkerDuerOS.humi(20)
        BlinkerDuerOS.pm25(20)
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

BlinkerDuerOS.attachQuery(duerQuery)

if __name__ == '__main__':

    while True:
        Blinker.run()
