# -*- coding: utf-8 -*-

"""
"""

__author__ = 'stao'

from asyncio.coroutines import iscoroutinefunction
from loguru import logger

__all__ = ["ButtonWidget", "TextWidget", "NumberWidget", "RangeWidget", "RGBWidget", "JoystickWidget",
           "ImageWidget", "VideoWidget", "ChartWidget"]


class _Widget:
    device = None

    def __init__(self, key: str, func=None):
        self.key = key
        self.state = {}

        self._device = None
        self.targetDevice = ""

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

    # def listen(self):
    #     self._change.subscribe(lambda msg: self._sub_change_func(msg))
    #     return self.change

    def _sub_change_func(self, msg):
        # self.device.target_device = msg["fromDevice"]
        # return self.change.on_next(msg["data"])
        try:
            self._func(msg)
        except TypeError:
            logger.error("Widget {0} not set callback func".format(self.key))


class ButtonWidget(_Widget):
    def turn(self, swi):
        self.state['swi'] = swi
        return self

    def text(self, text):
        self.state["tex"] = text
        return self

    def icon(self, icon):
        self.state["ico"] = icon
        return self

    def color(self, color):
        self.state["clr"] = color
        return self


class TextWidget(_Widget):
    def text(self, text):
        self.state["tex"] = text
        return self

    def text1(self, text):
        self.state["tex1"] = text
        return self

    def icon(self, icon):
        self.state["ico"] = icon
        return self

    def color(self, color):
        self.state["clr"] = color
        return self


class NumberWidget(_Widget):
    def text(self, text):
        self.state["tex"] = text
        return self

    def value(self, value):
        self.state["val"] = value
        return self

    def unit(self, unit):
        self.state["uni"] = unit
        return self

    def icon(self, icon):
        self.state["ico"] = icon
        return self

    def color(self, color):
        self.state["clr"] = color
        return self

    def max(self, num):
        self.state["max"] = num
        return self


class RangeWidget(_Widget):
    def text(self, text):
        self.state["tex"] = text
        return self

    def value(self, value):
        self.state["val"] = value
        return self

    def unit(self, unit):
        self.state["uni"] = unit
        return self

    def icon(self, icon):
        self.state["ico"] = icon
        return self

    def color(self, color):
        self.state["clr"] = color
        return self

    def max(self, num):
        self.state["max"] = num
        return self


class RGBWidget(_Widget):
    def text(self, text):
        self.state["tex"] = text
        return self

    def color(self, color):
        if type(color) == str and color[0] != "#":
            self.state = self.to_rgb(color)
        elif len(color) in (3, 4):
            self.state = color
        return self

    def brightness(self, brightness):
        self.state[3] = brightness
        return self

    @staticmethod
    def to_rgb(color_hex):
        r = str(int(color_hex[1:3], 16))
        g = str(int(color_hex[3:5], 16))
        b = str(int(color_hex[5:7], 16))
        return [r, g, b]


class JoystickWidget(_Widget):
    pass


class ImageWidget(_Widget):
    def show(self, img):
        self.state["img"] = img
        return self


class VideoWidget(_Widget):
    def url(self, addr: str):
        self.state["url"] = addr
        return self

    def autoplay(self, swi: bool):
        self.state["auto"] = swi
        return self


class ChartWidget(_Widget):
    pass
