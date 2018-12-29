# -*- coding: utf-8 -*-

import threading
import time as _time
from .BlinkerConfig import *
from .BlinkerDebug import *
from BlinkerUtility import *


# from BlinkerAdapters.BlinkerBLE import *
# from BlinkerAdapters.BlinkerLinuxWS import *
# from BlinkerAdapters.BlinkerMQTT import *
# from threading import Thread
# from zeroconf import ServiceInfo, Zeroconf
# from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

class Protocol(object):

    def __init__(self):
        self.conType = BLINKER_WIFI
        self.proto1 = None
        self.proto2 = None
        self.conn1 = None
        self.conn2 = None
        # self.debug = BLINKER_DEBUG

        self.msgFrom = None
        self.msgBuf = None
        self.sendBuf = {}
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


protocol = Protocol()


def mode(setType=BLINKER_WIFI):
    protocol.conType = setType
    if protocol.conType == BLINKER_BLE:
        import BlinkerAdapters.BlinkerBLE as bBLE

        protocol.proto1 = bBLE
        protocol.conn1 = protocol.proto1.BlinkerBLEService()
    elif protocol.conType == BLINKER_WIFI:
        import BlinkerAdapters as bWS

        protocol.proto1 = bWS
        protocol.conn1 = protocol.proto1.WebSocketServer()
    elif protocol.conType == BLINKER_MQTT :#or protocol.conType == BLINKER_WIFI:
        protocol.conType = BLINKER_MQTT
        import BlinkerAdapters as bWS
        import BlinkerAdapters as bMQTT

        protocol.proto1 = bMQTT
        protocol.proto2 = bWS
        protocol.conn1 = protocol.proto1.MQTTClient()
        protocol.conn2 = protocol.proto2.WebSocketServer(BLINKER_DIY_MQTT)


# def debugLevel(level=BLINKER_DEBUG):
#     protocol.debug = level


def begin(auth=None):
    if protocol.conType == BLINKER_BLE:
        # return
        # protocol.proto1.bleProto.debug = protocol.debug
        # bProto.conn1.run()
        protocol.conn1.start()
    elif protocol.conType == BLINKER_WIFI:
        # protocol.proto1.wsProto.debug = protocol.debug
        protocol.conn1.start()
    elif protocol.conType == BLINKER_MQTT:
        # protocol.conn1.mProto.debug = protocol.debug
        # protocol.proto2.wsProto.debug = protocol.debug
        protocol.msgFrom = BLINKER_MQTT
        protocol.conn1.start(auth)
        # BLINKER_LOG("deviceName: ", protocol.conn1.bmqtt.deviceName[0: 12])
        protocol.conn2.start(protocol.conn1.bmqtt.deviceName)#[0: 12])
        protocol.conn1.run()


def connected():
    if protocol.state is CONNECTED:
        return True
    else:
        return False


def connect(timeout=BLINKER_STREAM_TIMEOUT):
    protocol.state = CONNECTING
    start_time = millis()
    while (millis() - start_time) < timeout:
        run()
        if protocol.state is CONNECTED:
            return True
    return False


def disconnect():
    protocol.state = DISCONNECTED


def stateData():
    for tKey in protocol.Toggles:
        tValue = ''
        if protocol.Toggles[tKey]:
            tValue = 'on'
        else:
            tValue = 'off'
        print(tKey, tValue)
    for sKey in protocol.Sliders:
        print(sKey, protocol.Sliders[sKey])
    for rgbKey in protocol.RGB:
        print(rgbKey, protocol.RGB[rgbKey])


def heartbeat():
    if protocol.conType is BLINKER_MQTT:
        # beginFormat()
        print(BLINKER_CMD_STATE, BLINKER_CMD_ONLINE)
        stateData()
        # if endFormat() is False:
        #     print(BLINKER_CMD_STATE, BLINKER_CMD_ONLINE)
    else:
        # beginFormat()
        print(BLINKER_CMD_STATE, BLINKER_CMD_CONNECTED)
        stateData()
        # if endFormat() is False:
        #     print(BLINKER_CMD_STATE, BLINKER_CMD_CONNECTED)


def thread_run():
    if protocol.conType == BLINKER_BLE:
        protocol.conn1.run()
    # else :
    #     protocol.conn2.run()
    while True:
        checkData()


def run():
    if protocol.isThreadStart is False:
        protocol.thread = threading.Thread(target=thread_run)
        protocol.thread.daemon = True
        protocol.thread.start()
        protocol.isThreadStart = True
    checkData()
    checkAutoFormat()


# Data management

def parse():
    data = protocol.msgBuf
    if not data:
        return
    try:
        data = json.loads(data)
        BLINKER_LOG(data)
        # BLINKER_LOG(protocol.Sliders)
        if not isinstance(data, dict):
            raise TypeError()
        for key, value in data.items():
            if key in protocol.Buttons:
                protocol.isRead = False
                protocol.Buttons[key].func(data[key])
            elif key in protocol.Sliders:
                protocol.isRead = False
                protocol.Sliders[key].func(data[key])
            elif key in protocol.Toggles:
                protocol.isRead = False
                protocol.Toggles[key].func(data[key])
            elif key in protocol.RGB:
                protocol.isRead = False
                BLINKER_LOG(protocol.RGB[key])
                protocol.RGB[key].func(data[key][R], data[key][G], data[key][B], data[key][BR])
            elif key in protocol.Joystick:
                protocol.isRead = False
                protocol.Joystick[key].func(data[key][J_Xaxis], data[key][J_Yaxis])
            elif key == BLINKER_CMD_AHRS:
                # bProto.isAvail = False
                protocol.isRead = False
                protocol.Ahrs[Yaw] = data[key][Yaw]
                protocol.Ahrs[Pitch] = data[key][Pitch]
                protocol.Ahrs[Roll] = data[key][Roll]
                protocol.Ahrs[AHRS_state] = True
                # BLINKER_LOG(bProto.Ahrs)
            elif key == BLINKER_CMD_GPS:
                protocol.isRead = False
                protocol.GPS[LONG] = str(data[key][LONG])
                protocol.GPS[LAT] = str(data[key][LAT])

            elif key == BLINKER_CMD_GET and data[key] == BLINKER_CMD_VERSION:
                protocol.isRead = False
                print(BLINKER_CMD_VERSION, BLINKER_VERSION)

            elif key == BLINKER_CMD_GET and data[key] == BLINKER_CMD_STATE:
                protocol.isRead = False
                heartbeat()

    except ValueError:
        pass
    except TypeError:
        pass
    finally:
        if protocol.isRead:
            protocol.isAvail = True


def _parse(data):
    if not data:
        return
    try:
        data = json.loads(data)
        if not isinstance(data, dict):
            raise TypeError()
        for key in data.keys():
            # BLINKER_LOG(key)
            if key in protocol.Buttons:
                # bProto.isAvail = False
                protocol.isRead = False
                if data[key] == BLINKER_CMD_BUTTON_TAP:
                    protocol.Buttons[key] = BLINKER_CMD_BUTTON_TAP
                elif data[key] == BLINKER_CMD_BUTTON_PRESSED:
                    protocol.Buttons[key] = BLINKER_CMD_BUTTON_PRESSED
                else:
                    protocol.Buttons[key] = BLINKER_CMD_BUTTON_RELEASED
                # if data[key]
                # BLINKER_LOG(bProto.Buttons)

            elif key in protocol.Sliders:
                # bProto.isAvail = False
                protocol.isRead = False
                protocol.Sliders[key] = data[key]
                # BLINKER_LOG(bProto.Buttons)

            elif key in protocol.Toggles:
                # bProto.isAvail = False
                protocol.isRead = False
                if data[key] == BLINKER_CMD_ON:
                    protocol.Toggles[key] = True
                else:
                    protocol.Toggles[key] = False
                # BLINKER_LOG(bProto.Toggles)

            elif key in protocol.RGB:
                protocol.isRead = False
                rgb = [0, 0, 0]
                rgb[R] = data[key][R]
                rgb[G] = data[key][G]
                rgb[B] = data[key][B]
                protocol.RGB[key] = rgb
    except ValueError:
        pass
    except TypeError:
        pass
    finally:
        if protocol.isRead:
            protocol.isAvail = True


def checkData():
    if protocol.conType == BLINKER_BLE:
        # return
        protocol.state = protocol.proto1.bleProto.state
        if protocol.proto1.bleProto.isRead is True:
            protocol.msgBuf = protocol.proto1.bleProto.msgBuf
            protocol.isRead = True
            protocol.proto1.bleProto.isRead = False
            parse()
    # elif protocol.conType == BLINKER_WIFI:
    #     protocol.state = protocol.proto1.wsProto.state
    #     if protocol.proto1.wsProto.isRead is True:
    #         protocol.msgBuf = str(protocol.proto1.wsProto.msgBuf)
    #         protocol.isRead = True
    #         protocol.proto1.wsProto.isRead = False
    #         parse()
    elif protocol.conType == BLINKER_MQTT:
        protocol.state = protocol.conn1.bmqtt.state
        if protocol.proto2.wsProto.state is CONNECTED:
            protocol.state = protocol.proto2.wsProto.state
        # if protocol.conn1.bmqtt.isRead is True:
        #     protocol.msgBuf = protocol.conn1.bmqtt.msgBuf
        #     protocol.msgFrom = BLINKER_MQTT
        #     protocol.isRead = True
        #     protocol.conn1.bmqtt.isRead = False
        #     parse()
        if protocol.proto2.wsProto.isRead is True:
            protocol.msgBuf = str(protocol.proto2.wsProto.msgBuf)
            protocol.msgFrom = BLINKER_WIFI
            protocol.isRead = True
            protocol.proto2.wsProto.isRead = False
            parse()


def available():
    return protocol.isAvail


def readString():
    protocol.isRead = False
    protocol.isAvail = False
    return protocol.msgBuf


def times():
    return now()


def checkLength(data):
    if len(data) > BLINKER_MAX_SEND_SIZE:
        BLINKER_ERR_LOG('SEND DATA BYTES MAX THAN LIMIT!')
        return False
    else:
        return True


def _print(data):
    if checkLength(data) is False:
        return

    if protocol.conType == BLINKER_BLE:
        protocol.conn1.response(data)
    elif protocol.conType == BLINKER_WIFI:
        protocol.conn1.broadcast(data)
    elif protocol.conType == BLINKER_MQTT and protocol.msgFrom == BLINKER_MQTT:
        if BLINKER_CMD_NOTICE in data:
            _state = True
        elif BLINKER_CMD_STATE in data:
            _state = True
        else:
            _state = False
        protocol.conn1.pub(data, _state)
    elif protocol.conType == BLINKER_MQTT and protocol.msgFrom == BLINKER_WIFI:
        protocol.conn2.broadcast(data)

    _parse(data)


def print(key, value=None):
    if value is None:
        if protocol.isFormat:
            return
        data = str(key)
        _print(data)
    else:
        key = str(key)
        # if uint is not None:
            # value = str(value) + str(uint)
        # data = json_encode(key, value)
        # data = {}
        if protocol.isFormat == False:
            protocol.isFormat = True

        if (millis() - protocol.autoFormatFreshTime) >= 100 :
            protocol.autoFormatFreshTime = millis()

        protocol.sendBuf[key] = value

    #     else:
    #         data[key] = value

    # if protocol.isFormat is False:
    #     _print(data)

# def checkFormat():

def checkAutoFormat():
    if protocol.isFormat :
        if (millis() - protocol.autoFormatFreshTime) >= 100 :
            _print(protocol.sendBuf)
            protocol.isFormat = False


# def beginFormat():
#     protocol.isFormat = True
#     protocol.sendBuf.clear()


# def endFormat():
#     protocol.isFormat = False
#     _print(protocol.sendBuf)
#     return checkLength(protocol.sendBuf)


def notify(msg):
    print(BLINKER_CMD_NOTICE, msg)


def delay(ms):
    start = millis()
    time_run = 0
    while time_run < ms:
        run()
        time_run = millis() - start


def vibrate(t=200):
    if t > 1000:
        t = 1000
    print(BLINKER_CMD_VIBRATE, t)


def time():
    return _time.time()


def second():
    localtime = _time.localtime(_time.time())
    return localtime.tm_sec


def minute():
    localtime = _time.localtime(_time.time())
    return localtime.tm_min


def hour():
    localtime = _time.localtime(_time.time())
    return localtime.tm_hour


def mday():
    localtime = _time.localtime(_time.time())
    return localtime.tm_mday


def wday():
    localtime = _time.localtime(_time.time())
    return (localtime.tm_wday + 1) % 7


def month():
    localtime = _time.localtime(_time.time())
    return localtime.tm_mon


def year():
    localtime = _time.localtime(_time.time())
    return localtime.tm_year


def yday():
    localtime = _time.localtime(_time.time())
    return localtime.tm_yday


def dtime():
    localtime = _time.localtime(_time.time())
    return localtime.tm_hour * 60 * 60 + localtime.tm_min * 60 + localtime.tm_sec


def sms(sms_msg):
    if protocol.conType == BLINKER_MQTT:
        protocol.conn1.sendSMS(sms_msg)
    else:
        BLINKER_ERR_LOG('This code is intended to run on the MQTT!')


def ahrs(axis):
    if Yaw <= axis <= Roll:
        return protocol.Ahrs[axis]
    else:
        return 0


def attachAhrs():
    state = False
    while connected() is False:
        connect()
    print(BLINKER_CMD_AHRS, BLINKER_CMD_ON)
    delay(100)
    run()
    start_time = millis()
    state = protocol.Ahrs[AHRS_state]
    while state is False:
        if (millis() - start_time) > BLINKER_CONNECT_TIMEOUT_MS:
            BLINKER_LOG("AHRS attach failed...Try again")
            start_time = millis()
            print(BLINKER_CMD_AHRS, BLINKER_CMD_ON)
            delay(100)
            run()
        state = protocol.Ahrs[AHRS_state]
    BLINKER_LOG("AHRS attach sucessed...")


def detachAhrs():
    print(BLINKER_CMD_AHRS, BLINKER_CMD_OFF)
    protocol.Ahrs[Yaw] = 0
    protocol.Ahrs[Roll] = 0
    protocol.Ahrs[Pitch] = 0
    protocol.Ahrs[AHRS_state] = False


def gps(axis):
    print(BLINKER_CMD_GET, BLINKER_CMD_GPS)
    delay(100)
    run()
    if LONG <= axis <= LAT:
        return protocol.GPS[axis]
    else:
        return "0.000000"


class BlinkerButton(object):
    """ """

    def __init__(self, name, func=None):
        self.name = name
        self.func = func
        self._icon = None
        self.iconClr = None
        self._content = None
        self._text = None
        self._text1 = None
        self.textClr = None
        self.buttonData = None

        protocol.Buttons[name] = self

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
            self.buttonData = {BLINKER_CMD_SWITCH: state}

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

        # data = json.dumps(self.buttonData)
        data = {self.name: self.buttonData}
        _print(data)


class BlinkerRGB(object):
    """ """

    def __init__(self, name, func=None):
        self.name = name
        self.func = func
        self.rgbbrightness = 0
        self.rgbData = []
        self.registered = False

        protocol.RGB[name] = self

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
        data = {self.name: self.rgbData}
        _print(data)


class BlinkerSlider(object):
    """ """

    def __init__(self, name, func=None):
        self.name = name
        self.func = func
        self.textClr = ""
        self.sliderData = {}

        protocol.Sliders[name] = self

    def attach(self, func):
        self.func = func

    def color(self, _clr):
        self.textClr = _clr

    def print(self, value):
        self.sliderData[BLINKER_CMD_VALUE] = value
        if self.textClr:
            self.sliderData[BLINKER_CMD_COLOR] = self.textClr

        # data = json.dumps(self.sliderData)
        data = {self.name: self.sliderData}
        _print(data)


class BlinkerNumber(object):
    """ """

    def __init__(self, name):
        self.name = name
        self._icon = ""
        self._color = ""
        self._unit = ""
        self.buttonData = {}

        protocol.Numbers[name] = self

    def icon(self, _icon):
        self._icon = _icon

    def color(self, _clr):
        self._color = _clr

    def unit(self, _unit):
        self._unit = _unit

    def print(self, value):
        self.buttonData[BLINKER_CMD_VALUE] = value
        if self._icon:
            self.buttonData[BLINKER_CMD_ICON] = self._icon
        if self._color:
            self.buttonData[BLINKER_CMD_COLOR] = self._color
        if self._unit:
            self.buttonData[BLINKER_CMD_UNIT] = self._unit

        # data = json.dumps(self.buttonData)
        data = {self.name: self.buttonData}
        _print(data)

        self._icon = ""
        self._color = ""
        self._unit = ""


class BlinkerText(object):
    """ """

    def __init__(self, name):
        self.name = name
        self.textData = {}

        protocol.Texts[name] = self

    def print(self, text1, text2=None):
        self.textData[BLINKER_CMD_TEXT] = text1
        if text2:
            self.textData[BLINKER_CMD_TEXT1] = text2

        # data = json.dumps(self.textData)        
        data = {self.name: self.textData}
        _print(data)


class BlinkerJoystick(object):
    """ """

    def __init__(self, name, func=None):
        self.name = name
        self.func = func

        protocol.Joystick[name] = self

    def attach(self, _func):
        self.func = _func


class BlinkerSwitch(object):
    """ """

    def __init__(self, name=BLINKER_CMD_BUILTIN_SWITCH, func=None):
        self.name = name
        self.func = func

        protocol.Toggles[name] = self

    def attach(self, _func):
        self.func = _func

    def print(self, _state):
        print(self.name, _state)


BUILTIN_SWITCH = BlinkerSwitch()
