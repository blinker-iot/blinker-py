#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "stao"

import asyncio
import math
import threading
import time
import websockets

from asyncio.coroutines import iscoroutinefunction
from apscheduler.schedulers.background import BackgroundScheduler
from getmac import get_mac_address
from zeroconf import ServiceInfo, Zeroconf
from threading import Event
from queue import SimpleQueue

from loguru import logger

from .httpclient import *
from .mqttclient import *
from .cache import *
from .errors import *

__all__ = ["Device"]


class DeviceConf(object):
    def __init__(self, /, **kw):
        self.__dict__.update(kw)


class Device(object):
    """
    :param auth_key
    :param version
    :param protocol
    :param ali_type
    :param duer_type
    :param mi_type
    :param heartbeat_func
    :param ready_func
    """

    mqtt_client = None
    http_client = HttpClient()
    config: DeviceConf = None
    widgets = {}
    target_device = None
    shared_user_list = []
    cache_data = None

    voice_assistant = None

    received_data = SimpleQueue()
    data_reader = SimpleQueue()

    scheduler = BackgroundScheduler(timezone="Asia/Shanghai")

    auth_finished = Event()
    auth_finished.clear()
    mqtt_connected = Event()
    mqtt_connected.clear()

    # timing_tasks = TimingTasks()

    def __init__(self, auth_key, protocol: str = "mqtt", version: str = "1.0", ali_type: str = None,
                 duer_type: str = None, mi_type: str = None, websocket: bool = False, heartbeat_func=None,
                 ready_func=None):
        self.auth_key = auth_key
        self.version = version
        self.protocol = protocol
        self.ali_type = ali_type
        self.duer_type = duer_type
        self.mi_type = mi_type

        self.websocket = websocket
        self._heartbeat_callable = heartbeat_func
        self._ready_callable = ready_func

    @property
    def heartbeat_callable(self):
        return self._heartbeat_callable

    @heartbeat_callable.setter
    def heartbeat_callable(self, func):
        self._heartbeat_callable = func

    @property
    def ready_callable(self):
        return self._ready_callable

    @ready_callable.setter
    def ready_callable(self, func):
        self._ready_callable = func

    def scheduler_run(self):
        self.scheduler.start()
        print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

        try:
            # This is here to simulate application activity (which keeps the main thread alive).
            while True:
                time.sleep(2)
        except (KeyboardInterrupt, SystemExit):
            # Not strictly necessary if daemonic mode is enabled but should be done if possible
            self.scheduler.shutdown()

    async def _custom_runner(self, func):
        self.auth_finished.wait()
        self.mqtt_connected.wait()

        if iscoroutinefunction(func):
            await func()
        else:
            func()

    def add_widget(self, widget):
        widget.device = self
        self.widgets[widget.key] = widget
        return widget

    def addVoiceAssistant(self, voice_assistant):
        voice_assistant.device = self
        self.voice_assistant = voice_assistant
        return voice_assistant

    async def device_init(self):
        broker_info = await self.http_client.diy_device_auth(
            self.auth_key,
            self.protocol,
            self.version,
            self.ali_type,
            self.duer_type,
            self.mi_type
        )

        self.config = DeviceConf(**broker_info)

        share_info_res = await self.http_client.get_share_info()
        self.shared_user_list = share_info_res["users"]

        from .widget import BuiltinSwitch
        self.add_widget(BuiltinSwitch())

        # # 加载缓存数据
        # self.cache_data = CacheData(self.broker.deviceName)
        # self.timing_tasks.load()

        self.auth_finished.set()
        logger.success("Device auth successful...")

    async def mqttclient_init(self):
        self.auth_finished.wait()
        self.mqtt_client = MqttClient(self)
        await self.mqtt_client.connection()

    async def _cloud_heartbeat(self):
        """云端心跳上报 """

        self.auth_finished.wait()
        while True:
            logger.info("Send cloud heartbeat")
            await self.http_client.cloud_heartbeat()
            await asyncio.sleep(600)

    async def sendMessage(self, message: Dict, to_device: str):
        self.mqtt_client.send_to_device(message, to_device)

    async def set_position(self, lng, lat):
        await self.http_client.set_position(lng, lat)

    def vibrate(self, t=500):
        self.mqtt_client.send_to_device({"vibrate": t})

    def disable_timing_task(self, task):
        pass

    def execution_timing_task(self, act):
        self.received_data.put(act)

    def add_timing_task(self, task_data):
        if task_data["ena"] == 0:
            self.disable_timing_task(task_data["task"])
        else:
            hour = math.floor(task_data["tim"] / 60)
            minute = task_data["tim"] % 60

            day_of_week = []
            for i in range(len(task_data["day"])):
                if task_data["day"][i] == "1":
                    day_of_week.append((str(i)))

            conf = {"minute": minute, "hour": hour}
            if day_of_week:
                conf["day_of_week"] = ",".join(day_of_week)

            self.scheduler.add_job(self.execution_timing_task(task_data["act"][0]), "cron", **conf)

    async def _receiver(self):
        self.mqtt_connected.wait()

        logger.success("Receiver ready...")
        while True:
            data = self.received_data.get()
            logger.info("received msg: {0}".format(data))

            if isinstance(data, str):
                data = json.loads(data)

            self.target_device = data["fromDevice"]
            received_data = data["data"]

            if "get" in received_data:
                if received_data["get"] == "state":
                    if self.heartbeat_callable:
                        await self.heartbeat_callable()
                    self.mqtt_client.send_to_device({"state": "online"})
                elif received_data["get"] == "timing":
                    # TODO 反馈定时任务
                    pass
                elif received_data["get"] == "countdown":
                    # TODO 反馈倒计时任务
                    pass
            elif "set" in received_data:
                if "timing" in received_data["set"]:
                    if "dlt" in received_data["set"]["timing"][0]:
                        # TODO 删除定时
                        pass
                    else:
                        # TODO 设置定时任务
                        pass
                    # TODO 反馈定时任务
                elif "countdown" in received_data["set"]:
                    # TODO 设定并反馈倒计时任务
                    pass
            elif "rt" in received_data:
                # TODO 实时数据
                pass
            else:
                for key in received_data.keys():
                    if key in self.widgets.keys():
                        await self.widgets[key].handler(data)
                    else:
                        self.data_reader.put({"fromDevice": self.target_device, "data": {key: received_data[key]}})

            await asyncio.sleep(0)

    async def _websocket_action(self, websocket):
        async for message in websocket:
            logger.info("websocket received msg: {0}".format(message))
            self.received_data.put(message)

    async def init_local_service(self):
        self.auth_finished.wait()

        zero_conf = Zeroconf()
        # deviceType = '_' + typea
        # desc = {'deviceName': name}
        # desc = {}

        # info = ServiceInfo(deviceType + "._tcp.local.",
        #                    name + "." + deviceType + "._tcp.local.",
        #                    socket.inet_aton(deviceIP), 81, 0, 0,
        #                    desc, name + ".local.")
        info = ServiceInfo(
            type_="_blinker_" + self.config.deviceName[:12] + '._tcp.local.',
            name="_" + self.config.deviceName[:12] + '._tcp.local.',
            port=81,
            server="blinker",
            properties={
                "mac": get_mac_address().replace(":", "").upper()
            }
        )
        await zero_conf.async_register_service(info)
        async with websockets.serve(self._websocket_action, "localhost", 81):
            await asyncio.Future()

    # 短信通知
    async def sendSms(self, data: str):
        await self.http_client.send_sms(data[:20])
        await asyncio.sleep(60)

    # 微信通知
    async def wechat(self, title: str, state: str, text: str):
        await self.http_client.send_wx_template_msg(title, state, text)

    # App通知
    async def push(self, data: str):
        await self.http_client.send_push_msg(data)

    # 数据存储
    async def saveTsData(self, data: Dict):
        req_data = {}
        for key, value in data.items():
            if not isinstance(value, (int, float)):
                return BlinkerException(-1, "Value error")

            req_data[key] = [[int(time.time()), value]]
        await self.http_client.save_ts_data(req_data)
        await asyncio.sleep(60)

    async def saveObjectData(self, data: Dict):
        self.mqtt_client.send_obj_data(data)
        await asyncio.sleep(60)

    async def saveTextData(self, data: str):
        await self.mqtt_client.send_text_data(data)
        await asyncio.sleep(60)

    async def saveLogData(self, data: str):
        req_data = [[int(time.time()), data]]
        await self.http_client.save_log_data(req_data)
        await asyncio.sleep(60)

    # 气象数据
    async def getAir(self, city_code=""):
        return await self.http_client.get_air(city_code)

    async def getWeather(self, city_code=""):
        return await self.http_client.get_weather(city_code)

    async def getWeatherForecast(self, city_code=""):
        return await self.http_client.get_forecast(city_code)

    async def main(self):
        tasks = [
            threading.Thread(target=asyncio.run, args=(self.device_init(),)),
            threading.Thread(target=asyncio.run, args=(self.mqttclient_init(),)),
            threading.Thread(target=asyncio.run, args=(self._cloud_heartbeat(),)),
            threading.Thread(target=asyncio.run, args=(self._receiver(),)),
            threading.Thread(target=self.scheduler_run)
        ]

        if self.websocket:
            tasks.append(threading.Thread(target=asyncio.run, args=(self.init_local_service(),)))

        if self.heartbeat_callable:
            tasks.append(threading.Thread(target=asyncio.run, args=(self._custom_runner(self.heartbeat_callable),)))

        if self.ready_callable:
            tasks.append(threading.Thread(target=asyncio.run, args=(self._custom_runner(self.ready_callable),)))

        if self.voice_assistant:
            tasks.append(threading.Thread(target=asyncio.run, args=(self.voice_assistant.listen(),)))

        # start
        for task in tasks:
            task.start()

        for task in tasks:
            task.join()

    def run(self):
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self.main())
        except KeyboardInterrupt as e:
            loop.stop()
        finally:
            loop.close()
