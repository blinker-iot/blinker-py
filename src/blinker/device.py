#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "stao"

import asyncio
import datetime
import json

import math
import os
import threading
import time
import websockets

from typing import Dict

from asyncio.coroutines import iscoroutinefunction
from apscheduler.schedulers.background import BackgroundScheduler
from getmac import get_mac_address
from zeroconf import ServiceInfo, Zeroconf
from threading import Event
from queue import SimpleQueue

from loguru import logger

from .httpclient import *
from .mqttclient import *
from .errors import *

__all__ = ["Device"]


class BuiltinSwitch:
    device = None
    key = "switch"
    state = ""

    def __init__(self, device, func=None):
        self.device = device
        self._func = func

    @property
    def func(self):
        return self._func

    @func.setter
    def func(self, func):
        self._func = func

    async def handler(self, msg):
        if self.func:
            if iscoroutinefunction(self._func):
                await self._func(msg)
            else:
                self._func(msg)
        else:
            logger.warning("Not setting callable func for {0}".format(self.key))

    def set_state(self, state):
        self.state = state
        return self

    async def update(self):
        message = {self.key: self.state}
        self.device.mqtt_client.send_to_device(message)


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

    builtinSwitch: BuiltinSwitch = None

    realtime_tasks = {}

    scheduler = BackgroundScheduler(timezone="Asia/Shanghai")
    countdown_timer = None
    countdown_timer2 = None

    auth_finished = Event()
    auth_finished.clear()
    mqtt_connected = Event()
    mqtt_connected.clear()

    # timing_tasks = TimingTasks()

    def __init__(self, auth_key, protocol: str = "mqtt", version: str = "1.0", ali_type: str = None,
                 duer_type: str = None, mi_type: str = None, websocket: bool = False, heartbeat_func=None,
                 realtime_func=None, ready_func=None, builtin_switch_func=None):
        self.auth_key = auth_key
        self.version = version
        self.protocol = protocol
        self.ali_type = ali_type
        self.duer_type = duer_type
        self.mi_type = mi_type

        self.websocket = websocket
        self.temp_data_path = ""
        self.temp_data = {}

        self._heartbeat_callable = heartbeat_func
        self._ready_callable = ready_func
        self._realtime_callable = realtime_func
        self._builtin_switch_callable = builtin_switch_func

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

    @property
    def realtime_callable(self):
        return self._realtime_callable

    @realtime_callable.setter
    def realtime_callable(self, func):
        self._ready_callable = func

    @property
    def builtin_switch_callable(self):
        return self._builtin_switch_callable

    @builtin_switch_callable.setter
    def builtin_switch_callable(self, func):
        self._builtin_switch_callable = func

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

    async def _custom_runner(self, func, **kwargs):
        self.auth_finished.wait()
        self.mqtt_connected.wait()

        if iscoroutinefunction(func):
            await func(**kwargs)
        else:
            func(**kwargs)

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

        # 初始化内置开关
        self.builtinSwitch = BuiltinSwitch(self)
        self.builtinSwitch.func = self._builtin_switch_callable
        self.add_widget(self.builtinSwitch)

        # 加载缓存数据
        self.temp_data_path = f".{self.config.deviceName}.json"
        self.temp_data = await self.load_json_file()
        await self.load_timing_task()

        self.auth_finished.set()
        logger.success("Device auth successful...")

    async def load_json_file(self):
        if os.path.exists(self.temp_data_path):
            with open(self.temp_data_path) as f:
                return json.load(f)
        else:
            return {}

    def save_json_file(self, data):
        with open(self.temp_data_path, "w") as f:
            json.dump(data, f)

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

    def del_timing_task(self, task_id):
        self.disable_timing_task(task_id)

    def disable_timing_task(self, task_id):
        self.temp_data["timing"][task_id]["ena"] = 0
        self.scheduler.remove_job(f'timing-{task_id}')

        self.save_json_file(self.temp_data)

    async def load_timing_task(self):
        if "timing" not in self.temp_data:
            return

        for task in self.temp_data["timing"]:
            if task["ena"] == 1:
                await self.add_timing_task(task)

    def _execution_timing_task(self, task_data):
        self.received_data.put(task_data["act"][0])
        if task_data["day"] == "0000000":
            self.disable_timing_task(task_data["task"])
        self.mqtt_client.send_to_device(self.get_timing_data())

    def get_timing_data(self):
        if "timing" not in self.temp_data:
            return {"timing": []}
        else:
            return {"timing": self.temp_data["timing"]}

    async def set_timing_data(self, data):
        if "timing" not in self.temp_data:
            self.temp_data["timing"] = []
            index = 0
        else:
            index = data[0]["task"]
        if index < len(self.temp_data["timing"]):
            self.temp_data["timing"][index] = data[0]
        else:
            self.temp_data["timing"].append(data[0])

        await self.add_timing_task(data[0])

    async def add_timing_task(self, task_data):
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

            self.scheduler.add_job(self._execution_timing_task, "cron", **conf, args=[task_data],
                                   id=f'timing-{task_data["task"]}')

    async def del_timing_data(self, task_id):
        self.del_timing_task(task_id)
        del self.temp_data["timing"][task_id]
        for index in range(len(self.temp_data["timing"])):
            if index >= task_id:
                self.temp_data["timing"][index]["task"] = index
            index += 1

        self.save_json_file(self.temp_data)

    def get_countdown_data(self):
        if "countdown" not in self.temp_data:
            return {"countdown": False}
        else:
            return {"countdown": self.temp_data["countdown"]}

    def _countdown_func(self):
        if "countdown" in self.temp_data and not isinstance(self.temp_data["countdown"], bool):
            self.temp_data["countdown"]["rtim"] += 1
            self.mqtt_client.send_to_device(self.get_countdown_data())

            if self.temp_data["countdown"]["rtim"] == self.temp_data["countdown"]["ttim"]:
                self.received_data.put(self.temp_data["countdown"]["act"][0])
                self.temp_data["countdown"] = False
                self.mqtt_client.send_to_device(self.get_countdown_data())

    async def clear_countdown_job(self):
        if self.countdown_timer:
            self.countdown_timer.remove()

    async def set_countdown_data(self, data):
        if data == "dlt":
            # 删除倒计时
            self.temp_data["countdown"] = False
            await self.clear_countdown_job()
        elif "run" in data and self.countdown_timer:
            if "countdown" not in self.temp_data:
                self.temp_data["countdown"] = {}
            self.temp_data["countdown"]["run"] = data["run"]
            if self.temp_data["countdown"]["run"] == 0:
                # 暂停倒计时
                self.countdown_timer.pause()
            elif self.temp_data["countdown"]["run"] == 1:
                # 重启倒计时
                self.countdown_timer.resume()
        else:
            # 设置倒计时
            self.temp_data["countdown"] = data
            self.temp_data["countdown"]["rtim"] = 0
            await self.clear_countdown_job()

            # 添加倒计时任务
            countdown_time = self.temp_data["countdown"]["ttim"]  # 分钟
            start_date = datetime.datetime.now()
            end_date = start_date + datetime.timedelta(minutes=+countdown_time)
            self.countdown_timer = self.scheduler.add_job(self._countdown_func, "interval", minutes=1,
                                                          start_date=start_date, end_date=end_date,
                                                          id="countdownjob")

    async def _receiver(self):
        self.mqtt_connected.wait()

        logger.success("Receiver ready...")
        while True:
            data = self.received_data.get()
            logger.info("received msg: {0}".format(data))

            if isinstance(data, str):
                data = json.loads(data)

            if "fromDevice" in data:
                self.target_device = data["fromDevice"]
            else:
                self.target_device = self.config.uuid

            if "data" in data:
                received_data = data["data"]
            else:
                received_data = data

            if "get" in received_data:
                if received_data["get"] == "state":
                    if self.heartbeat_callable:
                        await self._custom_runner(self.heartbeat_callable, msg=received_data)
                    self.mqtt_client.send_to_device({"state": "online"})
                elif received_data["get"] == "timing":
                    self.mqtt_client.send_to_device(self.get_timing_data())
                elif received_data["get"] == "countdown":
                    self.mqtt_client.send_to_device(self.get_countdown_data())
            elif "set" in received_data:
                if "timing" in received_data["set"]:
                    if "dlt" in received_data["set"]["timing"][0]:
                        await self.del_timing_data(received_data["set"]["timing"][0]["dlt"])
                    else:
                        await self.set_timing_data(received_data["set"]["timing"])

                    self.mqtt_client.send_to_device(self.get_timing_data())
                elif "countdown" in received_data["set"]:
                    await self.set_countdown_data(received_data["set"]["countdown"])
                    self.mqtt_client.send_to_device(self.get_countdown_data())
            elif "rt" in received_data:
                if self._realtime_callable:
                    await self._custom_runner(self._realtime_callable, keys=received_data["rt"])
            else:
                for key in received_data.keys():
                    if key in self.widgets.keys():
                        await self.widgets[key].handler(received_data)
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

    # 实时数据
    async def sendRtData(self, key: str, data_func, t: int = 1):
        if key in self.realtime_tasks:
            self.realtime_tasks[key].remove()

        def rt_func():
            message = {key: {"val": data_func(), "date": int(time.time())}}
            self.mqtt_client.send_to_device(message, to_device=self.config.uuid)

        self.realtime_tasks[key] = self.scheduler.add_job(rt_func, "interval", seconds=t)

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

        # if self.heartbeat_callable:
        #     tasks.append(threading.Thread(target=asyncio.run, args=(self._custom_runner(self.heartbeat_callable),)))

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
