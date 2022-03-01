# -*- coding: utf-8 -*-

"""
"""

__author__ = 'stao'

from blinker import Device


async def ready_func():
    print(await device.getWeather())
    print(await device.getAir())
    print(await device.getWeatherForecast(510100))


device = Device("authKey")
device.ready_callable = ready_func

if __name__ == '__main__':
    device.run()
