#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import paho.mqtt.client as mqtt
from Blinker.BlinkerConfig import *
from Blinker.BlinkerDebug import *
from BlinkerUtility import *

class MQTTProtocol(object):
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
    isAliRead = False
    isDuerRead = False
    state = CONNECTING
    isAlive = False
    isAliAlive = False
    isDuerAlive = False
    printTime = 0
    aliPrintTime = 0
    duerPrintTime = 0
    kaTime = 0
    aliKaTime = 0
    duerKaTime = 0
    debug = BLINKER_DEBUG
    smsTime = 0
    pushTime = 0
    wechatTime = 0
    weatherTime = 0
    aqiTime = 0

# mProto = MQTTProtocol()

class BlinkerMQTT(MQTTProtocol):
    """ """

    # def isDebugAll(self):
    #     if self.debug == BLINKER_DEBUG_ALL:
    #         return True
    #     else:
    #         return False

    def checkKA(self):
        if self.isAlive is False:
            return False
        if (millis() - self.kaTime) < BLINKER_MQTT_KEEPALIVE:
            return True
        else:
            self.isAlive = False
            return False

    def checkAliKA(self):
        if self.isAliAlive is False:
            return False
        if (millis() - self.aliKaTime) < BLINKER_MQTT_KEEPALIVE:
            return True
        else:
            self.isAliAlive = False
            return False    

    def checkDuerKA(self):
        if self.isDuerAlive is False:
            return False
        if (millis() - self.duerKaTime) < BLINKER_MQTT_KEEPALIVE:
            return True
        else:
            self.isDuerAlive = False
            return False

    def checkCanPrint(self):
        if self.checkKA() is False:
            BLINKER_ERR_LOG("MQTT NOT ALIVE OR MSG LIMIT")
            return False
        if (millis() - self.printTime) >= BLINKER_MQTT_MSG_LIMIT or self.printTime == 0:
            return True
        BLINKER_ERR_LOG("MQTT NOT ALIVE OR MSG LIMIT")
        return False

    def checkAliCanPrint(self):
        if self.checkAliKA() is False:
            BLINKER_ERR_LOG("MQTT NOT ALIVE OR MSG LIMIT")
            return False
        if (millis() - self.aliPrintTime) >= BLINKER_MQTT_MSG_LIMIT or self.aliPrintTime == 0:
            return True
        BLINKER_ERR_LOG("MQTT NOT ALIVE OR MSG LIMIT")
        return False

    def checkDuerCanPrint(self):
        if self.checkDuerKA() is False:
            BLINKER_ERR_LOG("MQTT NOT ALIVE OR MSG LIMIT")
            return False
        if (millis() - self.duerPrintTime) >= BLINKER_MQTT_MSG_LIMIT or self.duerPrintTime == 0:
            return True
        BLINKER_ERR_LOG("MQTT NOT ALIVE OR MSG LIMIT")
        return False

    def checkSMS(self):
        if (millis() - self.smsTime) >= BLINKER_SMS_MSG_LIMIT or self.smsTime == 0:
            return True
        BLINKER_ERR_LOG("SMS MSG LIMIT")
        return False

    def checkPUSH(self):
        if (millis() - self.pushTime) >= BLINKER_PUSH_MSG_LIMIT or self.pushTime == 0:
            return True
        BLINKER_ERR_LOG("PUSH MSG LIMIT")
        return False

    def checkWECHAT(self):
        if (millis() - self.wechatTime) >= BLINKER_PUSH_MSG_LIMIT or self.wechatTime == 0:
            return True
        BLINKER_ERR_LOG("WECHAT MSG LIMIT")
        return False

    def checkWEATHER(self):
        if (millis() - self.weatherTime) >= BLINKER_WEATHER_MSG_LIMIT or self.weatherTime == 0:
            return True
        BLINKER_ERR_LOG("WEATHER MSG LIMIT")
        return False

    def checkAQI(self):
        if (millis() - self.aqiTime) >= BLINKER_AQI_MSG_LIMIT or self.aqiTime == 0:
            return True
        BLINKER_ERR_LOG("AQI MSG LIMIT")
        return False

    def delay10s(self):
        start = millis()
        time_run = 0
        while time_run < 10000:
            time_run = millis() - start

    def checkAuthData(self, data):
        if data['detail'] == BLINKER_CMD_NOTFOUND:
            while True:
                BLINKER_ERR_LOG("Please make sure you have put in the right AuthKey!")
                self.delay10s()

    @classmethod
    def getInfo(cls, auth, aliType, duerType):
        host = 'https://iot.diandeng.tech'
        url = '/api/v1/user/device/diy/auth?authKey=' + auth

        if aliType :
            url = url + aliType

        if duerType :
            url = url + duerType

        r = requests.get(url=host + url)
        data = ''

        if r.status_code != 200:
            BLINKER_ERR_LOG('Device Auth Error!')
            return
        else:
            data = r.json()
            cls().checkAuthData(data)
            # if cls().isDebugAll() is True:
            BLINKER_LOG_ALL('Device Auth Data: ', data)

        deviceName = data['detail']['deviceName']
        iotId = data['detail']['iotId']
        iotToken = data['detail']['iotToken']
        productKey = data['detail']['productKey']
        uuid = data['detail']['uuid']
        broker = data['detail']['broker']

        bmt = cls()

        # if bmt.isDebugAll() is True:
        BLINKER_LOG_ALL('deviceName: ', deviceName)
        BLINKER_LOG_ALL('iotId: ', iotId)
        BLINKER_LOG_ALL('iotToken: ', iotToken)
        BLINKER_LOG_ALL('productKey: ', productKey)
        BLINKER_LOG_ALL('uuid: ', uuid)
        BLINKER_LOG_ALL('broker: ', broker)

        if broker == 'aliyun':
            bmt.host = BLINKER_MQTT_ALIYUN_HOST
            bmt.port = BLINKER_MQTT_ALIYUN_PORT
            bmt.subtopic = '/' + productKey + '/' + deviceName + '/r'
            bmt.pubtopic = '/' + productKey + '/' + deviceName + '/s'
            bmt.clientID = deviceName
            bmt.userName = iotId
        elif broker == 'qcloud':
            bmt.host = BLINKER_MQTT_QCLOUD_HOST
            bmt.port = BLINKER_MQTT_QCLOUD_PORT
            bmt.subtopic = productKey + '/' + deviceName + '/r'
            bmt.pubtopic = productKey + '/' + deviceName + '/s'
            bmt.clientID = productKey + deviceName
            bmt.userName = bmt.clientID + ';' + iotId

        bmt.deviceName = deviceName
        bmt.password = iotToken
        bmt.uuid = uuid

        # if bmt.isDebugAll() is True:
        BLINKER_LOG_ALL('clientID: ', bmt.clientID)
        BLINKER_LOG_ALL('userName: ', bmt.userName)
        BLINKER_LOG_ALL('password: ', bmt.password)
        BLINKER_LOG_ALL('subtopic: ', bmt.subtopic)
        BLINKER_LOG_ALL('pubtopic: ', bmt.pubtopic)

        return bmt


class MQTTClient():
    def __init__(self):
        self.auth = ''
        self._isClosed = False
        self.client = None
        self.bmqtt = None
        self.mProto = BlinkerMQTT()

    def on_connect(self, client, userdata, flags, rc):
        # if self.bmqtt.isDebugAll() is True:
        BLINKER_LOG_ALL('Connected with result code ' + str(rc))
        if rc == 0:
            self.bmqtt.state = CONNECTED
            BLINKER_LOG("MQTT connected")
        else:
            BLINKER_ERR_LOG("MQTT Disconnected")
            return
        client.subscribe(self.bmqtt.subtopic)

    def on_message(self, client, userdata, msg):
        # if self.bmqtt.isDebugAll() is True:
        BLINKER_LOG_ALL('Subscribe topic: ', msg.topic)
        BLINKER_LOG_ALL('payload: ', msg.payload)
        data = msg.payload
        data = data.decode('utf-8')
        # BLINKER_LOG('data: ', data)
        data = json.loads(data)
        fromDevice = data['fromDevice']
        data = data['data']
        data = json.dumps(data)
        # self.bmqtt.msgBuf = data
        # self.bmqtt.isRead = True
        # self.bmqtt.isAlive = True
        # self.bmqtt.kaTime = millis()
        BLINKER_LOG_ALL('data: ', data)
        if fromDevice == self.bmqtt.uuid :
            self.bmqtt.msgBuf = data
            self.bmqtt.isRead = True
            self.bmqtt.isAlive = True
            self.bmqtt.kaTime = millis()
        elif fromDevice == 'AliGenie':
            self.bmqtt.msgBuf = data
            self.bmqtt.isAliRead = True
            self.bmqtt.isAliAlive = True
            self.bmqtt.aliKaTime = millis()        
        elif fromDevice == 'DuerOS':
            self.bmqtt.msgBuf = data
            self.bmqtt.isDuerRead = True
            self.bmqtt.isDuerAlive = True
            self.bmqtt.duerKaTime = millis()  

    def start(self, auth, aliType, duerType):
        self.auth = auth
        self.bmqtt = self.mProto.getInfo(auth, aliType, duerType)
        self.client = mqtt.Client(client_id=self.bmqtt.clientID)
        self.client.username_pw_set(self.bmqtt.userName, self.bmqtt.password)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.bmqtt.host, self.bmqtt.port, 60)

    def run(self):
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()

    def pub(self, msg, state=False):
        if state is False:
            if self.bmqtt.checkCanPrint() is False:
                return
        payload = {'fromDevice': self.bmqtt.deviceName, 'toDevice': self.bmqtt.uuid, 'data': msg , 'deviceType': 'OwnApp'}
        payload = json.dumps(payload)
        # if self.bmqtt.isDebugAll() is True:
        BLINKER_LOG_ALL('Publish topic: ', self.bmqtt.pubtopic)
        BLINKER_LOG_ALL('payload: ', payload)
        self.client.publish(self.bmqtt.pubtopic, payload)
        self.bmqtt.printTime = millis()

    def aliPrint(self, msg):
        if self.bmqtt.checkAliCanPrint() is False:
            return
        payload = {'fromDevice': self.bmqtt.deviceName, 'toDevice': 'AliGenie_r', 'data': msg , 'deviceType': 'vAssistant'}
        payload = json.dumps(payload)
        # if self.bmqtt.isDebugAll() is True:
        BLINKER_LOG_ALL('Publish topic: ', self.bmqtt.pubtopic)
        BLINKER_LOG_ALL('payload: ', payload)
        self.client.publish(self.bmqtt.pubtopic, payload)

    def duerPrint(self, msg):
        if self.bmqtt.checkDuerCanPrint() is False:
            return
        payload = {'fromDevice': self.bmqtt.deviceName, 'toDevice': 'DuerOS_r', 'data': msg , 'deviceType': 'vAssistant'}
        payload = json.dumps(payload)
        # if self.bmqtt.isDebugAll() is True:
        BLINKER_LOG_ALL('Publish topic: ', self.bmqtt.pubtopic)
        BLINKER_LOG_ALL('payload: ', payload)
        self.client.publish(self.bmqtt.pubtopic, payload)

    def sms(self, msg):
        if self.bmqtt.checkSMS() is False:
            return
        payload = json.dumps({'deviceName':self.bmqtt.deviceName, 'key': self.auth, 'msg': msg})
        response = requests.post('https://iot.diandeng.tech/api/v1/user/device/sms',
                                 data=payload, headers={'Content-Type': 'application/json'})

        self.bmqtt.smsTime = millis()
        data = response.json()
        # if self.bmqtt.isDebugAll() is True:
        BLINKER_LOG_ALL('response: ', data)
        if data[BLINKER_CMD_MESSAGE] != 1000:
            BLINKER_ERR_LOG(data[BLINKER_CMD_DETAIL])

    def push(self, msg):
        if self.bmqtt.checkPUSH() is False:
            return
        payload = json.dumps({'deviceName':self.bmqtt.deviceName, 'key': self.auth, 'msg': msg})
        response = requests.post('https://iot.diandeng.tech/api/v1/user/device/push',
                                 data=payload, headers={'Content-Type': 'application/json'})

        self.bmqtt.pushTime = millis()
        data = response.json()
        # if self.bmqtt.isDebugAll() is True:
        BLINKER_LOG_ALL('response: ', data)
        if data[BLINKER_CMD_MESSAGE] != 1000:
            BLINKER_ERR_LOG(data[BLINKER_CMD_DETAIL])

    def wechat(self, title, state, msg):
        if self.bmqtt.checkWECHAT() is False:
            return
        payload = json.dumps({'deviceName':self.bmqtt.deviceName, 'key': self.auth, 'title':title, 'state':state, 'msg': msg})
        response = requests.post('https://iot.diandeng.tech/api/v1/user/device/wxMsg/',
                                 data=payload, headers={'Content-Type': 'application/json'})

        self.bmqtt.pushTime = millis()
        data = response.json()
        # if self.bmqtt.isDebugAll() is True:
        BLINKER_LOG_ALL('response: ', data)
        if data[BLINKER_CMD_MESSAGE] != 1000:
            BLINKER_ERR_LOG(data[BLINKER_CMD_DETAIL])

    def dataUpdate(self, msg):
        payload = json.dumps({'deviceName':self.bmqtt.deviceName, 'key': self.auth, 'data': msg})
        response = requests.post('https://iot.diandeng.tech/api/v1/user/device/cloudStorage/',
                                 data=payload, headers={'Content-Type': 'application/json'})

        self.bmqtt.pushTime = millis()
        data = response.json()
        # if self.bmqtt.isDebugAll() is True:
        BLINKER_LOG_ALL('response: ', data)
        if data[BLINKER_CMD_MESSAGE] != 1000:
            BLINKER_ERR_LOG(data[BLINKER_CMD_DETAIL])
            return False
        return True

    def weather(self, city):
        if self.bmqtt.checkWEATHER() is False:
            return
        host = 'https://iot.diandeng.tech'
        url = '/api/v1/user/device/weather/now?deviceName=' + self.bmqtt.deviceName + '&key=' + self.auth + '&location=' + city

        r = requests.get(url=host + url)
        data = ''

        self.bmqtt.weatherTime = millis()

        if r.status_code != 200:
            BLINKER_ERR_LOG('Device Auth Error!')
            return
        else:
            data = r.json()
            return data['detail']

    def aqi(self, city):
        if self.bmqtt.checkAQI() is False:
            return
        host = 'https://iot.diandeng.tech'
        url = '/api/v1/user/device/weather/now?deviceName=' + self.bmqtt.deviceName + '&key=' + self.auth + '&location=' + city

        r = requests.get(url=host + url)
        data = ''       

        self.bmqtt.aqiTime = millis()

        if r.status_code != 200:
            BLINKER_ERR_LOG('Device Auth Error!')
            return
        else:
            data = r.json()
            return data['detail']


        # payload = json.dumps({'deviceName':self.bmqtt.deviceName, 'key': self.auth, 'title':title, 'state':state, 'msg': msg})
        # response = requests.post('https://iot.diandeng.tech/api/v1/user/device/wxMsg/',
        #                          data=payload, headers={'Content-Type': 'application/json'})

        # self.bmqtt.pushTime = millis()
        # data = response.json()
        # # if self.bmqtt.isDebugAll() is True:
        # BLINKER_LOG_ALL('response: ', data)
        # if data[BLINKER_CMD_MESSAGE] != 1000:
        #     BLINKER_ERR_LOG(data[BLINKER_CMD_DETAIL])
