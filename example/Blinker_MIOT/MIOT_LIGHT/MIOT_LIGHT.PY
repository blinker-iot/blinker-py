#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Blinker.Blinker import Blinker, BlinkerButton, BlinkerNumber, BlinkerMIOT
from Blinker.BlinkerConfig import *
from Blinker.BlinkerDebug import *

auth = 'Your Device Secret Key'

BLINKER_DEBUG.debugAll()

Blinker.mode('BLINKER_WIFI')
Blinker.miotType('BLINKER_MIOT_LIGHT')
Blinker.begin(auth)

button1 = BlinkerButton('btn-abc')
number1 = BlinkerNumber('num-abc')

counter = 0
wsState = 'on'
wsMode = BLINKER_CMD_COMMON

def miotPowerState(state):
    ''' '''

    BLINKER_LOG('need set power state: ', state)

    BlinkerMIOT.powerState(state)
    BlinkerMIOT.print()

def miotColor(color):
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

    BlinkerMIOT.color(color)
    BlinkerMIOT.print()

def miotMode(mode):
    ''' '''

    BLINKER_LOG('need set mode: ', mode)

    # if mode == BLINKER_CMD_MIOT_READING:
    #     # Your mode function
    # elif mode == BLINKER_CMD_MIOT_SLEEP:
    #     # Your mode function
    # elif mode == BLINKER_CMD_MIOT_ALARM:
    #     # Your mode function
    # elif mode == BLINKER_CMD_MIOT_NIGHT_LIGHT:
    #     # Your mode function
    # elif mode == BLINKER_CMD_MIOT_ROMANTIC:
    #     # Your mode function
    # elif mode == BLINKER_CMD_MIOT_READING:
    #     # Your mode function

    BlinkerMIOT.mode(mode)
    BlinkerMIOT.print()

def miotBright(bright):
    ''' '''

    BLINKER_LOG('need set brightness: ', bright)

    BlinkerMIOT.brightness(bright)
    BlinkerMIOT.print()

def miotQuery(queryCode):
    ''' '''

    BLINKER_LOG('MIOT Query codes: ', queryCode)

    if queryCode == BLINKER_CMD_QUERY_ALL_NUMBER :
        BLINKER_LOG('MIOT Query All')
        BlinkerMIOT.powerState(wsState)
        BlinkerMIOT.color(getColor())
        BlinkerMIOT.mode(wsMode)
        BlinkerMIOT.colorTemp(50)
        BlinkerMIOT.brightness(100)
        BlinkerMIOT.print()
    elif queryCode == BLINKER_CMD_QUERY_POWERSTATE_NUMBER :
        BLINKER_LOG('MIOT Query Power State')
        BlinkerMIOT.powerState(wsState)
        BlinkerMIOT.print()
    elif queryCode == BLINKER_CMD_QUERY_COLOR_NUMBER :
        BLINKER_LOG('MIOT Query Color')
        BlinkerMIOT.color('red')
        BlinkerMIOT.print()
    elif queryCode == BLINKER_CMD_QUERY_MODE_NUMBER :
        BLINKER_LOG('MIOT Query Mode')
        BlinkerMIOT.mode(wsMode)
        BlinkerMIOT.print()
    elif queryCode == BLINKER_CMD_QUERY_COLORTEMP_NUMBER :
        BLINKER_LOG('MIOT Query ColorTemperature')
        BlinkerMIOT.colorTemp(50)
        BlinkerMIOT.print()
    elif queryCode == BLINKER_CMD_QUERY_BRIGHTNESS_NUMBER :
        BLINKER_LOG('MIOT Query Brightness')
        BlinkerMIOT.brightness(100)
        BlinkerMIOT.print()
    else :
        BlinkerMIOT.powerState(wsState)
        BlinkerMIOT.color('red')
        BlinkerMIOT.mode(wsMode)
        BlinkerMIOT.colorTemp(50)
        BlinkerMIOT.brightness(100)
        BlinkerMIOT.print()

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

BlinkerMIOT.attachPowerState(miotPowerState)
BlinkerMIOT.attachColor(miotColor)
BlinkerMIOT.attachMode(miotMode)
BlinkerMIOT.attachBrightness(miotBright)
BlinkerMIOT.attachRelativeBrightness(miotRelativeBright)
BlinkerMIOT.attachQuery(miotQuery)

if __name__ == '__main__':

    while True:
        Blinker.run()
