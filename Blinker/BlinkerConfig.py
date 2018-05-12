# import uuid
# import json
# import time
# import socket
# from Blinker.BlinkerDebug import *

# os_time_start = time.time()

wsPort = 81
BLINKER_BLE = 1
BLINKER_WIFI = 2

W_BUTTON = 1
W_SLIDER = 2
W_TOGGLE = 3
W_RGB = 4

J_Xaxis = 0
J_Yaxis = 1

Yaw = 0
Pitch = 1
Roll = 2
AHRS_state = 3

LONG = 0
LAT = 1

R = 0
G = 1
B = 2

CONNECTING = 0
CONNECTED = 1
DISCONNECTED = 2

BLINKER_VERSION                 = '0.1.0'

BLINKER_MAX_READ_SIZE           = 256
BLINKER_MAX_SEND_SIZE           = 128

BLINKER_CONNECT_TIMEOUT_MS      = 10000
BLINKER_STREAM_TIMEOUT          = 100
BLINKER_CMD_ON                  = 'on'
BLINKER_CMD_OFF                 = 'off'
BLINKER_CMD_JOYSTICK            = 'joy'
BLINKER_CMD_GYRO                = 'gyro'
BLINKER_CMD_AHRS                = 'ahrs'
BLINKER_CMD_GPS                 = 'gps'
BLINKER_CMD_VIBRATE             = 'vibrate'
BLINKER_CMD_BUTTON_TAP          = 'tap'
BLINKER_CMD_BUTTON_PRESSED      = 'press'
BLINKER_CMD_BUTTON_RELEASED     = 'pressup'
BLINKER_CMD_NEWLINE             = '\n'
BLINKER_CMD_INTERSPACE          = ' '
BLINKER_CMD_GET                 = 'get'
BLINKER_CMD_STATE               = 'state'
BLINKER_CMD_ONLINE              = 'online'
BLINKER_CMD_CONNECTED           = 'connected'
BLINKER_CMD_VERSION             = 'version'
BLINKER_CMD_NOTICE              = 'notice'
BLINKER_JOYSTICK_VALUE_DEFAULT  = 128

# def check_json_format(raw_msg):
#     if isinstance(raw_msg, str):
#         try:
#             json.loads(raw_msg, encoding='utf-8')
#         except ValueError:
#             return False
#         return True
#     else:
#         return False

# def millis():
#     ms = (time.time() - os_time_start) * 1000
#     return int(ms)

# def now():
#     return time.strftime("%H:%M:%S %Y", time.localtime())

# def macAddress():
#     return (':'.join(['{:02X}'.format((uuid.getnode() >> ele) & 0xff)
#         for ele in range(0,8*6,8)][::-1]))

# def macDeviceName():
#     return (''.join(['{:02X}'.format((uuid.getnode() >> ele) & 0xff)
#         for ele in range(0,8*6,8)][::-1]))

# def localIP():
#     try:
#         s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         s.connect(('8.8.8.8', 80))
#         ip = s.getsockname()[0]
#     finally:
#         s.close()

#     return ip
