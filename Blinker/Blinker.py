import sys
import json
import socket
from Blinker.BlinkerConfig import *
from Blinker.BlinkerDebug import *
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

def json_encode(key, value):
    data = {}
    data[key] = value
    data = json.dumps(data)
    return data

class Protocol():
    conType = BLINKER_WIFI
    state = CONNECTING
    isAvail = False
    isRead = False
    msgBuf = ""
    Buttons = {}
    Sliders = {}
    Toggles = {}
    Joystick = [BLINKER_JOYSTICK_VALUE_DEFAULT, BLINKER_JOYSTICK_VALUE_DEFAULT]
    Ahrs = [0, 0, 0, False]
    GPS = ["0.000000", "0.000000"]
    RGB = {}

    # def parse(self):
    #     data = str(Protocol.msgBuf)
    #     BLINKER_LOG(data, check_json_format(data))

bProto = Protocol()

def mDNSinit():
    # deviceType = '_DiyArduino'
    deviceType = '_DiyLinux'
    desc = {'deviceType': deviceType}

    info = ServiceInfo(deviceType + "._tcp.local.",
                       deviceName + "." + deviceType +"._tcp.local.",
                       socket.inet_aton(deviceIP), wsPort, 0, 0,
                       desc, deviceName + ".local.")

    zeroconf = Zeroconf()
    zeroconf.register_service(info)

    BLINKER_LOG('mDNS responder init!')

class HandleServer(WebSocket):

    def handleMessage(self):
        bProto.msgBuf = self.data
        # bProto.isAvail = True
        bProto.isRead = True
        parse()
        BLINKER_LOG('Read data: ', self.data)
        
    def handleConnected(self):
        clients.append(self)
        msg = json_encode(BLINKER_CMD_STATE, BLINKER_CMD_CONNECTED)
        for client in clients:
            client.sendMessage(msg)
        BLINKER_LOG(self.address, 'connected')
        bProto.state = CONNECTED

    def handleClose(self):
        clients.remove(self)
        BLINKER_LOG(self.address, 'closed')
        if len(clients) == 0:
            bProto.state = DISCONNECTED

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
            msg = msg.encode('utf-8').decode("utf-8")
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
        if name in bProto.Buttons:
            return
        else:
            bProto.Buttons[name] = BLINKER_CMD_BUTTON_RELEASED
        # BLINKER_LOG(bProto.Buttons)

    elif wType == W_SLIDER:
        if name in bProto.Sliders:
            return
        else:
            bProto.Sliders[name] = 0
        # BLINKER_LOG(bProto.Sliders)

    elif wType == W_TOGGLE:
        if name in bProto.Toggles:
            return
        else:
            bProto.Toggles[name] = False

    elif wType == W_RGB:
        if name in bProto.RGB:
            return
        else:
            rgb = [0, 0, 0]
            bProto.RGB[name] = rgb
        BLINKER_LOG(bProto.Toggles)

def print(key, value = None, uint = None):
    if bProto.conType == BLINKER_BLE:
        return
    elif bProto.conType == BLINKER_WIFI:
        if value is None:
            data = str(key)
        else:
            key = str(key)
            if not uint is None:
                value = str(value) + str(uint)
            data = json_encode(key, value)
        if len(data) > BLINKER_MAX_SEND_SIZE:
            BLINKER_ERR_LOG('SEND DATA BYTES MAX THAN LIMIT!')
            return
        bWSServer.broadcast(data)
        BLINKER_LOG('Send data: ', data)

def notify(msg):
    print(BLINKER_CMD_NOTICE, msg)

def connected():
    if bProto.state is CONNECTED:
        return True
    else:
        return False 

def connect(timeout = BLINKER_STREAM_TIMEOUT):
    bProto.state = CONNECTING
    start_time = millis()
    while (millis() - start_time) < timeout:
        parse()
        if bProto.state is CONNECTED:
            return True
    return False

def disconnect():
    bProto.state = DISCONNECTED

def delay(ms):
    start = millis()
    time_run = 0
    while time_run < ms:
        time_run = millis() - start

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
                bProto.Ahrs[AHRS_state] = True
                # BLINKER_LOG(bProto.Ahrs)

            elif key == BLINKER_CMD_GPS:
                bProto.isRead = False
                bProto.GPS[LONG] = str(data[key][LONG])
                bProto.GPS[LAT] = str(data[key][LAT])

        if bProto.isRead:
            bProto.isAvail = True
        # BLINKER_LOG(data.keys())
    else:
        if bProto.isRead:
            bProto.isAvail = True
        return

def button(name):
    if not name in bProto.Buttons:
        wInit(name, W_BUTTON)
        parse()

    if bProto.Buttons[name] is BLINKER_CMD_BUTTON_RELEASED:
        return False
    
    if bProto.Buttons[name] is BLINKER_CMD_BUTTON_TAP:
        bProto.Buttons[name] = BLINKER_CMD_BUTTON_RELEASED
    return True

def slider(name):
    if name in bProto.Sliders:
        return bProto.Sliders[name]
    else:
        wInit(name, W_SLIDER)
        parse()
        return bProto.Sliders[name]

def toggle(name):
    if name in bProto.Toggles:
        return bProto.Toggles[name]
    else:
        wInit(name, W_TOGGLE)
        parse()
        return bProto.Toggles[name]

def rgb(name, color):
    if name in bProto.RGB:
        return bProto.RGB[name][color]
    else:
        wInit(name, W_RGB)
        parse()
        return bProto.RGB[name][color]

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

def attachAhrs():
    state = False
    while connected() is False:
        connect()
    print(BLINKER_CMD_AHRS, BLINKER_CMD_ON)
    delay(100)
    parse()
    start_time = millis()
    state = bProto.Ahrs[AHRS_state]
    while state is False:
        if (millis() - start_time) > BLINKER_CONNECT_TIMEOUT_MS:
            BLINKER_LOG("AHRS attach failed...Try again")
            start_time = millis()
            print(BLINKER_CMD_AHRS, BLINKER_CMD_ON)
            delay(100)
            parse()
        state = bProto.Ahrs[AHRS_state]
    BLINKER_LOG("AHRS attach sucessed...")

def detachAhrs():
    print(BLINKER_CMD_AHRS, BLINKER_CMD_OFF)
    bProto.Ahrs[Yaw] = 0
    bProto.Ahrs[Roll] = 0
    bProto.Ahrs[Pitch] = 0
    bProto.Ahrs[AHRS_state] = False

def gps(axis):
    print(BLINKER_CMD_GET, BLINKER_CMD_GPS)
    delay(100)
    parse()
    if axis >= LONG and axis <= LAT:
        return bProto.GPS[axis]
    else:
        return "0.000000"

def vibrate(time = 500):
    if time > 1000:
        time = 1000
    print(BLINKER_CMD_VIBRATE, time)
