# -*- coding: utf-8 -*-

"""
"""

__author__ = 'stao'

from blinker import Device


async def builtin_switch_func(msg):
    print("builtinSwitch: {0}".format(msg))
    if msg["switch"] == "on":
        await device.builtinSwitch.set_state("on").update()
    else:
        await device.builtinSwitch.set_state("off").update()


device = Device("authKey", builtin_switch_func=builtin_switch_func)

if __name__ == '__main__':
    device.run()
