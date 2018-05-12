from threading import Thread
from zeroconf import ServiceInfo, Zeroconf
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from Blinker.BlinkerConfig import *
from Blinker.BlinkerDebug import *
from BlinkerUtility.BlinkerUtility import *

clients = []
deviceName = macDeviceName()
deviceIP = localIP()

class WS_Protol():
    msgBuf = ''
    isRead = False
    state = CONNECTING

wsProto = WS_Protol()

def mDNSinit():
    deviceType = '_DiyArduino'
    # deviceType = '_DiyLinux'
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
        # bProto.msgBuf = self.data
        # bProto.isRead = True
        wsProto.msgBuf = self.data
        wsProto.isRead = True
        # parse()
        # dataGet(self.data)
        BLINKER_LOG('Read data: ', self.data)
        
    def handleConnected(self):
        clients.append(self)
        msg = json_encode(BLINKER_CMD_STATE, BLINKER_CMD_CONNECTED)
        for client in clients:
            client.sendMessage(msg)
        BLINKER_LOG(self.address, 'connected')
        wsProto.state = CONNECTED
        # freshState(CONNECTED)
        # bProto.state = CONNECTED

    def handleClose(self):
        clients.remove(self)
        BLINKER_LOG(self.address, 'closed')
        if len(clients) == 0:
            wsProto.state = DISCONNECTED
        #     bProto.state = DISCONNECTED
        #     freshState(DISCONNECTED)

class WebSocketServer(Thread):
    def __init__(self, name, port):
        Thread.__init__(self)
        self.server = SimpleWebSocketServer(deviceIP, wsPort, HandleServer)
        self._isClosed = False
        mDNSinit()
        # BLINKER_LOG('websocket Server init')
        # BLINKER_LOG('ws://', deviceIP, ':', wsPort)
        self.setDaemon(True)

    def start(self):
        BLINKER_LOG('websocket Server init')
        BLINKER_LOG('ws://', deviceIP, ':', wsPort)
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