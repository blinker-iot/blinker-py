#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import time as _time
import socket
import threading
from Blinker.BlinkerConfig import *
from Blinker.BlinkerDebug import *
from BlinkerUtility.BlinkerUtility import *
# from BlinkerAdapters.BlinkerBLE import *
# from BlinkerAdapters.BlinkerLinuxWS import *
# from BlinkerAdapters.BlinkerMQTT import *
# from threading import Thread
# from zeroconf import ServiceInfo, Zeroconf
# from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

class Protocol():

    def __init__(self):
        self.conType = "BLINKER_WIFI"
        self.proto1 = None
        self.proto2 = None
        self.conn1 = None
        self.conn2 = None
        # self.debug = BLINKER_DEBUG

        self.msgFrom = None
        self.msgBuf = None
        self.sendBuf = ''
        self.isFormat = False
        self.autoFormatFreshTime = millis()
        self.state = CONNECTING

        self.isAvail = False
        self.isRead = False

        self.isThreadStart = False
        self.thread = None

        self.Buttons = {}
        self.Sliders = {}
        self.Toggles = {}
        self.Numbers = {}
        self.Texts = {}

        # self.Joystick = [BLINKER_JOYSTICK_VALUE_DEFAULT, BLINKER_JOYSTICK_VALUE_DEFAULT]
        self.Joystick = {}
        self.Ahrs = [0, 0, 0, False]
        self.GPS = ["0.000000", "0.000000"]
        self.RGB = {}

        self.dataFunc = None
        self.heartbeatFunc = None        
        self.summaryFunc = None

        self.aliType = None
        self.duerType = None

bProto = Protocol()

class BlinkerPY:
    def mode(self, setType = "BLINKER_WIFI"):
        bProto.conType = setType
        if bProto.conType == "BLINKER_BLE":
            import BlinkerAdapters.BlinkerBLE as bBLE

            bProto.proto1 = bBLE
            bProto.conn1 = bProto.proto1.BlinkerBLEService()
        # elif bProto.conType == BLINKER_WIFI:
        #     import BlinkerAdapters.BlinkerLinuxWS as bWS

        #     bProto.proto1 = bWS
        #     bProto.conn1 = bProto.proto1.WebSocketServer()
        elif bProto.conType == "BLINKER_MQTT" or bProto.conType == "BLINKER_WIFI":
            bProto.conType = "BLINKER_MQTT"

            import BlinkerAdapters.BlinkerLinuxWS as bWS
            import BlinkerAdapters as bMQTT

            bProto.proto1 = bMQTT
            bProto.proto2 = bWS
            bProto.conn1 = bProto.proto1.MQTTClient()
            bProto.conn2 = bProto.proto2.WebSocketServer(BLINKER_DIY_MQTT)

    def aliTye(self, _type):
        if _type == BLINKER_ALIGENIE_LIGHT or _type == BLINKER_ALIGENIE_OUTLET or _type == BLINKER_ALIGENIE_SENSOR :
            bProto.aliType = _type

    def duerType(self, _type):
        if _type == BLINKER_DUEROS_LIGHT or _type == BLINKER_DUEROS_OUTLET or _type == BLINKER_DUEROS_SENSOR :
            bProto.duerType = _type
    # def debugLevel(level = BLINKER_DEBUG):
    #     bProto.debug = level

    def begin(self, auth = None):
        if bProto.conType == "BLINKER_BLE":
            # return
            bProto.proto1.bleProto.debug = bProto.debug
            # bProto.conn1.run()
            bProto.conn1.start()
        elif bProto.conType == "BLINKER_WIFI":
            # bProto.proto1.wsProto.debug = bProto.debug
            bProto.conn1.start()
        elif bProto.conType == "BLINKER_MQTT":
            # bProto.proto1.mProto.debug = bProto.debug
            # bProto.proto2.wsProto.debug = bProto.debug
            if auth :
                bProto.msgFrom = "BLINKER_MQTT"
                bProto.conn1.start(auth, bProto.aliType, bProto.duerType)
                bProto.conn2.start(bProto.conn1.bmqtt.deviceName)
                bProto.conn1.run()
            else :
                BLINKER_ERR_LOG('Please input your device secret key!')

    # def thread_run(self):
    #     if bProto.conType == "BLINKER_BLE":
    #         bProto.conn1.run()
    #     while True:
    #         BlinkerPY.checkData(self)

    def checkData(self):
        if bProto.conType == "BLINKER_BLE":
            # return
            bProto.state = bProto.proto1.bleProto.state
            if bProto.proto1.bleProto.isRead is True:
                bProto.msgBuf = bProto.proto1.bleProto.msgBuf
                bProto.isRead = True
                bProto.proto1.bleProto.isRead = False
                BlinkerPY.parse(self)
        elif bProto.conType == "BLINKER_WIFI":
            bProto.state = bProto.proto1.wsProto.state
            if bProto.proto1.wsProto.isRead is True:
                bProto.msgBuf = str(bProto.proto1.wsProto.msgBuf)
                bProto.isRead = True
                bProto.proto1.wsProto.isRead = False
                BlinkerPY.parse(self)
        elif bProto.conType == "BLINKER_MQTT":
            bProto.state = bProto.conn1.bmqtt.state
            if bProto.proto2.wsProto.state is CONNECTED:
                bProto.state = bProto.proto2.wsProto.state
            if bProto.conn1.bmqtt.isRead is True:
                bProto.msgBuf = bProto.conn1.bmqtt.msgBuf
                bProto.msgFrom = "BLINKER_MQTT"
                bProto.isRead = True
                bProto.conn1.bmqtt.isRead = False
                BlinkerPY.parse(self)
            if bProto.proto2.wsProto.isRead is True:
                bProto.msgBuf = str(bProto.proto2.wsProto.msgBuf)
                bProto.msgFrom = "BLINKER_WIFI"
                bProto.isRead = True
                bProto.proto2.wsProto.isRead = False
                BlinkerPY.parse(self)

    def run(self):
        if bProto.isThreadStart is False:
            bProto.thread = threading.Thread(target=thread_run)
            bProto.thread.daemon = True
            bProto.thread.start()
            bProto.isThreadStart = True
        BlinkerPY.checkData(self)
        BlinkerPY.checkAutoFormat(self)
        

    # def wInit(name, wType):
    #     if wType == W_BUTTON:
    #         if name in bProto.Buttons:
    #             return
    #         else:
    #             bProto.Buttons[name] = BLINKER_CMD_BUTTON_RELEASED
    #         # BLINKER_LOG(bProto.Buttons)

    #     elif wType == W_SLIDER:
    #         if name in bProto.Sliders:
    #             return
    #         else:
    #             bProto.Sliders[name] = 0
    #         # BLINKER_LOG(bProto.Sliders)

    #     elif wType == W_TOGGLE:
    #         if name in bProto.Toggles:
    #             return
    #         else:
    #             bProto.Toggles[name] = False

    #     elif wType == W_RGB:
    #         if name in bProto.RGB:
    #             return
    #         else:
    #             rgb = [0, 0, 0]
    #             bProto.RGB[name] = rgb
    #         BLINKER_LOG(bProto.Toggles)

    # def beginFormat():
    #     bProto.isFormat = True
    #     bProto.sendBuf.clear()

    # def endFormat():
    #     bProto.isFormat = False
    #     _print(bProto.sendBuf)
    #     return checkLength(bProto.sendBuf)

    def checkLength(self, data):
        if len(data) > BLINKER_MAX_SEND_SIZE:
            BLINKER_ERR_LOG('SEND DATA BYTES MAX THAN LIMIT!')
            return False
        else:
            return True

    def _print(self, data):
        if BlinkerPY.checkLength(self, data) is False:
            return
        
        if bProto.conType == "BLINKER_BLE":
            bProto.conn1.response(data)
        elif bProto.conType == "BLINKER_WIFI":
            bProto.conn1.broadcast(data)
        elif bProto.conType == "BLINKER_MQTT" and bProto.msgFrom == "BLINKER_MQTT":
            if BLINKER_CMD_NOTICE in data:
                _state = True
            elif BLINKER_CMD_STATE in data:
                _state = True
            else:
                _state = False
            bProto.conn1.pub(data, _state)
        elif bProto.conType == "BLINKER_MQTT" and bProto.msgFrom == "BLINKER_WIFI":
            bProto.conn2.broadcast(data)

        BlinkerPY._parse(self, data)

    def print(self, key, value = None, uint = None):

        if value is None:
            if bProto.isFormat:
                return
            data = str(key)
            BlinkerPY._print(self, data)
        else:
            key = str(key)
            # if not uint is None:
            #     value = str(value) + str(uint)
            # data = json_encode(key, value)
            # data = {}
            if bProto.isFormat == False:
                bProto.isFormat = True
                bProto.autoFormatFreshTime = millis()
            
            if (millis() - bProto.autoFormatFreshTime) < 100 :
                bProto.autoFormatFreshTime = millis()

            buffer = {}

            if bProto.sendBuf is not '' :
                buffer = json.loads(bProto.sendBuf)
            buffer[key] = value
            bProto.sendBuf = json.dumps(buffer)
            # # bProto.sendBuf[key] = value

            # # BLINKER_LOG_ALL("key: ", key, ", value: ", bProto.sendBuf[key])
            BLINKER_LOG_ALL("sendBuf: ", bProto.sendBuf)

        # if bProto.isFormat is False:
        #     _print(data)

    def checkAutoFormat(self):
        if bProto.isFormat :
            if (millis() - bProto.autoFormatFreshTime) >= 100 :
                # payload = {}
                # for key in bProto.sendBuf :
                #     BLINKER_LOG_ALL(key, ", ", bProto.sendBuf[key])
                BlinkerPY._print(self, json.loads(bProto.sendBuf))
                BLINKER_LOG_ALL("auto format: ", json.loads(bProto.sendBuf))
                bProto.sendBuf = ''
                bProto.isFormat = False


    def notify(self, msg):
        BlinkerPY.print(self, BLINKER_CMD_NOTICE, msg)

    def connected(self):
        if bProto.state is CONNECTED:
            return True
        else:
            return False 

    def connect(self, timeout = BLINKER_STREAM_TIMEOUT):
        bProto.state = CONNECTING
        start_time = millis()
        while (millis() - start_time) < timeout:
            BlinkerPY.run(self)
            if bProto.state is CONNECTED:
                return True
        return False

    def disconnect(self):
        bProto.state = DISCONNECTED

    def delay(self, ms):
        start = millis()
        time_run = 0
        while time_run < ms:
            BlinkerPY.run(self)
            time_run = millis() - start

    def available(self):
        return bProto.isAvail

    def attachData(self, func):
        bProto.dataFunc = func

    def attachHeartbeat(self, func):
        bProto.heartbeatFunc = func

    def attachSummary(self, func):
        bProto.summaryFunc = func

    def readString(self):
        bProto.isRead = False
        bProto.isAvail = False
        return bProto.msgBuf

    def times(self):
        return now()

    def parse(self):
        data = bProto.msgBuf
        if not data:
            return
        try:
            data = json.loads(data)
            BLINKER_LOG(data)
            if not isinstance(data, dict):
                raise TypeError()
            for key, value in data.items():
                if key in bProto.Buttons:
                    bProto.isRead = False
                    bProto.Buttons[key].func(data[key])
                elif key in bProto.Sliders:
                    bProto.isRead = False
                    bProto.Sliders[key].func(data[key])
                # elif key in bProto.Toggles:
                #     bProto.isRead = False
                #     bProto.Toggles[key].func(data[key])
                elif key in bProto.RGB:
                    bProto.isRead = False
                    BLINKER_LOG(bProto.RGB[key])
                    bProto.RGB[key].func(data[key][R], data[key][G], data[key][B], data[key][BR])
                elif key in bProto.Joystick:
                    bProto.isRead = False
                    bProto.Joystick[key].func(data[key][J_Xaxis], data[key][J_Yaxis])
                elif key == BLINKER_CMD_AHRS:
                    # bProto.isAvail = False
                    bProto.isRead = False
                    bProto.Ahrs[Yaw] = data[key][Yaw]
                    bProto.Ahrs[Pitch] = data[key][Pitch]
                    bProto.Ahrs[Roll] = data[key][Roll]
                    bProto.Ahrs[AHRS_state] = True
                    # BLINKER_LOG(bProto.Ahrs)
                elif key == BLINKER_CMD_GPS:
                    bProto.isRead = False
                    bProto.GPS[LONG] = str(data[key][LONG])
                    bProto.GPS[LAT] = str(data[key][LAT])

                elif key == BLINKER_CMD_GET and data[key] == BLINKER_CMD_VERSION:
                    bProto.isRead = False
                    BlinkerPY.print(self, BLINKER_CMD_VERSION, BLINKER_VERSION)

                elif key == BLINKER_CMD_GET and data[key] == BLINKER_CMD_STATE:
                    bProto.isRead = False
                    BlinkerPY.heartbeat(self)

        except ValueError:
            pass
        except TypeError:
            pass
        finally:
            if bProto.isRead:
                # bProto.isAvail = 
                if bProto.dataFunc :
                    bProto.dataFunc(data)
                # bProto.isAvail = False


    def _parse(self, data):
        if data is '':
            return
        if check_json_format(data):
            data = json.loads(data)
            for key in data.keys():
                # BLINKER_LOG(key)
                if key in bProto.Buttons:
                    # bProto.isAvail = False
                    bProto.isRead = False
                    if data[key] == BLINKER_CMD_BUTTON_TAP:
                        bProto.Buttons[key] = BLINKER_CMD_BUTTON_TAP
                    elif data[key] == BLINKER_CMD_BUTTON_PRESSED:
                        bProto.Buttons[key] = BLINKER_CMD_BUTTON_PRESSED
                    else:
                        bProto.Buttons[key] = BLINKER_CMD_BUTTON_RELEASED
                    # if data[key] 
                    # BLINKER_LOG(bProto.Buttons)

                elif key in bProto.Sliders:
                    # bProto.isAvail = False
                    bProto.isRead = False
                    bProto.Sliders[key] = data[key]
                    # BLINKER_LOG(bProto.Buttons)

                elif key in bProto.Toggles:
                    # bProto.isAvail = False
                    bProto.isRead = False
                    if data[key] == BLINKER_CMD_ON:
                        bProto.Toggles[key] = True
                    else:
                        bProto.Toggles[key] = False
                    # BLINKER_LOG(bProto.Toggles)

                elif key in bProto.RGB:
                    bProto.isRead = False
                    rgb = [0, 0, 0]
                    rgb[R] = data[key][R]
                    rgb[G] = data[key][G]
                    rgb[B] = data[key][B]
                    bProto.RGB[key] = rgb

    def heartbeat(self):
        if bProto.conType is "BLINKER_MQTT":
            # beginFormat()
            BlinkerPY.print(self, BLINKER_CMD_STATE, BLINKER_CMD_ONLINE)
            if bProto.heartbeatFunc :
                bProto.heartbeatFunc()
            if bProto.summaryFunc :
                bProto.summaryFunc()
            # stateData()
            # if endFormat() is False:
            #     print(BLINKER_CMD_STATE, BLINKER_CMD_ONLINE)
        else:
            # beginFormat()
            BlinkerPY.print(self, BLINKER_CMD_STATE, BLINKER_CMD_CONNECTED)
            if bProto.heartbeatFunc :
                bProto.heartbeatFunc()
            if bProto.summaryFunc :
                bProto.summaryFunc()
            # stateData()
            # if endFormat() is False:
            #     print(BLINKER_CMD_STATE, BLINKER_CMD_CONNECTED)

    def stateData(self):
        for tKey in bProto.Toggles:
            tValue = ''
            if bProto.Toggles[tKey]:
                tValue = 'on'
            else:
                tValue = 'off'
            BlinkerPY.print(self, tKey, tValue)
        for sKey in bProto.Sliders:
            BlinkerPY.print(self, sKey, bProto.Sliders[sKey])
        for rgbKey in bProto.RGB:
            BlinkerPY.print(self, rgbKey, bProto.RGB[rgbKey])


    # def button(self, name):
    #     if not name in bProto.Buttons:
    #         wInit(name, W_BUTTON)
    #         run()

    #     if bProto.Buttons[name] is BLINKER_CMD_BUTTON_RELEASED:
    #         return False
        
    #     if bProto.Buttons[name] is BLINKER_CMD_BUTTON_TAP:
    #         bProto.Buttons[name] = BLINKER_CMD_BUTTON_RELEASED
    #     return True

    # def slider(self, name):
    #     if name in bProto.Sliders:
    #         return bProto.Sliders[name]
    #     else:
    #         wInit(name, W_SLIDER)
    #         run()
    #         return bProto.Sliders[name]

    # def toggle(self, name):
    #     if name in bProto.Toggles:
    #         return bProto.Toggles[name]
    #     else:
    #         wInit(name, W_TOGGLE)
    #         run()
    #         return bProto.Toggles[name]

    # def rgb(name, color):
    #     if name in bProto.RGB:
    #         return bProto.RGB[name][color]
    #     else:
    #         wInit(name, W_RGB)
    #         run()
    #         return bProto.RGB[name][color]

    def joystick(self, axis):
        if axis >= J_Xaxis and axis <= J_Yaxis:
            return bProto.Joystick[axis]
        else:
            return BLINKER_JOYSTICK_VALUE_DEFAULT

    def ahrs(self, axis):
        if axis >= Yaw and axis <= Roll:
            return bProto.Ahrs[axis]
        else:
            return 0

    def attachAhrs(self):
        state = False
        while connected() is False:
            connect()
        BlinkerPY.print(self, BLINKER_CMD_AHRS, BLINKER_CMD_ON)
        delay(100)
        run()
        start_time = millis()
        state = bProto.Ahrs[AHRS_state]
        while state is False:
            if (millis() - start_time) > BLINKER_CONNECT_TIMEOUT_MS:
                BLINKER_LOG("AHRS attach failed...Try again")
                start_time = millis()
                BlinkerPY.print(self, BLINKER_CMD_AHRS, BLINKER_CMD_ON)
                delay(100)
                BlinkerPY.run(self)
            state = bProto.Ahrs[AHRS_state]
        BLINKER_LOG("AHRS attach sucessed...")

    def detachAhrs(self):
        BlinkerPY.print(self, BLINKER_CMD_AHRS, BLINKER_CMD_OFF)
        bProto.Ahrs[Yaw] = 0
        bProto.Ahrs[Roll] = 0
        bProto.Ahrs[Pitch] = 0
        bProto.Ahrs[AHRS_state] = False

    def gps(self, axis):
        BlinkerPY.print(self, BLINKER_CMD_GET, BLINKER_CMD_GPS)
        delay(100)
        run()
        if axis >= LONG and axis <= LAT:
            return bProto.GPS[axis]
        else:
            return "0.000000"

    def vibrate(self, time = 200):
        if time > 1000:
            time = 1000
        BlinkerPY.print(self, BLINKER_CMD_VIBRATE, time)

    def time(self):
        return _time.time()

    def second(self):
        localtime = _time.localtime(_time.time())
        return localtime.tm_sec

    def minute(self):
        localtime = _time.localtime(_time.time())
        return localtime.tm_min

    def hour(self):
        localtime = _time.localtime(_time.time())
        return localtime.tm_hour

    def mday(self):
        localtime = _time.localtime(_time.time())
        return localtime.tm_mday

    def wday(self):
        localtime = _time.localtime(_time.time())
        return (localtime.tm_wday + 1) % 7

    def month(self):
        localtime = _time.localtime(_time.time())
        return localtime.tm_mon

    def year(self):
        localtime = _time.localtime(_time.time())
        return localtime.tm_year

    def yday(self):
        localtime = _time.localtime(_time.time())
        return localtime.tm_yday

    def dtime(self):
        localtime = _time.localtime(_time.time())
        return localtime.tm_hour * 60 * 60 + localtime.tm_min * 60 + localtime.tm_sec

    def sms(self, msg):
        if bProto.conType == "BLINKER_MQTT":
            bProto.conn1.sms(msg)
        else:
            BLINKER_ERR_LOG('This code is intended to run on the MQTT!')

    def push(self, msg):
        if bProto.conType == "BLINKER_MQTT":
            bProto.conn1.push(msg)
        else:
            BLINKER_ERR_LOG('This code is intended to run on the MQTT!')

    def wechat(self, title, state, msg):
        if bProto.conType == "BLINKER_MQTT":
            bProto.conn1.wechat(title, state, msg)
        else:
            BLINKER_ERR_LOG('This code is intended to run on the MQTT!')

    def weather(self, city = 'default'):
        if bProto.conType == "BLINKER_MQTT":
            return bProto.conn1.weather(city)
        else:
            BLINKER_ERR_LOG('This code is intended to run on the MQTT!')

    def aqi(self, city = 'default'):
        if bProto.conType == "BLINKER_MQTT":
            return bProto.conn1.aqi(city)
        else:
            BLINKER_ERR_LOG('This code is intended to run on the MQTT!')

Blinker = BlinkerPY()

def thread_run():
    if bProto.conType == "BLINKER_BLE":
        bProto.conn1.run()
    while True:
        Blinker.checkData()

class BlinkerButton(object):
    """ """

    def __init__(self, name, func=None):
        self.name = name
        self.func = func
        self._icon = ""
        self.iconClr = ""
        self._content = ""
        self._text = ""
        self._text1 = ""
        self.textClr = ""
        self.buttonData = {}

        bProto.Buttons[name] = self

    def icon(self, _icon):
        self._icon = _icon

    def color(self, _clr):
        self.iconClr = _clr

    def content(self, _con):
        self._content = str(_con)

    def text(self, _text1, _text2=None):
        self._text = str(_text1)
        if _text2:
            self._text1 = str(_text2)

    def textColor(self, _clr):
        self.textClr = _clr

    def attach(self, func):
        self.func = func

    def print(self, state=None):

        if state :
            self.buttonData[BLINKER_CMD_SWITCH] = state
        if self._icon:
            self.buttonData[BLINKER_CMD_ICON] = self._icon
        if self.iconClr:
            self.buttonData[BLINKER_CMD_COLOR] = self.iconClr
        if self._content:
            self.buttonData[BLINKER_CMD_CONNECTED] = self._content
        if self._text:
            self.buttonData[BLINKER_CMD_TEXT] = self._text
        if self._text1:
            self.buttonData[BLINKER_CMD_TEXT1] = self._text1
        if self.textClr:
            self.buttonData[BLINKER_CMD_TEXTCOLOR] = self.textClr

        if len(self.buttonData) :
            # data = json.dumps(self.buttonData)
            # data = {self.name: self.buttonData}
            # Blinker._print(data)
            Blinker.print(self.name, self.buttonData)

            self.buttonData.clear()

            self._icon = ""
            self.iconClr = ""
            self._content = ""
            self._text = ""
            self._text1 = ""
            self.textClr = ""


class BlinkerNumber(object):
    """ """

    def __init__(self, name):
        self.name = name
        self._icon = ""
        self._color = ""
        self._unit = ""
        self._text = ""
        self.numberData = {}

        bProto.Numbers[name] = self

    def icon(self, _icon):
        self._icon = _icon

    def color(self, _clr):
        self._color = _clr

    def unit(self, _unit):
        self._unit = _unit
    
    def text(self, _text):
        self._text = _text

    def print(self, value = None):
        if value:
            self.numberData[BLINKER_CMD_VALUE] = value
        if self._icon:
            self.numberData[BLINKER_CMD_ICON] = self._icon
        if self._color:
            self.numberData[BLINKER_CMD_COLOR] = self._color
        if self._unit:
            self.numberData[BLINKER_CMD_UNIT] = self._unit
        if self._text:
            self.numberData[BLINKER_CMD_TEXT] = self._text

        if len(self.numberData) :
            # data = json.dumps(self.numberData)
            # data = {self.name: self.numberData}
            # Blinker._print(data)
            Blinker.print(self.name, self.numberData)

            self.numberData.clear()

            self._icon = ""
            self._color = ""
            self._unit = ""
            self._text = ""


class BlinkerRGB(object):
    """ """

    def __init__(self, name, func=None):
        self.name = name
        self.func = func
        self.rgbbrightness = 0
        self.rgbData = []
        self.registered = False

        bProto.RGB[name] = self

    def attach(self, func):
        self.func = func

    def brightness(self, _bright):
        self.rgbbrightness = _bright

    def print(self, r, g, b, _bright=None):
        self.rgbData.append(r)
        self.rgbData.append(g)
        self.rgbData.append(b)
        if _bright is None:
            self.rgbData.append(self.rgbbrightness)
        else:
            self.rgbData.append(_bright)
        
        # _print(self.rgbData)
        # data = {self.name: self.rgbData}
        # Blinker._print(data)
        Blinker.print(self.name, self.rgbData)


class BlinkerSlider(object):
    """ """

    def __init__(self, name, func=None):
        self.name = name
        self.func = func
        self.textClr = ""
        self.sliderData = {}

        bProto.Sliders[name] = self

    def attach(self, func):
        self.func = func

    def color(self, _clr):
        self.textClr = _clr

    def print(self, value):
        self.sliderData[BLINKER_CMD_VALUE] = value
        if self.textClr:
            self.sliderData[BLINKER_CMD_COLOR] = self.textClr

        # data = json.dumps(self.sliderData)
        # data = {self.name: self.sliderData}
        # Blinker._print(data)
        Blinker.print(self.name, self.sliderData)


class BlinkerText(object):
    """ """

    def __init__(self, name):
        self.name = name
        self.textData = {}

        bProto.Texts[name] = self

    def print(self, text1, text2=None):
        self.textData[BLINKER_CMD_TEXT] = text1
        if text2:
            self.textData[BLINKER_CMD_TEXT1] = text2

        # data = json.dumps(self.textData)        
        # data = {self.name: self.textData}
        # Blinker._print(data)
        Blinker.print(self.name, self.textData)


class BlinkerJoystick(object):
    """ """

    def __init__(self, name, func=None):
        self.name = name
        self.func = func

        bProto.Joystick[name] = self

    def attach(self, _func):
        self.func = _func


class BlinkerSwitch(object):
    """ """

    def __init__(self, name=BLINKER_CMD_BUILTIN_SWITCH, func=None):
        self.name = name
        self.func = func

        bProto.Toggles[name] = self

    def attach(self, _func):
        self.func = _func

    def print(self, _state):
        Blinker.print(self.name, _state)


BUILTIN_SWITCH = BlinkerSwitch()
