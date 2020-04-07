#!/usr/bin/env python
# -*- coding: utf-8 -*-

wsPort                          = 81

BLINKER_BLE                     = 0
BLINKER_WIFI                    = 1
BLINKER_MQTT                    = 2

W_BUTTON                        = 0
W_SLIDER                        = 1
W_TOGGLE                        = 2
W_RGB                           = 3

J_Xaxis                         = 0
J_Yaxis                         = 1

Yaw                             = 0
Pitch                           = 1
Roll                            = 2
AHRS_state                      = 3

LONG                            = 0
LAT                             = 1

R                               = 0
G                               = 1
B                               = 2
BR                              = 3

CONNECTING                      = 0
CONNECTED                       = 1
DISCONNECTED                    = 2

BLINKER_DEBUG                   = 0
BLINKER_DEBUG_ALL               = 1

BLINKER_VERSION                 = '0.1.0'

BLINKER_MAX_READ_SIZE           = 256
BLINKER_MAX_SEND_SIZE           = 128

BLINKER_DIY_WIFI                = 'blinker'
BLINKER_DIY_MQTT                = 'blinker'

BLINKER_CONNECT_TIMEOUT_MS      = 10000
BLINKER_STREAM_TIMEOUT          = 100
BLINKER_MQTT_MSG_LIMIT          = 1000
BLINKER_SMS_MSG_LIMIT           = 60000
BLINKER_PUSH_MSG_LIMIT          = 60000
BLINKER_WECHAT_MSG_LIMIT        = 60000
BLINKER_WEATHER_MSG_LIMIT       = 60000
BLINKER_AQI_MSG_LIMIT           = 60000
BLINKER_MQTT_KEEPALIVE          = 120000
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
BLINKER_CMD_NOTFOUND            = 'device not found'
BLINKER_CMD_SWITCH              = 'swi'
BLINKER_CMD_VALUE               = 'val'
BLINKER_CMD_ICON                = 'ico'
BLINKER_CMD_COLOR               = 'col'
BLINKER_CMD_TITLE               = 'tit'
BLINKER_CMD_CONTENT             = 'con'
BLINKER_CMD_TEXT                = 'tex'
BLINKER_CMD_TEXT1               = 'tex1'
BLINKER_CMD_TEXTCOLOR           = 'tco'
BLINKER_CMD_UNIT                = 'uni'
BLINKER_CMD_BUILTIN_SWITCH      = 'switch'
BLINKER_CMD_MESSAGE             = 'message'
BLINKER_CMD_DETAIL              = 'detail'
BLINKER_JOYSTICK_VALUE_DEFAULT  = 128
BLINKER_MAX_DATA_COUNT          = 4
BLINKER_DATA_FREQ_TIME          = 60.0

BLINKER_MQTT_ALIYUN_HOST        = 'public.iot-as-mqtt.cn-shanghai.aliyuncs.com'
BLINKER_MQTT_ALIYUN_PORT        = 1883

BLINKER_MQTT_QCLOUD_HOST        = 'iotcloud-mqtt.gz.tencentdevices.com'
BLINKER_MQTT_QCLOUD_PORT        = 1883

BLINKER_ALIGENIE_LIGHT          = 'light'
BLINKER_ALIGENIE_OUTLET         = 'outlet'
BLINKER_ALIGENIE_SENSOR         = 'sensor'
BLINKER_DUEROS_LIGHT            = 'LIGHT'
BLINKER_DUEROS_OUTLET           = 'SOCKET'
BLINKER_DUEROS_SENSOR           = 'AIR_MONITOR'
BLINKER_MIOT_LIGHT          = 'light'
BLINKER_MIOT_OUTLET         = 'outlet'
BLINKER_MIOT_SENSOR         = 'sensor'

BLINKER_CMD_QUERY_ALL_NUMBER        = 0
BLINKER_CMD_QUERY_POWERSTATE_NUMBER = 1
BLINKER_CMD_QUERY_COLOR_NUMBER      = 2
BLINKER_CMD_QUERY_MODE_NUMBER       = 3
BLINKER_CMD_QUERY_COLORTEMP_NUMBER  = 4
BLINKER_CMD_QUERY_BRIGHTNESS_NUMBER = 5
BLINKER_CMD_QUERY_TEMP_NUMBER       = 6
BLINKER_CMD_QUERY_HUMI_NUMBER       = 7
BLINKER_CMD_QUERY_PM25_NUMBER       = 8
BLINKER_CMD_QUERY_PM10_NUMBER       = 9
BLINKER_CMD_QUERY_CO2_NUMBER        = 10
BLINKER_CMD_QUERY_AQI_NUMBER        = 11
BLINKER_CMD_QUERY_TIME_NUMBER       = 12

BLINKER_CMD_MODE                    = "mode"
BLINKER_CMD_CANCELMODE              = "cMode"
BLINKER_CMD_READING                 = "reading"
BLINKER_CMD_MOVIE                   = "movie"
BLINKER_CMD_SLEEP                   = "sleep"
BLINKER_CMD_HOLIDAY                 = "holiday"
BLINKER_CMD_MUSIC                   = "music"
BLINKER_CMD_COMMON                  = "common"
BLINKER_CMD_ALIGENIE_READING        = "reading"
BLINKER_CMD_ALIGENIE_MOVIE          = "movie"
BLINKER_CMD_ALIGENIE_SLEEP          = "sleep"
BLINKER_CMD_ALIGENIE_HOLIDAY        = "holiday"
BLINKER_CMD_ALIGENIE_MUSIC          = "music"
BLINKER_CMD_ALIGENIE_COMMON         = "common"
BLINKER_CMD_MIOT_READING        = "reading"
BLINKER_CMD_MIOT_MOVIE          = "movie"
BLINKER_CMD_MIOT_SLEEP          = "sleep"
BLINKER_CMD_MIOT_HOLIDAY        = "holiday"
BLINKER_CMD_MIOT_MUSIC          = "music"
BLINKER_CMD_MIOT_COMMON         = "common"
BLINKER_CMD_DUEROS_READING          = "READING"
BLINKER_CMD_DUEROS_SLEEP            = "SLEEP"
BLINKER_CMD_DUEROS_ALARM            = "ALARM"
BLINKER_CMD_DUEROS_NIGHT_LIGHT      = "NIGHT_LIGHT"
BLINKER_CMD_DUEROS_ROMANTIC         = "ROMANTIC"
BLINKER_CMD_DUEROS_SUNDOWN          = "SUNDOWN"
BLINKER_CMD_DUEROS_SUNRISE          = "SUNRISE"
BLINKER_CMD_DUEROS_RELAX            = "RELAX"
BLINKER_CMD_DUEROS_LIGHTING         = "LIGHTING"
BLINKER_CMD_DUEROS_SUN              = "SUN"
BLINKER_CMD_DUEROS_STAR             = "STAR"
BLINKER_CMD_DUEROS_ENERGY_SAVING    = "ENERGY_SAVING"
BLINKER_CMD_DUEROS_MOON             = "MOON"
BLINKER_CMD_DUEROS_JUDI             = "JUDI"
