# -*- coding: utf-8 -*-

"""
"""

__author__ = 'stao'

import aiohttp
import json
import ssl
import certifi

from errors import BlinkerHttpException

__all__ = ["device_auth", "send_heartbeat"]

SERVER = "https://iot.diandeng.tech"
DEVICE_AUTH = SERVER + "/api/v1/user/device/diy/auth"
HEARTBEAT = SERVER + "/api/v1/user/device/heartbeat"

ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations(certifi.where())


async def _get(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl_context=ssl_context) as response:
            if response.status != 200:
                raise RuntimeError(f"http request error, http code is {response.status}")
            if response.content_type == "text/html":
                return json.loads(await response.text())
            else:
                return await response.json()


async def _post(url: str, data: json):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            if response.status != 200:
                raise RuntimeError(f"http request error, http code is {response.status}")
            return await response.json()


async def _request_handle(result: json) -> dict:
    if result["message"] != 1000:
        raise BlinkerHttpException(message=result["message"], detail=result["detail"])

    return result["detail"]


async def device_auth(auth_key: str, version: str = "1.0", protocol: str = "mqtts", ali_type: str = None,
                      duer_type: str = None, mi_type: str = None):
    url = f"{DEVICE_AUTH}?authKey={auth_key}&version={version}&protocol={protocol}"
    if ali_type:
        url += f"&aliType={ali_type}"
    if duer_type:
        url += f"&duerType={duer_type}"
    if mi_type:
        url += f"&miType={mi_type}"

    return await _request_handle(await _get(url))


async def send_heartbeat(devicename: str, key: str, heartbeat: int = 600):
    # logger.info("Start heartbeat to cloud")
    url = f"{HEARTBEAT}?deviceName={devicename}&key={key}&heartbeat={heartbeat}"
    await _request_handle(await _get(url))
