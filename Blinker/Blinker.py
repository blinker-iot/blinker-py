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
        self.Datas = {}

        self.dataTime = BLINKER_DATA_FREQ_TIME
        self.dataCount = 0
        self.dataTimes = 0
        self.dataTimesLimit = 0
        self.dataStorageFunc = None

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
        self.miType = None

        self.aliPowerSrareFunc = None
        self.aliSetColorFunc = None
        self.aliSetModeFunc = None
        self.aliSetcModeFunc = None
        self.aliSetBrightFunc = None
        self.aliRelateBrightFunc = None
        self.aliSetColorTempFunc = None
        self.aliRelateColorTempFunc = None
        self.aliQueryFunc = None

        self.duerPowerSrareFunc = None
        self.duerSetColorFunc = None
        self.duerSetModeFunc = None
        self.duerSetcModeFunc = None
        self.duerSetBrightFunc = None
        self.duerRelateBrightFunc = None
        # self.aliSetColorTempFunc = None
        # self.aliRelateColorTempFunc = None
        self.duerQueryFunc = None
        
        self.miPowerSrareFunc = None
        self.miSetColorFunc = None
        self.miSetModeFunc = None
        self.miSetcModeFunc = None
        self.miSetBrightFunc = None
        #self.mtRelateBrightFunc = None
        self.miSetColorTempFunc = None
        #self.mtRelateColorTempFunc = None
        self.miQueryFunc = None

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

    def aliType(self, _type):
        if _type == 'BLINKER_ALIGENIE_LIGHT':
            bProto.aliType = '&aliType=light'
        elif _type == 'BLINKER_ALIGENIE_OUTLET':
            bProto.aliType = '&aliType=outlet'
        elif _type == 'BLINKER_ALIGENIE_MULTI_OUTLET':
            bProto.aliType = '&aliType=multi_outlet'
        elif _type == 'BLINKER_ALIGENIE_SENSOR':
            bProto.aliType = '&aliType=sensor'

    def duerType(self, _type):
        if _type == 'BLINKER_DUEROS_LIGHT':
            bProto.duerType = '&duerType=LIGHT'
        elif _type == 'BLINKER_DUEROS_OUTLET':
            bProto.duerType = '&duerType=SOCKET'
        elif _type == 'BLINKER_DUEROS_MULTI_OUTLET':
            bProto.duerType = '&duerType=MULTI_SOCKET'        
        elif _type == 'BLINKER_DUEROS_SENSOR':
            bProto.duerType = '&duerType=AIR_MONITOR'
            

    def miType(self, _type):
        if _type == 'BLINKER_MIOT_LIGHT':
            bProto.miType = '&miType=light'
        elif _type == 'BLINKER_MIOT_OUTLET':
            bProto.miType = '&miType=outlet'
        elif _type == 'BLINKER_MIOT_MULTI_OUTLET':
            bProto.miType = '&miType=multi_outlet'        
        elif _type == 'BLINKER_MIOT_SENSOR':
            bProto.miType = '&miType=sensor'
    # def debugLevel(level = BLINKER_DEBUG):
    #     bProto.debug = level

    def begin(self, auth = None):
        if bProto.conType == "BLINKER_BLE":
            # return
            # bProto.proto1.bleProto.debug = bProto.debug
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
                bProto.conn1.start(auth, bProto.aliType, bProto.duerType, bProto.miType)
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
            if bProto.conn1.bmqtt.isAliRead is True:
                bProto.msgBuf = bProto.conn1.bmqtt.msgBuf
                bProto.conn1.bmqtt.isAliRead = False
                BlinkerPY.aliParse(self)
            if bProto.conn1.bmqtt.isDuerRead is True:
                bProto.msgBuf = bProto.conn1.bmqtt.msgBuf
                bProto.conn1.bmqtt.isDuerRead = False
                BlinkerPY.duerParse(self)
            if bProto.conn1.bmqtt.isMiRead is True:
                bProto.msgBuf = bProto.conn1.bmqtt.msgBuf
                bProto.conn1.bmqtt.isMiRead = False
                BlinkerPY.miParse(self)
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
            if bProto.conn1.bmqtt.isAliRead is True:
                bProto.msgBuf = bProto.conn1.bmqtt.msgBuf
                bProto.conn1.bmqtt.isAliRead = False
                BlinkerPY.aliParse(self)
            if bProto.conn1.bmqtt.isDuerRead is True:
                bProto.msgBuf = bProto.conn1.bmqtt.msgBuf
                bProto.conn1.bmqtt.isDuerRead = False
                BlinkerPY.duerParse(self)
            if bProto.conn1.bmqtt.isMiRead is True:
                bProto.msgBuf = bProto.conn1.bmqtt.msgBuf
                bProto.conn1.bmqtt.isMiRead = False
                BlinkerPY.miParse(self)

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

    

    def aliParse(self):
        data = bProto.msgBuf
        if not data:
            return
        try:
            data = json.loads(data)
            BLINKER_LOG(data)
            # if data.has_key('set'):
            if 'get' in data.keys():
                _num = 0
                if 'num' in data.keys():
                    _num = int(data['num'])
                data = data['get']
                if data == 'state':
                    if bProto.aliType == '&aliType=multi_outlet':
                        bProto.aliQueryFunc(BLINKER_CMD_QUERY_ALL_NUMBER, _num)
                    else :
                        bProto.aliQueryFunc(BLINKER_CMD_QUERY_ALL_NUMBER)
                elif data == 'pState':
                    if bProto.aliType == '&aliType=multi_outlet':
                        bProto.aliQueryFunc(BLINKER_CMD_QUERY_POWERSTATE_NUMBER, _num)
                    else :
                        bProto.aliQueryFunc(BLINKER_CMD_QUERY_POWERSTATE_NUMBER)
                elif data == 'col':
                    if bProto.aliQueryFunc:
                        bProto.aliQueryFunc(BLINKER_CMD_QUERY_COLOR_NUMBER)
                elif data == 'clr':
                    if bProto.aliQueryFunc:
                        bProto.aliQueryFunc(BLINKER_CMD_QUERY_COLOR_NUMBER)
                elif data == 'colTemp':
                    if bProto.aliQueryFunc:
                        bProto.aliQueryFunc(BLINKER_CMD_QUERY_COLORTEMP_NUMBER)
                elif data == 'bright':
                    if bProto.aliQueryFunc:
                        bProto.aliQueryFunc(BLINKER_CMD_QUERY_BRIGHTNESS_NUMBER)
                elif data == 'temp':
                    if bProto.aliQueryFunc:
                        bProto.aliQueryFunc(BLINKER_CMD_QUERY_TEMP_NUMBER)
                elif data == 'humi':
                    if bProto.aliQueryFunc:
                        bProto.aliQueryFunc(BLINKER_CMD_QUERY_HUMI_NUMBER)
                elif data == 'pm25':
                    if bProto.aliQueryFunc:
                        bProto.aliQueryFunc(BLINKER_CMD_QUERY_PM25_NUMBER)
                elif data == 'mode':
                    if bProto.aliQueryFunc:
                        bProto.aliQueryFunc(BLINKER_CMD_QUERY_MODE_NUMBER)
            
            # elif data.has_key('get'):
            elif 'set' in data.keys():
                data = data['set']
                _num = 0
                if 'num' in data.keys():
                    _num = int(data['num'])
                for key, value in data.items():
                    if key == 'pState':
                        if bProto.aliPowerSrareFunc:
                            # if data.has_key('num'):                            
                            if bProto.aliType == '&aliType=multi_outlet':
                                bProto.aliPowerSrareFunc(value, _num)
                            else :
                                bProto.aliPowerSrareFunc(value)
                    elif key == 'col':
                        if bProto.aliSetColorFunc:
                            bProto.aliSetColorFunc(value)
                    elif key == 'clr':
                        if bProto.aliSetColorFunc:
                            bProto.aliSetColorFunc(value)
                    elif key == 'bright':
                        if bProto.aliSetBrightFunc:
                            bProto.aliSetBrightFunc(value)
                    elif key == 'upBright':
                        if bProto.aliRelateBrightFunc:
                            bProto.aliRelateBrightFunc(value)
                    elif key == 'downBright':
                        if bProto.aliRelateBrightFunc:
                            bProto.aliRelateBrightFunc(value)
                    elif key == 'colTemp':
                        if bProto.aliSetColorTempFunc:
                            bProto.aliSetColorTempFunc(value)
                    elif key == 'upColTemp':
                        if bProto.aliRelateColorTempFunc:
                            bProto.aliRelateColorTempFunc(value)
                    elif key == 'downColTemp':
                        if bProto.aliRelateColorTempFunc:
                            bProto.aliRelateColorTempFunc(value)
                    elif key == 'mode':
                        if bProto.aliSetModeFunc:
                            bProto.aliSetModeFunc(value)
                    elif key == 'cMode':
                        if bProto.aliSetcModeFunc:
                            bProto.aliSetcModeFunc(value)

        except ValueError:
            pass
        except TypeError:
            pass
        finally:
            pass

    def duerParse(self):
        data = bProto.msgBuf
        if not data:
            return
        try:
            data = json.loads(data)
            BLINKER_LOG(data)
            # if data.has_key('set'):
            if 'get' in data.keys():
                _num = 0
                if 'num' in data.keys():
                    _num = int(data['num'])
                data = data['get']
                if data == 'time':
                    if bProto.duerType == '&duerType=MULTI_SOCKET':
                        bProto.duerQueryFunc(BLINKER_CMD_QUERY_TIME_NUMBER, _num)
                    else :
                        bProto.duerQueryFunc(BLINKER_CMD_QUERY_TIME_NUMBER)
                elif data == 'aqi':
                    if bProto.duerQueryFunc:
                        bProto.duerQueryFunc(BLINKER_CMD_QUERY_AQI_NUMBER)
                elif data == 'pm25':
                    if bProto.duerQueryFunc:
                        bProto.duerQueryFunc(BLINKER_CMD_QUERY_PM25_NUMBER)
                elif data == 'pm10':
                    if bProto.duerQueryFunc:
                        bProto.duerQueryFunc(BLINKER_CMD_QUERY_PM10_NUMBER)
                elif data == 'co2':
                    if bProto.duerQueryFunc:
                        bProto.duerQueryFunc(BLINKER_CMD_QUERY_CO2_NUMBER)
                elif data == 'temp':
                    if bProto.duerQueryFunc:
                        bProto.duerQueryFunc(BLINKER_CMD_QUERY_TEMP_NUMBER)
                elif data == 'humi':
                    if bProto.duerQueryFunc:
                        bProto.duerQueryFunc(BLINKER_CMD_QUERY_HUMI_NUMBER)
                elif data == 'pm25':
                    if bProto.duerQueryFunc:
                        bProto.duerQueryFunc(BLINKER_CMD_QUERY_PM25_NUMBER)
                elif data == 'mode':
                    if bProto.duerQueryFunc:
                        bProto.duerQueryFunc(BLINKER_CMD_QUERY_TIME_NUMBER)
            
            # elif data.has_key('get'):
            elif 'set' in data.keys():
                data = data['set']
                _num = 0
                if 'num' in data.keys():
                    _num = int(data['num'])
                for key, value in data.items():
                    if key == 'pState':
                        if bProto.duerPowerSrareFunc:
                            # if data.has_key('num'):                            
                            if bProto.duerType == '&duerType=MULTI_SOCKET':
                                bProto.duerPowerSrareFunc(value, _num)
                            else :
                                bProto.duerPowerSrareFunc(value)
                    elif key == 'col':
                        if bProto.duerSetColorFunc:
                            bProto.duerSetColorFunc(value)
                    elif key == 'clr':
                        if bProto.duerSetColorFunc:
                            bProto.duerSetColorFunc(value)
                    elif key == 'bright':
                        if bProto.duerSetBrightFunc:
                            bProto.duerSetBrightFunc(value)
                    elif key == 'upBright':
                        if bProto.duerRelateBrightFunc:
                            bProto.duerRelateBrightFunc(value)
                    elif key == 'downBright':
                        if bProto.duerRelateBrightFunc:
                            bProto.duerRelateBrightFunc(value)
                    # elif key == 'colTemp':
                    #     if bProto.duerSetColorTempFunc:
                    #         bProto.duerSetColorTempFunc(value)
                    # elif key == 'upColTemp':
                    #     if bProto.aliRelateColorTempFunc:
                    #         bProto.aliRelateColorTempFunc(value)
                    # elif key == 'downColTemp':
                    #     if bProto.duerRelateColorTempFunc:
                    #         bProto.duerRelateColorTempFunc(value)
                    elif key == 'mode':
                        if bProto.duerSetModeFunc:
                            bProto.duerSetModeFunc(value)
                    elif key == 'cMode':
                        if bProto.duerSetcModeFunc:
                            bProto.duerSetcModeFunc(value)

        except ValueError:
            pass
        except TypeError:
            pass
        finally:
            pass

    
    def miParse(self):
        data = bProto.msgBuf
        if not data:
            return
        try:
            data = json.loads(data)
            BLINKER_LOG(data)
            # if data.has_key('set'):
            if 'get' in data.keys():
                _num = 0
                if 'num' in data.keys():
                    _num = int(data['num'])
                data = data['get']
                if data == 'state':
                    if bProto.miType == '&miType=multi_outlet':
                        bProto.miQueryFunc(BLINKER_CMD_QUERY_ALL_NUMBER, _num)
                    else :
                        bProto.miQueryFunc(BLINKER_CMD_QUERY_ALL_NUMBER)
                elif data == 'pState':
                    if bProto.aliType == '&miType=multi_outlet':
                        bProto.miQueryFunc(BLINKER_CMD_QUERY_POWERSTATE_NUMBER, _num)
                    else :
                        bProto.miQueryFunc(BLINKER_CMD_QUERY_POWERSTATE_NUMBER)
                elif data == 'col':
                    if bProto.miQueryFunc:
                        bProto.miQueryFunc(BLINKER_CMD_QUERY_COLOR_NUMBER)
                elif data == 'clr':
                    if bProto.miQueryFunc:
                        bProto.miQueryFunc(BLINKER_CMD_QUERY_COLOR_NUMBER)
                elif data == 'colTemp':
                    if bProto.miQueryFunc:
                        bProto.miQueryFunc(BLINKER_CMD_QUERY_COLORTEMP_NUMBER)
                elif data == 'aqi':
                    if bProto.miQueryFunc:
                        bProto.miQueryFunc(BLINKER_CMD_QUERY_AQI_NUMBER)
                elif data == 'co2':
                    if bProto.miQueryFunc:
                        bProto.miQueryFunc(BLINKER_CMD_QUERY_CO2_NUMBER)
                elif data == 'bright':
                    if bProto.miQueryFunc:
                        bProto.miQueryFunc(BLINKER_CMD_QUERY_BRIGHTNESS_NUMBER)
                elif data == 'temp':
                    if bProto.miQueryFunc:
                        bProto.miQueryFunc(BLINKER_CMD_QUERY_TEMP_NUMBER)
                elif data == 'humi':
                    if bProto.miQueryFunc:
                        bProto.miQueryFunc(BLINKER_CMD_QUERY_HUMI_NUMBER)
                elif data == 'pm25':
                    if bProto.miQueryFunc:
                        bProto.miQueryFunc(BLINKER_CMD_QUERY_PM25_NUMBER)
                elif data == 'mode':
                    if bProto.miQueryFunc:
                        bProto.miQueryFunc(BLINKER_CMD_QUERY_MODE_NUMBER)
            
            # elif data.has_key('get'):
            elif 'set' in data.keys():
                data = data['set']
                _num = 0
                if 'num' in data.keys():
                    _num = int(data['num'])
                for key, value in data.items():
                    if key == 'pState':
                        if bProto.miPowerSrareFunc:
                            # if data.has_key('num'):                            
                            if bProto.miType == '&miType=multi_outlet':
                                bProto.miPowerSrareFunc(value, _num)
                            else :
                                bProto.miPowerSrareFunc(value)
                    elif key == 'col':
                        if bProto.miSetColorFunc:
                            bProto.miSetColorFunc(value)
                    elif key == 'clr':
                        if bProto.miSetColorFunc:
                            bProto.miSetColorFunc(value)
                    elif key == 'bright':
                        if bProto.miSetBrightFunc:
                            bProto.miSetBrightFunc(value)
                    elif key == 'upBright':
                        if bProto.miRelateBrightFunc:
                            bProto.miRelateBrightFunc(value)
                    elif key == 'downBright':
                        if bProto.miRelateBrightFunc:
                            bProto.miRelateBrightFunc(value)
                    elif key == 'colTemp':
                        if bProto.miSetColorTempFunc:
                            bProto.miSetColorTempFunc(value)
                    elif key == 'upColTemp':
                        if bProto.miRelateColorTempFunc:
                            bProto.miRelateColorTempFunc(value)
                    elif key == 'downColTemp':
                        if bProto.miRelateColorTempFunc:
                            bProto.miRelateColorTempFunc(value)
                    elif key == 'mode':
                        if bProto.miSetModeFunc:
                            bProto.miSetModeFunc(value)
                    elif key == 'cMode':
                        if bProto.miSetcModeFunc:
                            bProto.miSetcModeFunc(value)

        except ValueError:
            pass
        except TypeError:
            pass
        finally:
            pass

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
        while BlinkerPY.connected(self) is False:
            BlinkerPY.connect(self)
        BlinkerPY.print(self, BLINKER_CMD_AHRS, BLINKER_CMD_ON)
        BlinkerPY.delay(self, 100)
        run()
        start_time = millis()
        state = bProto.Ahrs[AHRS_state]
        while state is False:
            if (millis() - start_time) > BLINKER_CONNECT_TIMEOUT_MS:
                BLINKER_LOG("AHRS attach failed...Try again")
                start_time = millis()
                BlinkerPY.print(self, BLINKER_CMD_AHRS, BLINKER_CMD_ON)
                BlinkerPY.delay(self, 100)
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
        BlinkerPY.delay(self, 100)
        BlinkerPY.run(self)
        if axis >= LONG and axis <= LAT:
            return bProto.GPS[axis]
        else:
            return "0.000000"

    def vibrate(self, time = 200):
        if time > 1000:
            time = 1000
        BlinkerPY.print(self, BLINKER_CMD_VIBRATE, time)

    def time(self):
        return int(_time.time())

    def second(self):
        localtime = _time.localtime(int(_time.time()))
        return localtime.tm_sec

    def minute(self):
        localtime = _time.localtime(int(_time.time()))
        return localtime.tm_min

    def hour(self):
        localtime = _time.localtime(int(_time.time()))
        return localtime.tm_hour

    def mday(self):
        localtime = _time.localtime(int(_time.time()))
        return localtime.tm_mday

    def wday(self):
        localtime = _time.localtime(int(_time.time()))
        return (localtime.tm_wday + 1) % 7

    def month(self):
        localtime = _time.localtime(int(_time.time()))
        return localtime.tm_mon

    def year(self):
        localtime = _time.localtime(int(_time.time()))
        return localtime.tm_year

    def yday(self):
        localtime = _time.localtime(int(_time.time()))
        return localtime.tm_yday

    def dtime(self):
        localtime = _time.localtime(int(_time.time()))
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

    def dataStorageCallback(self):
        timer = threading.Timer(bProto.dataTime, dataStorage)
        timer.start()

        bProto.dataStorageFunc()
        bProto.dataTimesLimit = bProto.dataTimesLimit + 1

        if bProto.dataTimesLimit >= bProto.dataTimes:
            if BlinkerPY.dataUpdate(self):
                bProto.dataTimesLimit = 0

    def attachDataStorage(self, func, limit = BLINKER_DATA_FREQ_TIME, times = 4):
        bProto.dataStorageFunc = func
        if limit >= 60.0:
            bProto.dataTime = limit
        else:
            bProto.dataTime = 60.0
        bProto.dataTimes = times
        timer = threading.Timer(limit, dataStorage)
        timer.start()

    def dataStorage(self, name, data):
        now_time = BlinkerPY.time(self) - BlinkerPY.second(self)
        now_time = now_time - now_time % 10
        BLINKER_LOG_ALL('now_time: ', now_time)

        if name in bProto.Datas:
            bProto.Datas[name].saveData(data, now_time, bProto.dataTime)
        else:
            _Data = BlinkerData(name)
            _Data.saveData(data, now_time, bProto.dataTime)
            bProto.dataCount = bProto.dataCount + 1

    def dataUpdate(self):
        if bProto.dataCount == 0:
            return
        if bProto.conType == "BLINKER_MQTT":
            datas = {}
            for name in bProto.Datas:
                # datas.append(bProto.Datas[name].getData())
                datas[name] = bProto.Datas[name].getData()
            if bProto.conn1.dataUpdate(datas):
                for name in bProto.Datas:
                    bProto.Datas[name].flush()
                return True
            return False

        else:
            BLINKER_ERR_LOG('This code is intended to run on the MQTT!')

    

    ## ali
    def attachAliGenieSetPowerState(self, _func):
        bProto.aliPowerSrareFunc = _func
    
    def attachAliGenieSetColor(self, _func):
        bProto.aliSetColorFunc = _func

    def attachAliGenieSetMode(self, _func):
        bProto.aliSetModeFunc = _func

    def attachAliGenieSetcMode(self, _func):
        bProto.aliSetcModeFunc = _func

    def attachAliGenieSetBrightness(self, _func):
        bProto.aliSetBrightFunc = _func

    def attachAliGenieRelativeBrightness(self, _func):
        bProto.aliRelateBrightFunc = _func

    def attachAliGenieSetColorTemperature(self, _func):
        bProto.aliSetColorTempFunc = _func

    def attachAliGenieRelativeColorTemperature(self, _func):
        bProto.aliRelateColorTempFunc = _func

    def attachAliGenieQuery(self, _func):
        bProto.aliQueryFunc = _func

    def aliPrint(self, data):
        bProto.conn1.aliPrint(data)

    ## duer
    def attachDuerOSSetPowerState(self, _func):
        bProto.duerPowerSrareFunc = _func
    
    def attachDuerOSSetColor(self, _func):
        bProto.duerSetColorFunc = _func

    def attachDuerOSSetMode(self, _func):
        bProto.duerSetModeFunc = _func

    def attachDuerOSSetcMode(self, _func):
        bProto.duerSetcModeFunc = _func

    def attachDuerOSSetBrightness(self, _func):
        bProto.duerSetBrightFunc = _func

    def attachDuerOSRelativeBrightness(self, _func):
        bProto.duerRelateBrightFunc = _func

    # def attachAliGenieSetColorTemperature(self, _func):
    #     bProto.aliSetColorTempFunc = _func

    # def attachAliGenieRelativeColorTemperature(self, _func):
    #     bProto.aliRelateColorTempFunc = _func

    def attachDuerOSQuery(self, _func):
        bProto.duerQueryFunc = _func

    def duerPrint(self, data):
        bProto.conn1.duerPrint(data)
    ## mi
    def attachMiSetPowerState(self, _func):
        bProto.miPowerSrareFunc = _func
    
    def attachMiSetColor(self, _func):
        bProto.miSetColorFunc = _func

    def attachMiSetMode(self, _func):
        bProto.miSetModeFunc = _func

    def attachMiSetcMode(self, _func):
        bProto.miSetcModeFunc = _func

    def attachMiSetBrightness(self, _func):
        bProto.miSetBrightFunc = _func

    def attachMiRelativeBrightness(self, _func):
        bProto.miRelateBrightFunc = _func

    def attachMiSetColorTemperature(self, _func):
        bProto.miSetColorTempFunc = _func

    def attachMiRelativeColorTemperature(self, _func):
        bProto.miRelateColorTempFunc = _func

    def attachMiQuery(self, _func):
        bProto.miQueryFunc = _func

    def miPrint(self, data):
        bProto.conn1.miPrint(data)


Blinker = BlinkerPY()

def thread_run():
    if bProto.conType == "BLINKER_BLE":
        bProto.conn1.run()
    while True:
        Blinker.checkData()

def dataStorage():
    Blinker.dataStorageCallback()

class BlinkerData(object):
    """ """

    def __init__(self, name):
        self.name = name
        self.lastTime = 0
        self.dataCount = 0
        self.data = []
        
        bProto.Datas[name] = self

    # def name(self, name)
    #     self.name = name
    #     bProto.Datas[name] = self

    def saveData(self, _data, _now, _limit):
        if self.dataCount :
            if (_now - self.lastTime) < _limit :
                return
        self.lastTime = _now
        dataList = [_now, _data]
        self.data.append(dataList)
        self.dataCount = self.dataCount + 1
        BLINKER_LOG_ALL(self.data)

    def getData(self):
        return self.data

    def flush(self):
        self.data.clear()


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

class BLINKERA_LIGENIE():
    def __init__(self):
        self.payload = {}

    def attachPowerState(self, _func):
        Blinker.attachAliGenieSetPowerState(_func)

    def attachColor(self, _func):
        Blinker.attachAliGenieSetColor(_func)

    def attachMode(self, _func):
        Blinker.attachAliGenieSetMode(_func)

    def attachCancelMode(self, _func):
        Blinker.attachAliGenieSetcMode(_func)
    
    def attachBrightness(self, _func):
        Blinker.attachAliGenieSetBrightness(_func)

    def attachRelativeBrightness(self, _func):
        Blinker.attachAliGenieRelativeBrightness(_func)

    def attachColorTemperature(self, _func):
        Blinker.attachAliGenieSetColorTemperature(_func)

    def attachRelativeColorTemperature(self, _func):
        Blinker.attachAliGenieRelativeColorTemperature(_func)

    def attachQuery(self, _func):
        Blinker.attachAliGenieQuery(_func)

    def powerState(self, state, num = None):
        self.payload['pState'] = state
        if num :
            self.payload['num'] = num

    def color(self, clr):
        self.payload['clr'] = clr

    def mode(self, md):
        self.payload['mode'] = md

    def colorTemp(self, clrTemp):
        self.payload['colTemp'] = clrTemp

    def brightness(self, bright):
        self.payload['bright'] = bright

    def temp(self, tem):
        self.payload['temp'] = tem

    def humi(self, hum):
        self.payload['humi'] = hum

    def pm25(self, pm):
        self.payload['pm25'] = pm

    def print(self):
        BLINKER_LOG_ALL(self.payload)
        Blinker.aliPrint(self.payload)
        self.payload.clear()

BlinkerAliGenie = BLINKERA_LIGENIE()

class BLINKERA_DUEROS():
    def __init__(self):
        self.payload = {}

    def attachPowerState(self, _func):
        Blinker.attachDuerOSSetPowerState(_func)

    def attachColor(self, _func):
        Blinker.attachDuerOSSetColor(_func)

    def attachMode(self, _func):
        Blinker.attachDuerOSSetMode(_func)

    def attachCancelMode(self, _func):
        Blinker.attachDuerOSSetcMode(_func)
    
    def attachBrightness(self, _func):
        Blinker.attachDuerOSSetBrightness(_func)

    def attachRelativeBrightness(self, _func):
        Blinker.attachDuerOSRelativeBrightness(_func)

    # def attachColorTemperature(self, _func):
    #     Blinker.attachAliGenieSetColorTemperature(_func)

    # def attachRelativeColorTemperature(self, _func):
    #     Blinker.attachAliGenieRelativeColorTemperature(_func)

    def attachQuery(self, _func):
        Blinker.attachDuerOSQuery(_func)

    def powerState(self, state, num = None):
        self.payload['pState'] = state
        if num :
            self.payload['num'] = num

    def color(self, clr):
        self.payload['clr'] = clr

    def mode(self, md):
        self.payload['mode'] = ['', md]

    # def colorTemp(self, clrTemp):
    #     self.payload['colTemp'] = clrTemp

    def brightness(self, bright):
        self.payload['bright'] = ['', bright]

    def temp(self, tem):
        self.payload['temp'] = tem

    def humi(self, hum):
        self.payload['humi'] = hum

    def pm25(self, pm):
        self.payload['pm25'] = pm

    def pm10(self, pm):
        self.payload['pm10'] = pm

    def co2(self, pm):
        self.payload['co2'] = pm

    def aqi(self, pm):
        self.payload['aqi'] = pm

    def time(self, pm):
        self.payload['time'] = pm

    def print(self):
        BLINKER_LOG_ALL(self.payload)
        Blinker.duerPrint(self.payload)
        self.payload.clear()

BlinkerDuerOS = BLINKERA_DUEROS()

class BLINKERA_MIOT():
    def __init__(self):
        self.payload = {}

    def attachPowerState(self, _func):
        Blinker.attachMiSetPowerState(_func)

    def attachColor(self, _func):
        Blinker.attachMiSetColor(_func)

    def attachMode(self, _func):
        Blinker.attachMiSetMode(_func)

    def attachCancelMode(self, _func):
        Blinker.attachMiSetcMode(_func)
    
    def attachBrightness(self, _func):
        Blinker.attachMiSetBrightness(_func)

    def attachRelativeBrightness(self, _func):
        Blinker.attachMiRelativeBrightness(_func)

    def attachColorTemperature(self, _func):
        Blinker.attachMiSetColorTemperature(_func)

    def attachRelativeColorTemperature(self, _func):
        Blinker.attachMiRelativeColorTemperature(_func)

    def attachQuery(self, _func):
        Blinker.attachMiQuery(_func)

    def powerState(self, state, num = None):
        self.payload['pState'] = state
        if num :
            self.payload['num'] = num

    def color(self, clr):
        self.payload['clr'] = clr

    def mode(self, md):
        self.payload['mode'] = md

    def colorTemp(self, clrTemp):
        self.payload['colTemp'] = clrTemp

    def brightness(self, bright):
        self.payload['bright'] = bright

    def co2(self, pm):
        self.payload['co2'] = pm

    def aqi(self, pm):
        self.payload['aqi'] = pm
        
    def temp(self, tem):
        self.payload['temp'] = tem

    def humi(self, hum):
        self.payload['humi'] = hum

    def pm25(self, pm):
        self.payload['pm25'] = pm

    def print(self):
        BLINKER_LOG_ALL(self.payload)
        Blinker.miPrint(self.payload)
        self.payload.clear()

BlinkerMiot = BLINKERA_MIOT()

