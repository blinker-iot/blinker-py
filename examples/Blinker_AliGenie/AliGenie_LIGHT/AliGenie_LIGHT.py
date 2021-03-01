#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Blinker.Blinker import Blinker, BlinkerButton, BlinkerNumber, BlinkerAliGenie
from Blinker.BlinkerConfig import *
from Blinker.BlinkerDebug import *

auth = 'Your Device Secret Key'

BLINKER_DEBUG.debugAll()

Blinker.mode('BLINKER_WIFI')
Blinker.aliType('BLINKER_ALIGENIE_LIGHT')
Blinker.begin(auth)

button1 = BlinkerButton('btn-abc')
number1 = BlinkerNumber('num-abc')

counter = 0
wsState = 'on'
wsMode = BLINKER_CMD_COMMON

def aligeniePowerState(state):
    ''' '''

    BLINKER_LOG('need set power state: ', state)

    BlinkerAliGenie.powerState(state)
    BlinkerAliGenie.print()

def aligenieColor(color):
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

    BlinkerAliGenie.color(color)
    BlinkerAliGenie.print()

def aligenieMode(mode):
    ''' '''

    BLINKER_LOG('need set mode: ', mode)

    # if mode == BLINKER_CMD_ALIGENIE_READING:
    #     # Your mode function
    # elif mode == BLINKER_CMD_ALIGENIE_MOVIE:
    #     # Your mode function
    # elif mode == BLINKER_CMD_ALIGENIE_SLEEP:
    #     # Your mode function
    # elif mode == BLINKER_CMD_ALIGENIE_HOLIDAY:
    #     # Your mode function
    # elif mode == BLINKER_CMD_ALIGENIE_MUSIC:
    #     # Your mode function
    # elif mode == BLINKER_CMD_ALIGENIE_COMMON:
    #     # Your mode function

    BlinkerAliGenie.mode(mode)
    BlinkerAliGenie.print()

def aligeniecMode(cmode):
    ''' '''

    BLINKER_LOG('need cancel mode: ', cmode)

    # if mode == BLINKER_CMD_ALIGENIE_READING:
    #     # Your mode function
    # elif mode == BLINKER_CMD_ALIGENIE_MOVIE:
    #     # Your mode function
    # elif mode == BLINKER_CMD_ALIGENIE_SLEEP:
    #     # Your mode function
    # elif mode == BLINKER_CMD_ALIGENIE_HOLIDAY:
    #     # Your mode function
    # elif mode == BLINKER_CMD_ALIGENIE_MUSIC:
    #     # Your mode function
    # elif mode == BLINKER_CMD_ALIGENIE_COMMON:
    #     # Your mode function

    BlinkerAliGenie.mode(cMode)
    BlinkerAliGenie.print()

def aligenieBright(bright):
    ''' '''

    BLINKER_LOG('need set brightness: ', bright)

    BlinkerAliGenie.brightness(bright)
    BlinkerAliGenie.print()

def aligenieRelativeBright(bright):
    ''' '''

    BLINKER_LOG('need set relative brightness: ', bright)

    BlinkerAliGenie.brightness(bright)
    BlinkerAliGenie.print()

def aligenieColorTemp(colorTemp):
    ''' '''

    BLINKER_LOG('need set colorTemperature: ', colorTemp)

    BlinkerAliGenie.colorTemp(colorTemp)
    BlinkerAliGenie.print()

def aligenieRelativeColorTemp(colorTemp):
    ''' '''

    BLINKER_LOG('need set relative colorTemperature: ', colorTemp)

    BlinkerAliGenie.colorTemp(colorTemp)
    BlinkerAliGenie.print()

def aligenieQuery(queryCode):
    ''' '''

    BLINKER_LOG('AliGenie Query codes: ', queryCode)

    if queryCode == BLINKER_CMD_QUERY_ALL_NUMBER :
        BLINKER_LOG('AliGenie Query All')
        BlinkerAliGenie.powerState(wsState)
        BlinkerAliGenie.color(getColor())
        BlinkerAliGenie.mode(wsMode)
        BlinkerAliGenie.colorTemp(50)
        BlinkerAliGenie.brightness(100)
        BlinkerAliGenie.print()
    elif queryCode == BLINKER_CMD_QUERY_POWERSTATE_NUMBER :
        BLINKER_LOG('AliGenie Query Power State')
        BlinkerAliGenie.powerState(wsState)
        BlinkerAliGenie.print()
    elif queryCode == BLINKER_CMD_QUERY_COLOR_NUMBER :
        BLINKER_LOG('AliGenie Query Color')
        BlinkerAliGenie.color('red')
        BlinkerAliGenie.print()
    elif queryCode == BLINKER_CMD_QUERY_MODE_NUMBER :
        BLINKER_LOG('AliGenie Query Mode')
        BlinkerAliGenie.mode(wsMode)
        BlinkerAliGenie.print()
    elif queryCode == BLINKER_CMD_QUERY_COLORTEMP_NUMBER :
        BLINKER_LOG('AliGenie Query ColorTemperature')
        BlinkerAliGenie.colorTemp(50)
        BlinkerAliGenie.print()
    elif queryCode == BLINKER_CMD_QUERY_BRIGHTNESS_NUMBER :
        BLINKER_LOG('AliGenie Query Brightness')
        BlinkerAliGenie.brightness(100)
        BlinkerAliGenie.print()
    else :
        BlinkerAliGenie.powerState(wsState)
        BlinkerAliGenie.color('red')
        BlinkerAliGenie.mode(wsMode)
        BlinkerAliGenie.colorTemp(50)
        BlinkerAliGenie.brightness(100)
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

BlinkerAliGenie.attachPowerState(aligeniePowerState)
BlinkerAliGenie.attachColor(aligenieColor)
BlinkerAliGenie.attachMode(aligenieMode)
BlinkerAliGenie.attachCancelMode(aligeniecMode)
BlinkerAliGenie.attachBrightness(aligenieBright)
BlinkerAliGenie.attachRelativeBrightness(aligenieRelativeBright)
BlinkerAliGenie.attachColorTemperature(aligenieColorTemp)
BlinkerAliGenie.attachRelativeColorTemperature(aligenieRelativeColorTemp)
BlinkerAliGenie.attachQuery(aligenieQuery)

if __name__ == '__main__':

    while True:
        Blinker.run()
