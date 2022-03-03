#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "stao"

import json
import ssl
import certifi

from typing import Dict, Any, List
from loguru import logger
from queue import SimpleQueue
from paho.mqtt.client import Client
from .errors import BlinkerBrokerException

__all__ = ["MqttClient"]

ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations(certifi.where())


class MqttClient:
    device = None

    def __init__(self, device):
        self.device = device
        self.name = device.config.broker
        self.client_id = device.config.deviceName
        self.client = Client(client_id=self.client_id)
        self._sub_topic = f"/device/{self.client_id}/r"
        self._pub_topic = f"/device/{self.client_id}/s"
        self._exasub_topic = f"/device/ServerSender/r"
        self._exapub_topic = f"/device/ServerReceiver/s"

        self.port = device.config.port
        self.username = device.config.iotId
        self.password = device.config.iotToken

        mqtt_url = device.config.host.split("//")
        self.protocol = mqtt_url[0]
        self.host = mqtt_url[-1]

        self.device.mqtt_client = self

    def _on_connect(self, client, userdata, flags, rc):
        logger.info("Connect to broker from mqtt")
        if rc == 0:
            logger.success("Broker connected...")
            self.device.mqtt_connected.set()
            self.client.subscribe([(self._sub_topic, 0), (self._exasub_topic, 0)])
        else:
            logger.error("Connect to broker error, code is {0}".format(rc))

    def _on_message(self, client, userdata, msg):
        received_msg = msg.payload.decode("utf8")
        logger.info("received msg: {0}".format(received_msg))

        if isinstance(received_msg, str):
            try:
                received_data = json.loads(received_msg)
            except json.decoder.JSONDecodeError:
                received_data = None
                logger.error("mqtt received msg isn't json")
        else:
            received_data = received_msg

        if received_data:
            if received_data["fromDevice"] == "ServerSender":
                self.device.voice_assistant.va_received_data.put(received_data)
            else:
                self.device.received_data.put(received_data)

    async def connection(self):
        self.client.username_pw_set(self.username, self.password)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

        if self.protocol == "mqtts:":
            self.client.tls_set_context(context=ssl_context)
        self.client.connect_async(self.host, int(self.port))
        self.client.loop_start()

    def _get_target_device(self, to_device: str = None):
        return to_device if to_device else self.device.target_device

    def _format_msg_to_device(self, data: Any, to_device: str = "") -> Dict:
        return {"deviceType": "OwnApp", "fromDevice": self.client_id, "toDevice": self._get_target_device(to_device),
                "data": data}

    def _format_msg_to_group(self, data: Any, to_group: str) -> Dict:
        return {"fromDevice": self.client_id, "toGroup": to_group, "data": data}

    def _format_msg_to_storage(self, data: Any, storage_type: str) -> Dict:
        return {"fromDevice": self.client_id, "toStorage": storage_type, "data": data}

    def _format_msg_to_voiceassistant(self, data: Any) -> Dict:
        return {"fromDevice": self.client_id, "toDevice": "ServerReceiver", "data": data}

    def _check_or_reconnect(self):
        if not self.client.is_connected():
            self.client.reconnect()

    def send_to_device(self, data, to_device: str = None):
        self._check_or_reconnect()
        payload = json.dumps(self._format_msg_to_device(data, to_device))
        logger.info("send mqtt message: {0}".format(payload))
        self.client.publish(self._pub_topic, payload)

    def send_to_voiceassistant(self, data):
        self._check_or_reconnect()
        payload = json.dumps(self._format_msg_to_voiceassistant(data))
        logger.info("send mqtt message to voice assistant: {0}".format(payload))
        self.client.publish(self._exapub_topic, payload)

    # 存储
    def _save_check(self):
        if self.name != "blinker":
            raise BlinkerBrokerException(-1, "仅可用于blinker broker")

    def send_ts_data(self, data: List):
        self._check_or_reconnect()
        payload = json.dumps(self._format_msg_to_storage(data, "ts"))
        payload = payload.replace(" ", "")
        self.client.publish(self._pub_topic, payload)
        logger.info("sended ts data")

    def send_obj_data(self, data: Dict):
        self._check_or_reconnect()
        # data = json.dumps(data)
        payload = json.dumps(self._format_msg_to_storage(data, "ot"))
        payload = payload.replace(" ", "")
        logger.info("mqtt message topic: {0}".format(self._pub_topic))
        logger.info("mqtt message payload: {0}".format(payload))
        self.client.publish(self._pub_topic, payload)

    def send_text_data(self, data: str):
        self._check_or_reconnect()
        payload = json.dumps(self._format_msg_to_storage(data, "tt"))
        payload = payload.replace(" ", "")
        self.client.publish(self._pub_topic, payload)
