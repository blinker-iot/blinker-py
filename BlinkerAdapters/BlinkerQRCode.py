#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import paho.mqtt.client as mqtt
from Blinker.BlinkerConfig import *
from Blinker.BlinkerDebug import *
from BlinkerUtility import *
import demjson
import base64
import qrcode
import threading
import time
import os
import chardet


class MQTTProtocol(object):
    host = ''
    port = ''
    subtopic = ''
    exatopic = ''
    exapubtopic = ''
    message_id = ''
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
    isMiRead = False
    state = CONNECTING
    isAlive = False
    isAliAlive = False
    isDuerAlive = False
    isMiAlive = False
    printTime = 0
    aliPrintTime = 0
    duerPrintTime = 0
    miPrintTime = 0
    kaTime = 0
    aliKaTime = 0
    duerKaTime = 0
    miKaTime = 0
    debug = BLINKER_DEBUG
    smsTime = 0
    pushTime = 0
    wechatTime = 0
    weatherTime = 0
    aqiTime = 0
    isAuth = False
    registerKey = ''
    times = 0


def text_create(name, msg):
    desktop_path = "..\\"
    full_path = name + '.txt'
    file = open(full_path, 'w')
    file.write(msg)


def check_auth_file():
    if os.path.exists('auth.txt'):
        BLINKER_LOG_ALL('auth file exists')
        f = open("auth.txt","r")
        line = f.readline()
        BLINKER_LOG_ALL(line)

        if line == 'not register':
            return False
        else:
            return line
    else:
        BLINKER_LOG_ALL('text_create')
        text_create('auth', 'not register')
        return False


def auth_file_write(msg):
    file = open('auth.txt', 'w')
    file.write(msg)


def qrcode_display(key_display):
    qr = qrcode.QRCode(
        # version=1,
        # error_correction=qrcode.constants.ERROR_CORRECT_L,
        # box_size=10,
        # border=4,
    )

    BLINKER_LOG_ALL('key_display: ', key_display)
    # fencoding = chardet.detect(key_display)
    # BLINKER_LOG_ALL(fencoding)

    qr.add_data(key_display)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.show()
    # qr.print_ascii(out=None, tty=False, invert=False)

times = 0

def auth_check(urls):
    global times
    times = times + 1
    BLINKER_LOG_ALL("times: " + str(times))
    # global timer

    r = requests.get(url=urls)

    if r.status_code != 200:
        BLINKER_LOG_ALL('Device Auth Error!')
    else:
        data = r.json()
        BLINKER_LOG_ALL(data)
        if data['message'] == -1 :
            pass
        else :
            return

    if times < 6 :
        timer = threading.Timer(10.0, auth_check, [urls])
        timer.start()
    else :
        pass


class BlinkerMQTTQRCode(MQTTProtocol):
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
            return False    

    def checkMiKA(self):
        if self.isMiAlive is False:
            return False
        if (millis() - self.miKaTime) < BLINKER_MQTT_KEEPALIVE:
            return True
        else:
            self.isMiAlive = False
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

    def checkMiCanPrint(self):
        if self.checkMiKA() is False:
            BLINKER_ERR_LOG("MQTT NOT ALIVE OR MSG LIMIT")
            return False
        if (millis() - self.miPrintTime) >= BLINKER_MQTT_MSG_LIMIT or self.miPrintTime == 0:
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
    def getInfo(cls, type, auth, time, aliType, duerType, miType):
        bmt = cls()
        bmt.isAuth = check_auth_file()

        host = 'https://iot.diandeng.tech'
        url = '/api/v1/user/device/scancode/add?deviceType=' + type + '&typeKey=' + auth + '&expiredIn=' + str(time)

        if bmt.isAuth == False:
            if aliType :
                url = url + aliType

            if duerType :
                url = url + duerType

            if miType :
                url = url + miType

            BLINKER_LOG_ALL('url: ', host + url)

            r = requests.get(url=host + url)
            data = ''
            
            bmt.times = time / 10

            if r.status_code != 200:
                BLINKER_ERR_LOG('Device Auth Error!')
                return
            else:
                data = r.json()
                bmt.registerKey = data['detail']
                BLINKER_LOG_ALL('registerKey: ', bmt.registerKey)
                
                url = '/api/v1/user/device/scancode/auth/get?deviceType=' + type + '&typeKey=' + auth + '&register=' + bmt.registerKey

                if bmt.isAuth == False:
                    qrcode_display(bmt.registerKey)

                    global times
                    times = 0

                    timer = threading.Timer(10.0, auth_check, [host + url])
                    timer.start()
                else:
                    bmt.registerKey  = check_auth_file()
                    pass
        else:
            bmt.registerKey  = check_auth_file()

        url = '/api/v1/user/device/scancode/auth/get?deviceType=' + type + '&typeKey=' + auth + '&register=' + bmt.registerKey

        r = requests.get(url=host + url)
        data = r.json()
        BLINKER_LOG_ALL(data)
        if data['message'] == -1 :
            bmt.isAuth = False
            pass
        elif data['message'] == 1000 :
            auth_file_write(bmt.registerKey)
            bmt.isAuth = True

            cls().checkAuthData(data)
            # if cls().isDebugAll() is True:
            BLINKER_LOG_ALL('Device Auth Data: ', data)

            deviceName = data['detail']['deviceName']
            iotId = data['detail']['iotId']
            iotToken = data['detail']['iotToken']
            productKey = data['detail']['productKey']
            uuid = data['detail']['uuid']
            broker = data['detail']['broker']

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
                bmt.exatopic = '/sys/' + productKey + '/' + deviceName + '/rrpc/request/+'
                bmt.exapubtopic = '/sys/' + productKey + '/' + deviceName + '/rrpc/response/'
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


class MQTTClientQRCode():
    def __init__(self):
        self.type = ''
        self.auth = ''
        self._isClosed = False
        self.client = None
        self.bmqtt = None
        self.mProto = BlinkerMQTTQRCode()

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

        get_topic = msg.topic[0:55]
        message_id = msg.topic[55:]

        self.bmqtt.message_id = message_id

        BLINKER_LOG_ALL('Get topic: ', get_topic)
        BLINKER_LOG_ALL('message_id: ', message_id)

        data = msg.payload
        # if get_topic != self.bmqtt.exatopic:
        data = data.decode('utf-8')
        BLINKER_LOG('data: ', data)
        data = demjson.decode(data)
        BLINKER_LOG('data: ', data)
        fromDevice = data['fromDevice']
        data = data['data']
        data = json.dumps(data)
        # else :

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
        elif fromDevice == 'MIOT':
            self.bmqtt.msgBuf = data
            self.bmqtt.isMiRead = True
            self.bmqtt.isMiAlive = True
            self.bmqtt.miKaTime = millis() 

    def start(self, type, auth, time, aliType, duerType, miType):
        self.type = type
        self.auth = auth
        self.bmqtt = self.mProto.getInfo(type, auth, time, aliType, duerType, miType)
        # if bmt.isAuth == True:
        #     self.client = mqtt.Client(client_id=self.bmqtt.clientID)
        #     self.client.username_pw_set(self.bmqtt.userName, self.bmqtt.password)
        #     self.client.on_connect = self.on_connect
        #     self.client.on_message = self.on_message
        #     self.client.connect(self.bmqtt.host, self.bmqtt.port, 60)

    def connect(self):
        if self.bmqtt.isAuth == True:
            self.client = mqtt.Client(client_id=self.bmqtt.clientID)
            self.client.username_pw_set(self.bmqtt.userName, self.bmqtt.password)
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message
            self.client.connect(self.bmqtt.host, self.bmqtt.port, 60)

            return True
        else :
            return False


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
        pub_topic = self.bmqtt.exapubtopic + self.bmqtt.message_id
        BLINKER_LOG_ALL('Publish topic: ', pub_topic)
        payload = base64.b64encode(payload.encode("utf-8"))
        payload = str(payload, encoding = "utf-8")  
        BLINKER_LOG_ALL('payload: ', payload)
        self.client.publish(pub_topic, payload)

    def duerPrint(self, msg):
        if self.bmqtt.checkDuerCanPrint() is False:
            return
        payload = {'fromDevice': self.bmqtt.deviceName, 'toDevice': 'DuerOS_r', 'data': msg , 'deviceType': 'vAssistant'}
        payload = json.dumps(payload)
        # if self.bmqtt.isDebugAll() is True:
        pub_topic = self.bmqtt.exapubtopic + self.bmqtt.message_id
        BLINKER_LOG_ALL('Publish topic: ', pub_topic)
        payload = base64.b64encode(payload.encode("utf-8"))
        # payload.decode('utf-8')
        payload = str(payload, encoding = "utf-8")  
        BLINKER_LOG_ALL('payload: ', payload)
        # BLINKER_LOG_ALL('payload: ', base64.b64decode(payload))
        self.client.publish(pub_topic, payload)

    def miPrint(self, msg):
        if self.bmqtt.checkMiCanPrint() is False:
            return
        payload = {'fromDevice': self.bmqtt.deviceName, 'toDevice': 'MIOT_r', 'data': msg , 'deviceType': 'vAssistant'}
        payload = json.dumps(payload)
        # if self.bmqtt.isDebugAll() is True:
        pub_topic = self.bmqtt.exapubtopic + self.bmqtt.message_id
        BLINKER_LOG_ALL('Publish topic: ', pub_topic)
        payload = base64.b64encode(payload.encode("utf-8"))
        # payload.decode('utf-8')
        payload = str(payload, encoding = "utf-8")  
        BLINKER_LOG_ALL('payload: ', payload)
        # BLINKER_LOG_ALL('payload: ', base64.b64decode(payload))
        self.client.publish(pub_topic, payload)

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
