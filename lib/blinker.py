import paho.mqtt.client as mqtt
import requests
import rx


class BlinkerDevice:

    options: authOption = {
        version: '1.0',
        protocol: 'mqtts',
        webSocket: true
    }

    mqttClient: mqtt.MqttClient

    wsServer
    ws

    config: {
        broker: string,
        deviceName: string,
        host: string,
        iotId: string,
        iotToken: string,
        port: string,
        productKey: string,
        uuid: string,
        authKey?: string
    }

    subTopic
    pubTopic

    deviceName

    targetDevice

    dataRead = new Subject < Message > ()

    heartbeat = new Subject < Message > ()

    builtinSwitch = new BuiltinSwitch()

    configReady = new BehaviorSubject(false)

    widgetKeyList = []
    widgetDict = {}

    sharedUserList = []

    __tempData
    __tempDataPath

    def __init__(this, authkey='', options?: authOption):
        # if authkey == '':
        #     authkey = loadJsonFile('.auth.json').authkey

        # for option in options:
        #     this.options[key] = options
        
        # this.options['authKey'] = authkey
        # this.init(authkey)

    # def init(this, authkey):
    #     axios.get(API.AUTH, {params: this.options}).then(async resp= > {
    #         console.log(resp.data)
    #         if (resp.data.message != 1000) {
    #             error(resp.data)
    #             return
    #         }
    #         this.config=resp.data.detail
    #         this.config['authKey']=authkey
    #         if (this.config.broker == 'aliyun') {
    #             mqttLog('broker:aliyun')
    #             this.initBroker_Aliyun()
    #         } else if (this.config.broker == 'blinker') {
    #             mqttLog('broker:blinker')
    #             this.initBroker_Blinker()
    #         }
    #         await this.connectBroker()
    #         this.addWidget(this.builtinSwitch)
    #         this.getShareInfo()
    #         this.initLocalService()
    #         // 加载暂存数据
    #         this.tempDataPath= `.${this.config.deviceName}.json`
    #         this.tempData=loadJsonFile(this.tempDataPath)
    #         this.loadTimingTask()
    #         this.configReady.next(true)
    #     })
