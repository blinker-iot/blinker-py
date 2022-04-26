# -*- coding: utf-8 -*-

"""
"""

__author__ = 'stao'

import json
import ssl
import time
import certifi
import aiohttp
import requests

from loguru import logger
from typing import Dict, List
from .errors import BlinkerHttpException

__all__ = ["HttpClient"]

ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations(certifi.where())


class _HttpRequestConf:
    SERVER = "https://iot.diandeng.tech"
    API = {
        "DIY_AUTH": SERVER + "/api/v1/user/device/diy/auth",
        "HEARTBEAT": SERVER + "/api/v1/user/device/heartbeat",
        "SMS": SERVER + '/api/v1/user/device/sms',
        "WECHAT": SERVER + '/api/v1/user/device/wxMsg/',
        "PUSH": SERVER + '/api/v1/user/device/push',
        "SHARE": SERVER + '/api/v1/user/device/share/device',
        "STORAGE_TS": SERVER + "/api/v1/user/device/cloudStorage/",
        "STORAGE_OBJ": SERVER + "/api/v1/user/device/cloud_storage/object",
        "STORAGE_TEXT": SERVER + "/api/v1/user/device/cloud_storage/text",
        "LOG": SERVER + '/api/v1/user/device/cloud_storage/logs',
        "POSITION": SERVER + '/api/v1/user/device/cloud_storage/coordinate',
        "WEATHER": SERVER + '/api/v3/weather',
        "WEATHER_FORECAST": SERVER + '/api/v3/forecast',
        "AIR": SERVER + '/api/v3/air',
        "VOICE_ASSISTANT": SERVER + "/api/v1/user/device/voice_assistant",
    }


class HttpClient(_HttpRequestConf):
    def __init__(self):
        self.device = ""
        self.auth_key = ""
        self.auth_token = ""

    @staticmethod
    async def _async_response_handler(res: aiohttp.client.ClientResponse):
        if res.status != 200:
            raise BlinkerHttpException(-1, "Http request error, err code is {0}".format(res.status))

        try:
            if res.content_type == "text/html":
                result = json.loads(await res.text())
            else:
                result = await res.json()
        except Exception as e:
            raise BlinkerHttpException(-1, "Decode http response error, err is {0}".format(e))

        if result["message"] != 1000:
            logger.error("code: {0}, message: {1}".format(result["message"], result["detail"]))
            raise BlinkerHttpException(message=result["message"], detail=result["detail"])

        return result["detail"]

    async def _async_get(self, url: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, ssl_context=ssl_context) as response:
                return await self._async_response_handler(response)

    async def _async_post(self, url: str, **kwargs):
        async with aiohttp.ClientSession() as session:
            async with session.post(url, **kwargs, ssl_context=ssl_context) as response:
                return await self._async_response_handler(response)

    @staticmethod
    def _response_handler(res):
        if res.status_code != 200:
            raise BlinkerHttpException(-1, "Http request error, err code is {0}".format(res.status))

        try:
            result = res.json()
        except Exception as e:
            raise BlinkerHttpException(-1, "Decode http response error, err is {0}".format(e))

        if result["message"] != 1000:
            raise BlinkerHttpException(message=result["message"], detail=result["detail"])

        return result["detail"]

    def _get(self, url: str):
        res = requests.get(url)
        return self._response_handler(res)

    def _post(self, url: str, data: Dict):
        res = requests.post(url, data=data)
        return self._response_handler(res)

    async def diy_device_auth(self, auth_key, protocol="mqtt", version="", ali_type=None, duer_type=None,
                              mi_type=None):
        url = "{0}?authKey={1}&protocol={2}".format(self.API["DIY_AUTH"], auth_key, protocol)
        if version:
            url += "&version={0}".format(version)
        if ali_type:
            url += "&aliType={0}".format(ali_type)
        elif duer_type:
            url += "&duerType={0}".format(duer_type)
        elif mi_type:
            url += "&miType={0}".format(mi_type)

        res = await self._async_get(url)
        self.auth_key = auth_key
        self.auth_token = res["iotToken"]
        self.device = res["deviceName"]

        return res

    async def get_share_info(self):
        url = "{0}?deviceName={1}&key={2}".format(self.API["SHARE"], self.device, self.auth_key)
        return await self._async_get(url)

    async def cloud_heartbeat(self, heartbeat=600):
        logger.info("http cloud heartbeat")
        url = "{0}?deviceName={1}&key={2}&heartbeat={3}".format(self.API["HEARTBEAT"], self.device, self.auth_key,
                                                                heartbeat)
        return await self._async_get(url)

    async def set_position(self, lng, lat):
        url = self.API["POSITION"]
        data = {
            "token": self.auth_token,
            "data": [int(time.time()), [lng, lat]]
        }

        return await self._async_post(url, json=data)

    async def save_ts_data(self, data: Dict):
        """
        data: {"key": [[t1, v], [t2, v], ...]}
        """
        url = self.API["STORAGE_TS"]
        req_data = {
            "deviceName": self.device,
            "key": self.auth_key,
            "data": json.dumps(data)
        }

        return await self._async_post(url, data=req_data)

    async def save_log_data(self, data: List):
        """
        data: [[t1, string], [t2, string], ...]
        """

        url = self.API["LOG"]
        req_data = {
            "token": self.auth_token,
            "data": data
        }

        return await self._async_post(url, json=req_data)

    async def get_object_data(self, keyword=None):
        url = self.API["STORAGE_OBJ"] + "?deviceId=" + self.device
        if keyword:
            url += "&keyword={0}".format(keyword)

        return await self._async_get(url)

    async def get_text_data(self):
        url = self.API["STORAGE_TEXT"] + "?deviceId=" + self.device
        return await self._async_get(url)

    # 存储
    # def save_ts_data(self, data: Dict):
    #     """
    #     data: {"key": [[t1, v], [t2, v], ...]}
    #     """
    #     url = self.API["TS_STORAGE"]
    #     req_data = {
    #         "deviceName": self.device,
    #         "key": self.auth_key,
    #         "data": json.dumps(data)
    #     }
    #
    #     return self._post(url, req_data)

    # def save_log_data(self, data: List):
    #     """
    #     data: [[t1, string], [t2, string], ...]
    #     """
    #
    #     url = self.API["LOG"]
    #     req_data = {
    #         "token": self.auth_token,
    #         "data": data
    #     }
    #
    #     return self._response_handler(requests.post(url, json=req_data))

    # 天气
    async def get_weather(self, city_code):
        url = '{0}?device={1}&key={2}&code={3}'.format(self.API["WEATHER"], self.device, self.auth_token, city_code)
        return await self._async_get(url)

    async def get_forecast(self, city_code):
        url = '{0}?device={1}&key={2}&code={3}'.format(self.API["WEATHER_FORECAST"], self.device, self.auth_token,
                                                       city_code)
        return await self._async_get(url)

    async def get_air(self, city_code):
        url = '{0}?device={1}&key={2}&code={3}'.format(self.API["AIR"], self.device, self.auth_token, city_code)
        return await self._async_get(url)

    # 消息
    async def send_sms(self, data: str, phone: str = ""):
        url = self.API["SMS"]
        req_data = {
            "deviceName": self.device,
            "key": self.auth_key,
            "cel": phone,
            "msg": data
        }

        return await self._async_post(url, data=req_data)

    async def send_wx_template_msg(self, title, state, text):
        url = self.API["WECHAT"]
        req_data = {
            "deviceName": self.device,
            "key": self.auth_key,
            "title": title,
            "state": state,
            "msg": text
        }

        return await self._async_post(url, data=req_data)

    async def send_push_msg(self, msg: str, receivers: List = None):
        url = self.API["PUSH"]
        req_data = {
            "deviceName": self.device,
            "key": self.auth_key,
            "msg": msg
        }

        if receivers:
            req_data["receivers"] = receivers

        return await self._async_post(url, data=req_data)
