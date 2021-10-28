#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "stao"

import demjson

from typing import Dict
from loguru import logger
from collections import deque

from paho.mqtt.client import Client

from errors import BlinkerBrokerException

__all__ = ["Broker"]


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
            logger.info("Connected")
            self.client.subscribe(self._sub_topic)
            logger.info("Subscribe mqtt success")
        else:
            logger.info("Connect to broker error, code is {0}".format(rc))

    def _on_message(self, client, userdata, msg):
        logger.info("Received message:")
        logger.info('Subscribe topic: {0}'.format(msg.topic))
        logger.info('payload: {0}'.format(msg.payload))

        get_topic = msg.topic[0:55]
        message_id = msg.topic[55:]

        logger.info('Get topic: {0}'.format(get_topic))
        logger.info('message_id: {0}'.format(message_id))

        data = msg.payload
        # if get_topic != self.bmqtt.exatopic:
        data = data.decode('utf-8')
        data = demjson.decode(data)
        from_device = data['fromDevice']
        data = data['data']
        # data = json.dumps(data)

        logger.info('data: {0}'.format(data))

        forward_msg = {"fromDevice": from_device, "msg": data}

        self.received_msg.append(forward_msg)

    def connection(self):
        logger.info("Host: {0}".format(self.host))
        logger.info("Port: {0}".format(self.port))

        self.client.username_pw_set(self.username, self.password)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

        if self.protocol == "mqtts:":
            self.client.tls_set()
        self.client.connect_async(self.host, int(self.port))

    def run(self):
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()

    def pub(self, payload):
        logger.info(self.client.is_connected())
        logger.info("Mqtt push msg: {0}".format(payload))
        if not self.client.is_connected():
            self.connection()
        res = self.client.publish(self._pub_topic, payload)
        logger.info("Mqtt pushed result: {0}".format(res.is_published()))
