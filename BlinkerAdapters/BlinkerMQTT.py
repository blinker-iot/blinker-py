import json
import requests
import paho.mqtt.client as mqtt
from Blinker.BlinkerConfig import *
from Blinker.BlinkerDebug import *
from BlinkerUtility.BlinkerUtility import *

class MQTT_Protol():
    host = ''
    port = ''
    subtopic = ''
    pubtopic = ''
    deviceName = ''
    clientID = ''
    userName = ''
    password = ''
    uuid = ''
    msgBuf = ''
    isRead = False
    state = CONNECTING
    isAlive = False
    printTime = 0
    kaTime = 0
    debug = BLINKER_DEBUG

mProto = MQTT_Protol()

def isDebugAll():
    if mProto.debug == BLINKER_DEBUG_ALL:
        return True
    else:
        return False

def checkKA():
    if mProto.isAlive is False:
        return False
    if (millis() - mProto.kaTime) < BLINKER_MQTT_KEEPALIVE:
        return True
    else:
        mProto.isAlive = False
        return False

def checkCanPrint():
    if checkKA() is False:
        BLINKER_ERR_LOG("MQTT NOT ALIVE OR MSG LIMIT")
        return False
    if (millis() - mProto.printTime) >= BLINKER_MQTT_MSG_LIMIT:
        return True
    BLINKER_ERR_LOG("MQTT NOT ALIVE OR MSG LIMIT")
    return False

def delay10s():
    start = millis()
    time_run = 0
    while time_run < 10000:
        time_run = millis() - start

def checkAuthData(data):
    if data['detail'] == BLINKER_CMD_NOTFOUND:
        while True:
            BLINKER_ERR_LOG("Please make sure you have put in the right AuthKey!")
            delay10s()            

def getInfo(auth):

    host = 'https://iotdev.clz.me'
    url = '/api/v1/user/device/diy/auth?authKey=' + auth

    r = requests.get(url = host + url)
    data = ''

    if r.status_code != 200:
        BLINKER_ERR_LOG('Device Auth Error!')
        return
    else:
        data = r.json()
        checkAuthData(data)
        if isDebugAll() is True:
            BLINKER_LOG('Device Auth Data: ', data)

    deviceName = data['detail']['deviceName']
    iotId = data['detail']['iotId']
    iotToken = data['detail']['iotToken']
    productKey = data['detail']['productKey']
    uuid = data['detail']['uuid']
    broker = data['detail']['broker']

    if isDebugAll() is True:
        BLINKER_LOG('deviceName: ', deviceName)
        BLINKER_LOG('iotId: ', iotId)
        BLINKER_LOG('iotToken: ', iotToken)
        BLINKER_LOG('productKey: ', productKey)
        BLINKER_LOG('uuid: ', uuid)
        BLINKER_LOG('broker: ', broker)

    if (broker == 'aliyun'):
        mProto.host = BLINKER_MQTT_ALIYUN_HOST
        mProto.port = BLINKER_MQTT_ALIYUN_PORT
        mProto.subtopic = '/' + productKey + '/' + deviceName + '/r'
        mProto.pubtopic = '/' + productKey + '/' + deviceName + '/s'
        mProto.clientID = deviceName
        mProto.userName = iotId
    elif (broker == 'qcloud'):
        mProto.host = BLINKER_MQTT_QCLOUD_HOST
        mProto.port = BLINKER_MQTT_QCLOUD_PORT
        mProto.subtopic = productKey + '/' + deviceName + '/r'
        mProto.pubtopic = productKey + '/' + deviceName + '/s'
        mProto.clientID = productKey + deviceName
        mProto.userName =  mProto.clientID + ';' + iotId
    
    mProto.deviceName = deviceName
    mProto.password = iotToken
    mProto.uuid = uuid

    if isDebugAll() is True:
        BLINKER_LOG('clientID: ', mProto.clientID)
        BLINKER_LOG('userName: ', mProto.userName)
        BLINKER_LOG('password: ', mProto.password)
        BLINKER_LOG('subtopic: ', mProto.subtopic)
        BLINKER_LOG('pubtopic: ', mProto.pubtopic)

def on_connect(client, userdata, flags, rc):
    if isDebugAll() is True:
        BLINKER_LOG('Connected with result code '+str(rc))
    if rc == 0:
        mProto.state = CONNECTED
        BLINKER_LOG("MQTT connected")
    else:
        BLINKER_ERR_LOG("MQTT Disconnected")
        return
    client.subscribe(mProto.subtopic)

def on_message(client, userdata, msg):
    if isDebugAll() is True:
        BLINKER_LOG('Subscribe topic: ', msg.topic)
        BLINKER_LOG('payload: ', msg.payload)
    data = msg.payload
    data = data.decode('utf-8')
    # BLINKER_LOG('data: ', data)
    data = json.loads(data)
    data = data['data']
    data = json.dumps(data)
    mProto.msgBuf = data
    mProto.isRead = True
    mProto.isAlive = True
    mProto.kaTime = millis()

class MQTTClient():
    def __init__(self):
        self.auth = ''
        self._isClosed = False

    def start(self, auth):
        self.auth = auth
        getInfo(self.auth)
        self.client = mqtt.Client(client_id = mProto.clientID)
        self.client.username_pw_set(mProto.userName, mProto.password)
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.connect(mProto.host, mProto.port, 60)
        
    def run(self):
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()

    def pub(self, msg, state = False):
        if state is False:
            if checkCanPrint() is False:
                return
        payload = {'fromDevice':mProto.deviceName, 'toDevice':mProto.uuid, 'data':msg}
        payload = json.dumps(payload)
        if isDebugAll() is True:
            BLINKER_LOG('Publish topic: ', mProto.pubtopic)
            BLINKER_LOG('payload: ', payload)
        self.client.publish(mProto.pubtopic, payload)
        mProto.printTime = millis()
