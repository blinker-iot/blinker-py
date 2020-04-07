#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Blinker.Blinker import Blinker, BlinkerButton, BlinkerNumber, BlinkerMiot
from Blinker.BlinkerConfig import *
from Blinker.BlinkerDebug import *

auth = 'Your Device Secret Key'

BLINKER_DEBUG.debugAll()

Blinker.mode('BLINKER_WIFI')
Blinker.miType('BLINKER_MIOT_LIGHT')
Blinker.begin(auth)

button1 = BlinkerButton('btn-abc')
number1 = BlinkerNumber('num-abc')

counter = 0
wsState = 'on'
wsMode = BLINKER_CMD_COMMON

def miotPowerState(state):
    ''' '''

    BLINKER_LOG('need set power state: ', state)

    BlinkerMiot.powerState(state)
    BlinkerMiot.print()

def miotColor(color):
    ''' '''

    BLINKER_LOG('need set color: ', color)

    # if color == 'Red':
    #     # your codes
    # elif color == 'Yellow':
    #     # your codes
    # elif color == 'Blue':
    #     # your codes
    # elif color == 'Green':
    #     # your codes
    # elif color == 'White':
    #     # your codes
    # elif color == 'Black':
    #     # your codes
    # elif color == 'Cyan':
    #     # your codes
    # elif color == 'Purple':
    #     # your codes
    # elif color == 'Orange':
    #     # your codes

    BlinkerMiot.color(color)
    BlinkerMiot.print()

def miotMode(mode):
    ''' '''

    BLINKER_LOG('need set mode: ', mode)

    # if mode == BLINKER_CMD_Miot_READING:
    #     # Your mode function
    # elif mode == BLINKER_CMD_Miot_MOVIE:
    #     # Your mode function
    # elif mode == BLINKER_CMD_Miot_SLEEP:
    #     # Your mode function
    # elif mode == BLINKER_CMD_Miot_HOLIDAY:
    #     # Your mode function
    # elif mode == BLINKER_CMD_Miot_MUSIC:
    #     # Your mode function
    # elif mode == BLINKER_CMD_Miot_COMMON:
    #     # Your mode function

    BlinkerMiot.mode(mode)
    BlinkerMiot.print()

def miotcMode(cmode):
    ''' '''

    BLINKER_LOG('need cancel mode: ', cmode)

    # if mode == BLINKER_CMD_Miot_READING:
    #     # Your mode function
    # elif mode == BLINKER_CMD_Miot_MOVIE:
    #     # Your mode function
    # elif mode == BLINKER_CMD_Miot_SLEEP:
    #     # Your mode function
    # elif mode == BLINKER_CMD_Miot_HOLIDAY:
    #     # Your mode function
    # elif mode == BLINKER_CMD_Miot_MUSIC:
    #     # Your mode function
    # elif mode == BLINKER_CMD_Miot_COMMON:
    #     # Your mode function

    BlinkerMiot.mode(cMode)
    BlinkerMiot.print()

def miotBright(bright):
    ''' '''

    BLINKER_LOG('need set brightness: ', bright)

    BlinkerMiot.brightness(bright)
    BlinkerMiot.print()


def miotColorTemp(colorTemp):
    ''' '''

    BLINKER_LOG('need set colorTemperature: ', colorTemp)

    BlinkerMiot.colorTemp(colorTemp)
    BlinkerMiot.print()

def miotQuery(queryCode):
    ''' '''

    BLINKER_LOG('Miot Query codes: ', queryCode)

    if queryCode == BLINKER_CMD_QUERY_ALL_NUMBER :
        BLINKER_LOG('Miot Query All')
        BlinkerMiot.powerState(wsState)
        BlinkerMiot.color(getColor())
        BlinkerMiot.mode(wsMode)
        BlinkerMiot.colorTemp(50)
        BlinkerMiot.brightness(100)
        BlinkerMiot.print()
    elif queryCode == BLINKER_CMD_QUERY_POWERSTATE_NUMBER :
        BLINKER_LOG('Miot Query Power State')
        BlinkerMiot.powerState(wsState)
        BlinkerMiot.print()
    elif queryCode == BLINKER_CMD_QUERY_COLOR_NUMBER :
        BLINKER_LOG('Miot Query Color')
        BlinkerMiot.color('red')
        BlinkerMiot.print()
    elif queryCode == BLINKER_CMD_QUERY_MODE_NUMBER :
        BLINKER_LOG('Miot Query Mode')
        BlinkerMiot.mode(wsMode)
        BlinkerMiot.print()
    elif queryCode == BLINKER_CMD_QUERY_COLORTEMP_NUMBER :
        BLINKER_LOG('Miot Query ColorTemperature')
        BlinkerMiot.colorTemp(50)
        BlinkerMiot.print()
    elif queryCode == BLINKER_CMD_QUERY_BRIGHTNESS_NUMBER :
        BLINKER_LOG('Miot Query Brightness')
        BlinkerMiot.brightness(100)
        BlinkerMiot.print()
    else :
        BlinkerMiot.powerState(wsState)
        BlinkerMiot.color('red')
        BlinkerMiot.mode(wsMode)
        BlinkerMiot.colorTemp(50)
        BlinkerMiot.brightness(100)
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
BlinkerMiot.attachColor(miotColor)
BlinkerMiot.attachMode(miotMode)
BlinkerMiot.attachCancelMode(miotcMode)
BlinkerMiot.attachBrightness(miotBright)
BlinkerMiot.attachColorTemperature(miotColorTemp)
BlinkerMiot.attachQuery(miotQuery)

if __name__ == '__main__':

    while True:
        Blinker.run()
