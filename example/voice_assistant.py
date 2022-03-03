# -*- coding: utf-8 -*-

"""
"""

__author__ = 'stao'

from blinker import Device
from blinker.voice_assistant import VoiceAssistant, VAType, AliLightMode, PowerMessage, ModeMessage, ColorMessage, \
    ColorTempMessage, BrightnessMessage, DataMessage


async def power_change(message: PowerMessage):
    """ 电源状态改变(适用于灯和插座)
    """

    set_state = message.data["pState"]
    print("change power state to : {0}".format(set_state))

    if set_state == "on":
        pass
    elif set_state == "off":
        pass

    await (await message.power(set_state)).update()


async def mode_change(message: ModeMessage):
    """ 模式改变(适用于灯和插座)
    """

    mode = message.data["mode"]
    print("change mode to {0}".format(mode))

    if mode == AliLightMode.READING:
        pass
    elif mode == AliLightMode.MOVIE:
        pass
    elif mode == AliLightMode.SLEEP:
        pass
    elif mode == AliLightMode.HOLIDAY:
        pass
    elif mode == AliLightMode.MUSIC:
        pass
    elif mode == AliLightMode.COMMON:
        pass

    await (await message.mode(mode)).update()


async def color_change(message: ColorMessage):
    """ 颜色改变(适用于灯)
    支持的颜色：Red红色\Yellow黄色\Blue蓝色\Green绿色\White白色\Black黑色\Cyan青色\Purple紫色\Orange橙色
    """

    color = message.data["col"]
    print("change color to {0}".format(color))
    await (await message.color(color)).update()


async def colorTemp_change(message: ColorTempMessage):
    """色温改变(适用于灯)
    """

    color_temp = message.data["colTemp"]
    print("change color temp to {0}".format(color_temp))
    await (await message.colorTemp(100)).update()


async def brightness_change(message: BrightnessMessage):
    """ 亮度改变(适用于灯)
    """

    if "bright" in message.data:
        brightness = int(message.data["bright"])
    elif "upBright" in message.data:
        brightness = int(message.data["upBright"])
    elif "downBright" in message.data:
        brightness = int(message.data["downBright"])
    else:
        brightness = 50

    print("change brightness to {0}".format(brightness))
    await (await message.brightness(brightness)).update()


async def state_query(message: DataMessage):
    print("query state: {0}".format(message.data))
    await message.power("on")
    await message.mode(AliLightMode.HOLIDAY)
    await message.color("red")
    await message.brightness(66)
    await message.update()


device = Device("authKey", ali_type=VAType.LIGHT)
voice_assistant = VoiceAssistant(VAType.LIGHT)
voice_assistant.mode_change_callable = mode_change
voice_assistant.colortemp_change_callable = colorTemp_change
voice_assistant.color_change_callable = color_change
voice_assistant.brightness_change_callable = brightness_change
voice_assistant.state_query_callable = state_query
voice_assistant.power_change_callable = power_change

device.addVoiceAssistant(voice_assistant)

if __name__ == '__main__':
    device.run()
