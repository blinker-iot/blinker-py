#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "stao"

import asyncio
import threading
import time

from threading import Event
from queue import SimpleQueue

from loguru import logger

from .httpclient import *
from .mqttclient import *
from .cache import *
from .errors import *

__all__ = ["Device", "Storage", "Notice"]


class DeviceBrokerInfo(object):
    def __init__(self, /, **kw):
        self.__dict__.update(kw)


class Notice(object):
    device = None

    def __init__(self, device):
        self.device = device

    def sms(self, data: str):
        self.device.http_client.send_sms(data[:20])

    def wechat(self, title: str, state: str, text: str):
        self.device.http_client.send_wx_template_msg(title, state, text)

    def push(self, data: str):
        self.device.http_client.send_push_msg(data)


class Storage(object):
    device = None

    def __init__(self, device):
        self.device = device

    def save_ts(self, data: Dict):
        req_data = {}
        for key, value in data.items():
            if not isinstance(value, (int, float)):
                return BlinkerException(-1, "Value error")

            req_data[key] = [[int(time.time()), value]]
        self.device.http_client.save_ts_data(req_data)

        time.sleep(60)

    def save_obj(self, data: Dict):
        self.device.mqtt_client.send_obj_data(data)
        time.sleep(60)

    def save_text(self, data: str):
        self.device.mqtt_client.send_text_data(data)
        time.sleep(60)

    def save_log(self, data: str):
        req_data = [[int(time.time()), data]]
        self.device.http_client.save_log_data(req_data)
        time.sleep(60)


class Device(object):
    """
    :param auth_key
    :param version
    :param protocol
    :param ali_type
    :param duer_type
    :param mi_type
    :param heartbeat_callable
    :param init_ready_func
    """

    mqtt_client = None
    http_client = None
    broker = None
    widgets = {}
    target_device = None
    shared_user_list = []
    cache_data = None
    data_reader = SimpleQueue()

    auth_finished = Event()
    auth_finished.clear()
    mqtt_connected = Event()
    mqtt_connected.clear()

    # timing_tasks = TimingTasks()

    def __init__(self, auth_key, protocol, version: str = "1.0", ali_type: str = None, duer_type: str = None,
                 mi_type: str = None, heartbeat_func=None, init_ready_func=None, data_read_func=None):
        self.auth_key = auth_key
        self.version = version
        self.protocol = protocol
        self.ali_type = ali_type
        self.duer_type = duer_type
        self.mi_type = mi_type

        self._heartbeat_callable = heartbeat_func
        self._init_ready_callable = init_ready_func
        self._data_read_callable = data_read_func

    @property
    def heartbeat_callable(self):
        return self._heartbeat_callable

    @heartbeat_callable.setter
    def heartbeat_callable(self, func):
        self._heartbeat_callable = func

    @property
    def init_ready_callable(self):
        return self._init_ready_callable

    @init_ready_callable.setter
    def init_ready_callable(self, func):
        self._init_ready_callable = func

    @property
    def data_read_callable(self):
        return self._data_read_callable

    @data_read_callable.setter
    def data_read_callable(self, func):
        self._data_read_callable = func

    async def _custom_runner(self, func):
        self.auth_finished.wait()
        self.mqtt_connected.wait()

        func()

    def add_widget(self, widget):
        widget.device = self
        self.widgets[widget.key] = widget
        return widget

    async def device_init(self):
        self.http_client = HttpClient()
        broker_info = await self.http_client.diy_device_auth(
            self.auth_key,
            self.protocol,
            self.version,
            self.ali_type,
            self.duer_type,
            self.mi_type
        )

        self.broker = DeviceBrokerInfo(**broker_info)

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

    def set_position(self, lng, lat):
        self.http_client.set_position(lng, lat)

    def vibrate(self, t=500):
        self.mqtt_client.send_to_device({"vibrate": t})

    async def _receiver(self):
        self.mqtt_connected.wait()
        logger.success("Receiver ready...")
        while True:
            received_msg = self.mqtt_client.received_msg.get()
            logger.info("received msg: {0}".format(received_msg))

            self.target_device = received_msg["fromDevice"]
            received_data = received_msg["data"]

            if "get" in received_data:
                if received_data["get"] == "state":
                    if self.heartbeat_callable:
                        self.heartbeat_callable()
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
                        await self.widgets[key].handler(received_msg)
                    else:
                        self.data_reader.put({"fromDevice": self.target_device, "data": {key: received_data[key]}})

            await asyncio.sleep(0)

    async def main(self):
        tasks = [
            threading.Thread(target=asyncio.run, args=(self.device_init(),)),
            threading.Thread(target=asyncio.run, args=(self.mqttclient_init(),)),
            threading.Thread(target=asyncio.run, args=(self._cloud_heartbeat(),)),
            threading.Thread(target=asyncio.run, args=(self._receiver(),))
        ]

        if self.heartbeat_callable:
            tasks.append(threading.Thread(target=asyncio.run, args=(self._custom_runner(self.heartbeat_callable),)))

        if self.init_ready_callable:
            tasks.append(threading.Thread(target=asyncio.run, args=(self._custom_runner(self.init_ready_callable),)))

        if self.data_read_callable:
            tasks.append(threading.Thread(target=asyncio.run, args=(self._custom_runner(self.data_read_callable),)))

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
