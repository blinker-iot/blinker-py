#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Blinker.Blinker import Blinker, BlinkerButton, BlinkerNumber, BlinkerDuerOS
from Blinker.BlinkerConfig import *
from Blinker.BlinkerDebug import *

auth = 'Your Device Secret Key'

BLINKER_DEBUG.debugAll()

Blinker.mode('BLINKER_WIFI')
Blinker.duerType('BLINKER_DUEROS_LIGHT')
Blinker.begin(auth)

button1 = BlinkerButton('btn-abc')
number1 = BlinkerNumber('num-abc')

counter = 0
wsState = 'on'
wsMode = BLINKER_CMD_COMMON

def duerPowerState(state):
    ''' '''

    BLINKER_LOG('need set power state: ', state)

    BlinkerDuerOS.powerState(state)
    BlinkerDuerOS.print()

def duerColor(color):
    ''' '''

    BLINKER_LOG('need set color: ', color)

    # if color == 0xFF0000: # 'Red':
    #     # your codes
    # elif color == 0xFFFF00: # 'Yellow':
    #     # your codes
    # elif color == 0x0000FF: # 'Blue':
    #     # your codes
    # elif color == 0x00FF00: # 'Green':
    #     # your codes
    # elif color == 0xFFFFFF: # 'White':
    #     # your codes
    # elif color == 0x000000: # 'Black':
    #     # your codes
    # elif color == 0x00FFFF: # 'Cyan':
    #     # your codes
    # elif color == 0x800080: # 'Purple':
    #     # your codes
    # elif color == 0xFFA500: # 'Orange':
    #     # your codes

    BlinkerDuerOS.color(color)
    BlinkerDuerOS.print()

def duerMode(mode):
    ''' '''

    BLINKER_LOG('need set mode: ', mode)

    # if mode == BLINKER_CMD_DUEROS_READING:
    #     # Your mode function
    # elif mode == BLINKER_CMD_DUEROS_SLEEP:
    #     # Your mode function
    # elif mode == BLINKER_CMD_DUEROS_ALARM:
    #     # Your mode function
    # elif mode == BLINKER_CMD_DUEROS_NIGHT_LIGHT:
    #     # Your mode function
    # elif mode == BLINKER_CMD_DUEROS_ROMANTIC:
    #     # Your mode function
    # elif mode == BLINKER_CMD_DUEROS_READING:
    #     # Your mode function

    BlinkerDuerOS.mode(mode)
    BlinkerDuerOS.print()

def duercMode(cmode):
    ''' '''

    BLINKER_LOG('need cancel mode: ', cmode)

    # if mode == BLINKER_CMD_DUEROS_READING:
    #     # Your mode function
    # elif mode == BLINKER_CMD_DUEROS_SLEEP:
    #     # Your mode function
    # elif mode == BLINKER_CMD_DUEROS_ALARM:
    #     # Your mode function
    # elif mode == BLINKER_CMD_DUEROS_NIGHT_LIGHT:
    #     # Your mode function
    # elif mode == BLINKER_CMD_DUEROS_ROMANTIC:
    #     # Your mode function
    # elif mode == BLINKER_CMD_DUEROS_READING:
    #     # Your mode function

    BlinkerDuerOS.mode(cMode)
    BlinkerDuerOS.print()

def duerBright(bright):
    ''' '''

    BLINKER_LOG('need set brightness: ', bright)

    BlinkerDuerOS.brightness(bright)
    BlinkerDuerOS.print()

def duerRelativeBright(bright):
    ''' '''

    BLINKER_LOG('need set relative brightness: ', bright)

    BlinkerDuerOS.brightness(bright)
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
BlinkerDuerOS.attachColor(duerColor)
BlinkerDuerOS.attachMode(duerMode)
BlinkerDuerOS.attachCancelMode(duercMode)
BlinkerDuerOS.attachBrightness(duerBright)
BlinkerDuerOS.attachRelativeBrightness(duerRelativeBright)
BlinkerDuerOS.attachQuery(duerQuery)

if __name__ == '__main__':

    while True:
        Blinker.run()
