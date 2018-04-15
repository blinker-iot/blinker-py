import uuid
# import json
import socket
from BlinkerDebug import *

wsPort = 8000
BLINKER_BLE = 1
BLINKER_WIFI = 2

W_BUTTON = 1
W_SLIDER = 2
W_TOGGLE = 3

J_Xaxis = 0
J_Yaxis = 1

Yaw = 0
Pitch = 1
Roll = 2

BLINKER_CMD_ON = 'on'
BLINKER_CMD_OFF = 'off'
BLINKER_CMD_JOYSTICK = 'joy'
BLINKER_CMD_GYRO = 'gyro'
BLINKER_CMD_AHRS = 'ahrs'
BLINKER_CMD_VIBRATE = 'vibrate'
BLINKER_CMD_BUTTON_TAP = 'tap'
BLINKER_CMD_BUTTON_PRESSED = 'pressed'
BLINKER_CMD_BUTTON_RELEASED = 'released'
BLINKER_CMD_NEWLINE = '\n'
BLINKER_CMD_INTERSPACE = ' '
BLINKER_JOYSTICK_VALUE_DEFAULT = 128

# def check_json_format(raw_msg):
#     if isinstance(raw_msg, str):
#         try:
#             json.loads(raw_msg, encoding='utf-8')
#         except ValueError:
#             return False
#         return True
#     else:
#         return False

def macAddress():
    return (':'.join(['{:02X}'.format((uuid.getnode() >> ele) & 0xff)
        for ele in range(0,8*6,8)][::-1]))

def macDeviceName():
    return (''.join(['{:02X}'.format((uuid.getnode() >> ele) & 0xff)
        for ele in range(0,8*6,8)][::-1]))

def localIP():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip