#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "stao"

import json

import ssl
import certifi

from typing import Dict
from loguru import logger
from collections import deque

from paho.mqtt.client import Client

from .errors import BlinkerBrokerException

__all__ = ["Broker"]

ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations(certifi.where())


def generate_broker_info(broker, client_id, product_key="") -> Dict:
    if broker == "aliyun":
        info = {
            "sub_topic": f"/{product_key}/{client_id}/r",
            "pub_topic": f"/{product_key}/{client_id}/s",
            "exasub_topic": f"/sys/{product_key}/{client_id}/rrpc/request/+",
            "exapub_topic": f"/sys/{product_key}/{client_id}/rrpc/response/"
        }
    elif broker == "blinker":
        info = {
            "sub_topic": f"/device/{client_id}/r",
            "pub_topic": f"/device/{client_id}/s"
        }
    else:
        raise BlinkerBrokerException(message=102, detail="Not support broker")

    return info


class Broker:
    def __init__(self, broker: str, client_id: str, product_key: str = "", host: str = "", port: int = "",
                 username: str = "", password: str = ""):
        self.clientId = client_id
        self.client = Client(client_id=client_id)
        broker_info = generate_broker_info(broker, client_id, product_key)
        self._sub_topic = broker_info["sub_topic"]
        self._pub_topic = broker_info["pub_topic"]

        self.port = port
        self.username = username
        self.password = password

        mqtt_url = host.split("//")
        self.protocol = mqtt_url[0]
        self.host = mqtt_url[-1]

        self.received_msg = deque()

    def _on_connect(self, client, userdata, flags, rc):
        logger.info("Connect to broker from mqtt")
        if rc == 0:
            logger.success("Broker connected...")
            self.client.subscribe(self._sub_topic)
        else:
            logger.error("Connect to broker error, code is {0}".format(rc))

    def _on_message(self, client, userdata, msg):
        received_msg = msg.payload.decode("utf8")
        self.received_msg.append(received_msg)  # str

    def connection(self):
        self.client.username_pw_set(self.username, self.password)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

        if self.protocol == "mqtts:":
            self.client.tls_set_context(context=ssl_context)
        self.client.connect_async(self.host, int(self.port))
        self.client.loop_start()

    def pub(self, data, to_device):
        if not self.client.is_connected():
            self.client.reconnect()
        payload = json.dumps({"fromDevice": self.clientId, "toDevice": to_device, "data": data})
        logger.info("send mqtt message: {0}".format(payload))
        self.client.publish(self._pub_topic, payload)
