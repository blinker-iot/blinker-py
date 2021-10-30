#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "stao"

import asyncio
import json

from loguru import logger

from ._http import *
from .broker import *

__all__ = ["Device"]


class BaseDevice(object):
    def __init__(self, authkey: str, *, version: str = "1.0", protocol: str = "mqtt", ali_type: str = None,
                 duer_type: str = None, mi_type: str = None):
        self.authKey = authkey
        self.version = version
        self.protocol = protocol
        self.aliType = ali_type
        self.duerType = duer_type
        self.miType = mi_type

        self.device = None
        self.broker = None

        self.push_broker_msg = None
        self.target_device = ""

        self.widgets = {}  # {key: widget}

    def add_widget(self, widget):
        widget.device = self
        self.widgets[widget.key] = widget
        return widget

    async def handle_widget_data(self, key, data):
        return self.widgets[key].func(data)

    async def init_actions(self):
        self.device = await device_auth(self.authKey, self.version, self.protocol, self.aliType, self.duerType,
                                        self.miType)

        logger.success("device auth ok...")

    async def waiting_auth_device(self):
        while True:
            if self.device:
                break
            logger.info("waiting auth device...")
            await asyncio.sleep(2)

    async def waiting_broker_connected(self):
        while True:
            if self.broker:
                break
            logger.info("waiting broker connected...")
            await asyncio.sleep(2)

    async def init_broker(self):
        await self.waiting_auth_device()
        self.broker = Broker(self.device["broker"], self.device["deviceName"], self.device["productKey"],
                             self.device["host"], self.device["port"], self.device["iotId"], self.device["iotToken"])
        self.push_broker_msg = self.broker.pub
        self.broker.connection()

    async def heartbeat(self):
        await self.waiting_auth_device()
        # http heartbeat
        while True:
            await send_heartbeat(self.device["deviceName"], self.authKey)
            logger.info("Send heartbeat")
            await asyncio.sleep(600)

    def push_msg(self, data, target=None):
        if not target:
            target = self.target_device
        self.push_broker_msg(data, target)

    async def handle_data(self):
        await self.waiting_broker_connected()
        while True:
            if not self.broker.received_msg:
                await asyncio.sleep(10)
                continue
            received_msg = json.loads(self.broker.received_msg.pop())
            logger.info("received msg: {0}".format(received_msg))

            self.target_device = received_msg["fromDevice"]
            received_data = received_msg["data"]

            if isinstance(received_data, (str, int)):
                logger.info("not json data: {0}".format(received_data))
                return

            if "get" in received_data:
                if received_data["get"] == "state":
                    self.push_msg({"state": "online"})
            elif "set" in received_data:
                pass
            else:
                for key in received_data.keys():
                    if key in self.widgets.keys():
                        widget = self.widgets[key]
                        widget.change.on_next({"fromDevice": self.target_device, "data": received_data[key]})

    def task(self):
        asyncio.ensure_future(self.init_actions())
        asyncio.ensure_future(self.heartbeat())
        asyncio.ensure_future(self.init_broker())
        asyncio.ensure_future(self.handle_data())

    def run(self):
        self.task()
        loop = asyncio.get_event_loop()
        try:
            loop.run_forever()
        except KeyboardInterrupt as e:
            loop.stop()
        finally:
            loop.close()


class Device(BaseDevice):
    def __init__(self, authkey: str, version: str = "1.0", protocol: str = "mqtt", ali_type: str = None,
                 duer_type: str = None, mi_type: str = None):
        super(Device, self).__init__(authkey=authkey, version=version, protocol=protocol, ali_type=ali_type,
                                     duer_type=duer_type, mi_type=mi_type)
