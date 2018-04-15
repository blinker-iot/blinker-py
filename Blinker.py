import sys
import json
import socket
from BlinkerConfig import *
from BlinkerDebug import *
from threading import Thread
from zeroconf import ServiceInfo, Zeroconf
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

clients = []
deviceName = macDeviceName()
deviceIP = localIP()

def check_json_format(raw_msg):
    if isinstance(raw_msg, str):
        if raw_msg[0] == '{':
            try:
                json.loads(raw_msg, encoding='utf-8')
            except ValueError:
                return False
            return True
        else:
            return False
    else:
        return False

class Protocol():
    conType = BLINKER_WIFI
    isAvail = False
    isRead = False
    msgBuf = ""
    Buttons = {}
    Sliders = {}
    Toggles = {}
    Joystick = [BLINKER_JOYSTICK_VALUE_DEFAULT, BLINKER_JOYSTICK_VALUE_DEFAULT]
    Ahrs = [0, 0, 0]

    # def parse(self):
    #     data = str(Protocol.msgBuf)
    #     BLINKER_LOG(data, check_json_format(data))

bProto = Protocol()

def mDNSinit():
    info = ServiceInfo("_DiyArduino._tcp.local.",
                       deviceName + "._DiyArduino._tcp.local.",
                       socket.inet_aton(deviceIP), wsPort, 0, 0,
                       "", deviceName + ".local.")

    zeroconf = Zeroconf()
    zeroconf.register_service(info)

    BLINKER_LOG('mDNS responder init!')

class HandleServer(WebSocket):

    def handleMessage(self):
        bProto.msgBuf = self.data
        # bProto.isAvail = True
        bProto.isRead = True
        parse()
        # BLINKER_LOG('Read data: ', self.data)
        
    def handleConnected(self):
        clients.append(self)
        # BLINKER_LOG(self.address, 'connected')

    def handleClose(self):
        clients.remove(self)
        # BLINKER_LOG(self.address, 'closed')

class WebSocketServer(Thread):
    def __init__(self, name, port):
        Thread.__init__(self)
        self.server = SimpleWebSocketServer(deviceIP, wsPort, HandleServer)
        self._isClosed = False
        mDNSinit()
        BLINKER_LOG('websocket Server init')
        BLINKER_LOG('ws://', deviceIP, ':', wsPort)
        self.setDaemon(True)

    def start(self):
        super(WebSocketServer, self).start()

    def run(self):
        self.server.serveforever()

    def stop(self):
        self.server.close()
        self._isClosed = True

    def broadcast(self, msg):
        if isinstance(msg, str):
            msg = unicode(msg, "utf-8")
        for client in clients:
            client.sendMessage(msg)
            while client.sendq:
                opcode, payload = client.sendq.popleft()
                remaining = client._sendBuffer(payload)
                if remaining is not None:
                    client.sendq.appendleft((opcode, remaining))
                    break

bWSServer = WebSocketServer(deviceIP, wsPort)

def setMode(setType = BLINKER_WIFI):
    bProto.conType = setType

def begin():
    if bProto.conType == BLINKER_BLE:
        return
    elif bProto.conType == BLINKER_WIFI:
        bWSServer.start()

def wInit(name, wType):
    if wType == W_BUTTON:
        if bProto.Buttons.has_key(name):
            return
        else:
            bProto.Buttons[name] = False
        # BLINKER_LOG(bProto.Buttons)

    elif wType == W_SLIDER:
        if bProto.Sliders.has_key(name):
            return
        else:
            bProto.Sliders[name] = 0
        # BLINKER_LOG(bProto.Sliders)

    elif wType == W_TOGGLE:
        if bProto.Toggles.has_key(name):
            return
        else:
            bProto.Toggles[name] = False
        # BLINKER_LOG(bProto.Toggles)

def Print(data):
    if bProto.conType == BLINKER_BLE:
        return
    elif bProto.conType == BLINKER_WIFI:
        data = str(data)
        bWSServer.broadcast(data)
        BLINKER_LOG('Send data: ', data)

def available():
    return bProto.isAvail

def readString():
    bProto.isRead = False
    bProto.isAvail = False
    return bProto.msgBuf

def times():
    return now()

def parse():
    data = str(bProto.msgBuf)
    if check_json_format(data):
        data = json.loads(data)
        for key in data.keys():
            # BLINKER_LOG(key)
            if bProto.Buttons.has_key(key):
                # bProto.isAvail = False
                bProto.isRead = False
                if data[key] == BLINKER_CMD_BUTTON_PRESSED:
                    bProto.Buttons[key] = True
                else:
                    bProto.Buttons[key] = False
                # BLINKER_LOG(bProto.Buttons)

            elif bProto.Sliders.has_key(key):
                # bProto.isAvail = False
                bProto.isRead = False
                bProto.Sliders[key] = data[key]
                # BLINKER_LOG(bProto.Buttons)

            elif bProto.Toggles.has_key(key):
                # bProto.isAvail = False
                bProto.isRead = False
                if data[key] == BLINKER_CMD_ON:
                    bProto.Toggles[key] = True
                else:
                    bProto.Toggles[key] = False
                # BLINKER_LOG(bProto.Toggles)
            
            elif key == BLINKER_CMD_JOYSTICK:
                # bProto.isAvail = False
                bProto.isRead = False
                bProto.Joystick[J_Xaxis] = data[key][J_Xaxis]
                bProto.Joystick[J_Yaxis] = data[key][J_Yaxis]
                # BLINKER_LOG(bProto.Joystick)

            elif key == BLINKER_CMD_AHRS:
                # bProto.isAvail = False
                bProto.isRead = False
                bProto.Ahrs[Yaw] = data[key][Yaw]
                bProto.Ahrs[Pitch] = data[key][Pitch]
                bProto.Ahrs[Roll] = data[key][Roll]
                # BLINKER_LOG(bProto.Ahrs)

        if bProto.isRead:
            bProto.isAvail = True
        # BLINKER_LOG(data.keys())
    else:
        if bProto.isRead:
            bProto.isAvail = True
        return

def button(name):
    if bProto.Buttons.has_key(name):
        state = bProto.Buttons[name]
        bProto.Buttons[name] = False
        return state
    else:
        wInit(name, W_BUTTON)
        parse()
        state = bProto.Buttons[name]
        bProto.Buttons[name] = False
        return state

def slider(name):
    if bProto.Sliders.has_key(name):
        return bProto.Sliders[name]
    else:
        wInit(name, W_SLIDER)
        parse()
        return bProto.Sliders[name]

def toggle(name):
    if bProto.Toggles.has_key(name):
        return bProto.Toggles[name]
    else:
        wInit(name, W_TOGGLE)
        parse()
        return bProto.Toggles[name]

def joystick(axis):
    if axis >= J_Xaxis and axis <= J_Yaxis:
        return bProto.Joystick[axis]
    else:
        return BLINKER_JOYSTICK_VALUE_DEFAULT

def ahrs(axis):
    if axis >= Yaw and axis <= Roll:
        return bProto.Ahrs[axis]
    else:
        return 0
