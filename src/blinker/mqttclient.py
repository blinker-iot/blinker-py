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


class MqttClient:
    device = None

    def __init__(self, device):
        self.device = device
        self.name = device.broker.broker
        self.client_id = device.broker.deviceName
        self.client = Client(client_id=self.client_id)
        broker_info = generate_broker_info(self.name, self.client_id, device.broker.productKey, )
        self._sub_topic = broker_info["sub_topic"]
        self._pub_topic = broker_info["pub_topic"]

        self.port = device.broker.port
        self.username = device.broker.iotId
        self.password = device.broker.iotToken

        mqtt_url = device.broker.host.split("//")
        self.protocol = mqtt_url[0]
        self.host = mqtt_url[-1]

        self.received_msg = SimpleQueue()

        self.device.mqtt_client = self

    def _on_connect(self, client, userdata, flags, rc):
        logger.info("Connect to broker from mqtt")
        if rc == 0:
            logger.success("Broker connected...")
            self.device.mqtt_connected.set()
            self.client.subscribe(self._sub_topic)
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
            self.received_msg.put_nowait(received_data)

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

    def _check_or_reconnect(self):
        if not self.client.is_connected():
            self.client.reconnect()

    def send_to_device(self, data, to_device: str = None):
        self._check_or_reconnect()
        payload = json.dumps(self._format_msg_to_device(data, to_device))
        logger.info("send mqtt message: {0}".format(payload))
        self.client.publish(self._pub_topic, payload)

    # 存储
    def _save_check(self):
        if self.name != "blinker":
            raise BlinkerBrokerException(-1, "仅可用于blinker broker")

    def send_ts_data(self, data: List):
        self._check_or_reconnect()
        payload = json.dumps(self._format_msg_to_storage(data, "ts"))
        self.client.publish(self._pub_topic, payload)
        logger.info("sended ts data")

    def send_obj_data(self, data: Dict):
        self._check_or_reconnect()
        data = json.dumps(data)
        payload = json.dumps(self._format_msg_to_storage(data, "ot"))
        logger.info("send mqtt message: {0}".format(payload))
        self.client.publish(self._pub_topic, payload)

    def send_text_data(self, data: str):
        self._check_or_reconnect()
        payload = json.dumps(self._format_msg_to_storage(data, "tt"))
        self.client.publish(self._pub_topic, payload)
