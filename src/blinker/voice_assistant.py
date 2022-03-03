# -*- coding: utf-8 -*-

"""
"""

__author__ = 'stao'

from asyncio.coroutines import iscoroutinefunction
from queue import SimpleQueue
from loguru import logger
from typing import Dict, Union, List


class VAType:
    LIGHT = "light"
    OUTLET = "outlet"
    MULTI_OUTLET = "multi_outlet"
    SENSOR = "sensor"
    FAN = "fan"
    AIRCONDITION = "aircondition"


class MiLightMode:
    DAY = "day"
    NIGHT = "night"
    COLOR = "color"
    WARMTH = "warmth"
    TV = "tv"
    READING = "reading"
    COMPUTER = "computer"


class AliLightMode:
    READING = "reading"
    MOVIE = 'movie'
    SLEEP = 'sleep'
    LIVE = 'live'
    HOLIDAY = 'holiday'
    MUSIC = 'music'
    COMMON = 'common'
    NIGHT = 'night'


class DuerLightMode:
    READING = 'READING'
    SLEEP = 'SLEEP'
    ALARM = 'ALARM'
    NIGHT_LIGHT = 'NIGHT_LIGHT'
    ROMANTIC = 'ROMANTIC'
    SUNDOWN = 'SUNDOWN'
    SUNRISE = 'SUNRISE'
    RELAX = 'RELAX'
    LIGHTING = 'LIGHTING'
    SUN = 'SUN'
    STAR = 'STAR'
    ENERGY_SAVING = 'ENERGY_SAVING'
    MOON = 'MOON'
    JUDI = 'JUDI'


class VAMessage(object):
    voice_assistant = None

    def __init__(self, voice_assistant, data: Dict = None):
        self.voice_assistant = voice_assistant
        self.data = data
        self.push_data = {}

    def send(self):
        raise NotImplemented

    async def update(self):
        await self.voice_assistant.push_msg(self.push_data)


class PowerMessage(VAMessage):
    async def power(self, state):
        self.push_data["pState"] = state
        return self

    async def num(self, num: Union[int, float]):
        self.push_data["num"] = num
        return self


class ModeMessage(VAMessage):
    async def mode(self, state: Union[str, int, float]):
        self.push_data["mode"] = state
        return self


class ColorMessage(VAMessage):
    async def color(self, color: Union[str, int, float]):
        self.push_data["clr"] = color
        return self


class ColorTempMessage(VAMessage):
    async def colorTemp(self, val: Union[int, float]):
        self.push_data["colTemp"] = val
        return self


class BrightnessMessage(VAMessage):
    async def brightness(self, val: Union[int, float, str]):
        self.push_data["bright"] = val
        return self


class DataMessage(VAMessage):
    async def temp(self, val: Union[int, float, str]):
        self.push_data["temp"] = str(val)
        return self

    async def humi(self, val: Union[int, float, str]):
        self.push_data["humi"] = str(val)
        return self

    async def aqi(self, val: Union[int, float, str]):
        self.push_data["aqi"] = str(val)
        return self

    async def pm25(self, val: Union[int, float, str]):
        self.push_data["pm25"] = str(val)
        return self

    async def pm10(self, val: Union[int, float, str]):
        self.push_data["pm10"] = str(val)
        return self

    async def co2(self, val: Union[int, float, str]):
        self.push_data["co2"] = str(val)
        return self

    async def brightness(self, val: Union[int, float, str]):
        self.push_data["brightness"] = str(val)
        return self

    async def color(self, val: Union[int, float, str, List[int]]):
        self.push_data["color"] = val
        return self

    async def colorTemp(self, val: Union[int, float, str]):
        self.push_data["colorTemp"] = str(val)
        return self

    async def mode(self, state: Union[int, float, str]):
        self.push_data["mode"] = state
        return self

    async def power(self, state: str):
        if self.voice_assistant.va_name == "MIOT":
            if state == "on":
                state = "true"
            else:
                state = "false"

        self.push_data["pState"] = state
        return self


class VoiceAssistant(object):
    device = None
    va_received_data = SimpleQueue()

    def __init__(self, va_type, power_change=None, mode_change=None, color_change=None, colortemp_change=None,
                 brightness_change=None, state_query=None):
        self.va_type = va_type

        self.va_name = ""
        self.message_id = ""

        self._power_change_callable = power_change
        self._mode_change_callable = mode_change
        self._color_change_callable = color_change
        self._colortemp_change_callable = colortemp_change
        self._brightness_change_callable = brightness_change
        self._state_query_callable = state_query

    @property
    def power_change_callable(self):
        return self._power_change_callable

    @power_change_callable.setter
    def power_change_callable(self, func):
        self._power_change_callable = func

    @property
    def mode_change_callable(self):
        return self._mode_change_callable

    @mode_change_callable.setter
    def mode_change_callable(self, func):
        self._mode_change_callable = func

    @property
    def color_change_callable(self):
        return self._color_change_callable

    @color_change_callable.setter
    def color_change_callable(self, func):
        self._color_change_callable = func

    @property
    def colortemp_change_callable(self):
        return self._colortemp_change_callable

    @colortemp_change_callable.setter
    def colortemp_change_callable(self, func):
        self._colortemp_change_callable = func

    @property
    def brightness_change_callable(self):
        return self._brightness_change_callable

    @brightness_change_callable.setter
    def brightness_change_callable(self, func):
        self._brightness_change_callable = func

    @property
    def state_query_callable(self):
        return self._state_query_callable

    @state_query_callable.setter
    def state_query_callable(self, func):
        self._state_query_callable = func

    @staticmethod
    async def custom_run(func, data):
        if iscoroutinefunction(func):
            await func(data)
        else:
            func(data)

    async def push_msg(self, data: Dict):
        data["messageId"] = self.message_id
        self.device.mqtt_client.send_to_voiceassistant(data)

    async def listen(self):
        while True:
            received_msg = self.va_received_data.get()
            # self.target_device = received_msg["fromDevice"]
            self.va_name = received_msg["data"]["from"]
            self.message_id = received_msg["data"]["messageId"]

            await self.process_data(received_msg["data"])

    async def process_data(self, data):
        if "get" in data:
            await self.custom_run(self.state_query_callable, DataMessage(self, data["get"]))
        elif "set" in data:
            set_ops = data["set"]
            if "pState" in set_ops:
                await self.custom_run(self.power_change_callable, PowerMessage(self, set_ops))
            elif "col" in set_ops:
                await self.custom_run(self.color_change_callable, ColorMessage(self, set_ops))
            elif "colTemp" in set_ops:
                await self.custom_run(self.colortemp_change_callable, ColorTempMessage(self, set_ops))
            elif "mode" in set_ops:
                await self.custom_run(self.mode_change_callable, ModeMessage(self, set_ops))
            elif "bright" in set_ops or "downBright" in set_ops or "upBright" in set_ops:
                await self.custom_run(self.brightness_change_callable, BrightnessMessage(self, set_ops))
            else:
                logger.warning("Not support set operate: {0}".format(set_ops))
        else:
            logger.warning("Not support voice assistant ops: {0}".format(data))
