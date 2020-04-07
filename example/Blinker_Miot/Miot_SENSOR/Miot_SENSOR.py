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

counter = 0

def miQuery(queryCode):
    ''' '''

    BLINKER_LOG('MIOT Query codes: ', queryCode)

    if queryCode == BLINKER_CMD_QUERY_ALL_NUMBER :
        BLINKER_LOG('MIOT Query All')
        BlinkerMiot.temp(20)
        BlinkerMiot.humi(21)
        BlinkerMiot.pm25(22)
        BlinkerMiot.print()
    else :
        BlinkerMiot.temp(23)
        BlinkerMiot.humi(24)
        BlinkerMiot.pm25(25)
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

if __name__ == '__main__':

    while True:
        Blinker.run()