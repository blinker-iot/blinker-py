# blinker-py
Blinker python library for hardware. Works with Raspberry Pi, linux, windows.  

# What's Blinker
[Blinker](https://blinker-iot.com/) is a platform with iOS and Android apps to control embedded hardware like Arduino. You can easily build graphic interfaces for all your projects by simply dragging and dropping widgets.  
  
[Blinker](https://blinker-iot.com/) 是一个运行在 IOS 和 Android 上用于控制嵌入式硬件的应用程序。你可以通过拖放控制组件，轻松地为你的项目建立图形化控制界面。  

# Reference/参考
* [EN-英文](https://github.com/blinker-iot/blinker-py#currently-supported-hardware)  
* [CN-中文](https://github.com/blinker-iot/blinker-py#%E7%9B%AE%E5%89%8D%E6%94%AF%E6%8C%81%E7%9A%84%E7%A1%AC%E4%BB%B6)  

  
# Currently supported hardware
* Raspberry Pi boards
<!-- * Arduino boards
    - Arduino Uno, Duemilanove
    - Arduino Nano, Mini, Pro Mini, Pro Micro, Due, Mega
* ESP8266 based boards with [esp8266/arduino](https://github.com/esp8266/arduino)  
* ESP32 based board with [espressif/arduino-esp32](https://github.com/espressif/arduino-esp32)   -->
  
# Connection types
* Bluetooth Smart (BLE 4.0)  
* WiFi  
* MQTT  
  
# Prerequisites
You should have the following ready before beginning with hardware:
* [python3.x](https://www.python.org/downloads/) 
* Install the [simple-websocket-server](https://github.com/dpallot/simple-websocket-server)  
`pip3 install git+https://github.com/dpallot/simple-websocket-server.git`  

* Install the [python-zeroconf](https://github.com/jstasiak/python-zeroconf)  
`pip3 install zeroconf`   

* Install the [paho.mqtt.python](https://github.com/eclipse/paho.mqtt.python)  
`pip3 install paho-mqtt`

* Install the [requests](https://github.com/requests/requests)  
`pip3 install requests`  

<!-- py2.7.x : `pip install https://github.com/jstasiak/python-zeroconf/archive/0.17.7.zip`   -->
* Install the [blinker-py](https://github.com/blinker-iot/blinker-py)  
`pip3 install git+https://github.com/blinker-iot/blinker-py.git`  



  
# Blinker Api
## Configuration
### Blinker.begin()
Call **Blinker.begin()** to configure Blinker:
```
Blinker.begin(...);
```
Choose different parameters based on the type of connection you use  
  
BLE:
```
from Blinker import * 
  
Blinker.setMode(BLINKER_BLE)
Blinker.begin()
```  

<!-- >SerialBLE Modules:  
>**Blinker.begin()** will config SoftWareSerial with default settings.  
>  
>Blinker.begin();// default settings digital pins 2(RX) 3(TX) and baudrate 9600 bps  
>Blinker.begin(4, 5);// config digital pins 4(RX) 5(TX) with default baudrate 9600 bps  
>Blinker.begin(4, 5, 115200);// config digital pins 4(RX) 5(TX) and baudrate 115200 bps   -->
  
WiFi:
```
from Blinker import *  
  
Blinker.setMode(BLINKER_WIFI)  
Blinker.begin()
```  
  
MQTT:
```
from Blinker import *  
  
Blinker.setMode(BLINKER_MQTT)  
Blinker.begin()
```
<!-- > MQTT support hardware: WiFiduino, WiFiduino32, ESP8266, ESP32   -->

**begin()** is basically doing these steps:  
1.Configure hardware  
2.Wait for connection app  

## Connection management
### Blinker.connect()
This function will try onnecting to app.  
Return true when connected, return false if timeout reached.  
Default timeout is 10 seconds.
```
result = Blinker.connect()  
  

timeout = 30000 # ms  
result = Blinker.connect(timeout)
```
### Blinker.disconnect()
Disconnect **Blinker** connection
```
Blinker.disconnect()
```
### Blinker.connected()
Get the status of **Blinker** connection
```
result = Blinker.connected()
```  
### Blinker.run()
This function should be called frequently to process incoming commands and perform of Blinker connection. It is usually called in main
```
if __name__ == '__main__':  
    while True:  
        Blinker.run()
```
## Data management
### Blinker.available()
Return true when data already arrived and stored in the receive buffer
```
if Blinker.available():  
    print('data available')  
else:  
    print('none data')
```
### Blinker.readString()
This function to reads characters from Blinker into a string.
```
data = Blinker.readString()
```
`*max read data bytes is 256bytes`
### Blinker.print()
Prints data to Blinker app
```
Blinker.print(data)
```
Prints a Json data to Blinkrt app, eg: {"temp":30.2}
```
Blinker.print("temp", 30.2)
```  
Prints a Json data with unit to Blinkrt app, eg: {"temp":"30.2 °C"}
```
Blinker.print("temp", 30.2, "°C");
```
>Json data can display in the Blinker TEXT widget  

`*max send data bytes is 128bytes`  

### Blinker.notify()
when use **notify** . Sending data begins with exclamation point, will send notification to app,  otherwise Json data will be sent to app.  

send notify
```
Blinker.notify("!notify")
```
send Json data, eg: {"notice":"notify"}
```
Blinker.notify("notify")
```  

## App Widgets
### Blinker.wInit()
Init widget, **Button** **Slider** and **Toggle** widget recommended to initialize before use.
```
Blinker.wInit("ButtonName", W_BUTTON)  
Blinker.wInit("SliderName", W_SLIDER)  
Blinker.wInit("ToggleName", W_TOGGLE)//keyName, type  
```
>type:  
>W_BUTTON Button  
>W_SLIDER Slider  
>W_TOGGLE Toggle  
>W_RGB    RGB  

### Blinker.button() 
Device receives an update of **Button** state from app, return true when **Pressed**, return false when **Released**.
```
if Blinker.button("Button1"):  
    print('Button pressed!')  
else:  
    print('Button released!')
```  
### Blinker.slider()
Return the latest update of **Slider** value from app
```
result = Blinker.slider("Slider1")
```
### Blinker.toggle() 
Device receives an update of **Toggle** state from app, return true when **ON**, return false when **OFF**.
```
if Blinker.toggle("Toggle1"):  
    print('Toggle1 on!')  
else:  
    print('Toggle1 off!')
```
### Blinker.joystick()
Return the latest update of **Joystick** value from app
```
result_X = Blinker.joystick(J_Xaxis)  
result_Y = Blinker.joystick(J_Yaxis)
```
### Blinker.ahrs()
Send **AHRS** attach commond to Blinker
```
Blinker.attachAhrs()
```
Return the latest update of **AHRS** value from app
```
result_Yaw = Blinker.ahrs(Yaw)  
result_Roll = Blinker.ahrs(Roll)  
result_Pitch = Blinker.ahrs(Pitch)
```
Send **AHRS** detach commond to Blinker
```
Blinker.detachAhrs()
```
### Blinker.gps()
<!-- Send **GPS** fresh commond to Blinker
```
Blinker.freshGPS();
``` -->
Return the latest update of **GPS** value from app
```
result_LONG = Blinker.gps(LONG)  
result_LAT = Blinker.gps(LAT)
```
> LONG for longitude  
> LAT for latitude  

### Blinker.rgb()
Return the latest update of **RGB** value from app
```
result_R = Blinker.rgb("RGBKEY", R)  
result_G = Blinker.rgb("RGBKEY", G)  
result_B = Blinker.rgb("RGBKEY", B)
```
### Blinker.vibrate()
Send vibrate commond to Blinker, default vibration time is 500 milliseconds
```
Blinker.vibrate()  
Blinker.vibrate(255)
```
## Delay
### Blinker.delay()
This function can process incoming commands and perform of Blinker connection when delay
```
Blinker.delay(500)
```  
## Debug
<!-- To enable debug prints on the Serial, add this on the top of your sketch:
```
#define BLINKER_PRINTER Serial
```
Init & enable Serial in `void setup()` :
```
Serial.begin(115200);
```
You can also use spare HardWareSerial or SoftWareSerial for debug output (you will need an adapter to connect to it with your PC).   -->
  
If you want debug output all detail :
```
from Blinker import *  

Blinker.setMode(BLINKER_WIFI)  
Blinker.debugLevel(BLINKER_DEBUG_ALL)  
Blinker.begin()
```
## LOG
After enabled debug, you can use **BLINKER_LOG()** to debug output:
```
BLINKER_LOG("detail message 1")  
BLINKER_LOG("detail message 1", " 2")  
```
  
# Thanks
[simple-websocket-server](https://github.com/dpallot/simple-websocket-server) - for Blinker to build up a websocket server  
[python-zeroconf](https://github.com/jstasiak/python-zeroconf) - for Blinker to build up a mDNS service  
[paho.mqtt.python](https://github.com/eclipse/paho.mqtt.python) - for Blinker to build up a MQTT Client  
[requests](https://github.com/requests/requests) - for Blinker to send a web request  
  

---
# 目前支持的硬件
<!-- * Arduino boards
    - Arduino Uno, Duemilanove
    - Arduino Nano, Mini, Pro Mini, Pro Micro, Due, Mega
* 使用 [esp8266/arduino](https://github.com/esp8266/arduino) 的ESP8266  
* 使用 [espressif/arduino-esp32](https://github.com/espressif/arduino-esp32) 的ESP32   -->
  
# 连接类型
* Bluetooth Smart (BLE 4.0)  
* WiFi  
* MQTT  
  
# 准备工作
开始使用前你需要做好如下准备:
* [python3.x](https://www.python.org/downloads/) 
* Install the [simple-websocket-server](https://github.com/dpallot/simple-websocket-server)  
`pip3 install git+https://github.com/dpallot/simple-websocket-server.git`  

* Install the [python-zeroconf](https://github.com/jstasiak/python-zeroconf)  
`pip3 install zeroconf`   

* Install the [paho.mqtt.python](https://github.com/eclipse/paho.mqtt.python)  
`pip3 install paho-mqtt`

* Install the [requests](https://github.com/requests/requests)  
`pip3 install requests`  

<!-- py2.7.x : `pip install https://github.com/jstasiak/python-zeroconf/archive/0.17.7.zip`   -->
* Install the [blinker-py](https://github.com/blinker-iot/blinker-py)  
`pip3 install git+https://github.com/blinker-iot/blinker-py.git`  
<!-- py2.7.x : `pip install https://github.com/jstasiak/python-zeroconf/archive/0.17.7.zip`  
py3.x : `pip install zeroconf`  -->
<!-- * 使用 Arduino IDE 的库管理器安装 [WebSockets](https://github.com/Links2004/arduinoWebSockets)     -->
  
# Blinker接口函数
## 设备配置
### Blinker.begin()
使用 **Blinker.begin()** 来配置 Blinker:
```
Blinker.begin(...);
```
根据你使用的连接方式选择不同的参数用于配置Blinker  
  

BLE:
```
from Blinker import *  
  
Blinker.setMode(BLINKER_BLE)  
Blinker.begin()
```  
  
<!-- >串口蓝牙模块:  
>**Blinker.begin()** 将使用默认设置配置 SoftWareSerial   
>  
>Blinker.begin();// 默认设置: 数字IO 2(RX) 3(TX), 波特率 9600 bps  
>Blinker.begin(4, 5);// 设置数字IO 4(RX) 5(TX), 默认波特率 9600 bps  
>Blinker.begin(4, 5, 115200);// 设置数字IO 4(RX) 5(TX) 及波特率 115200 bps   -->
  
WiFi:
```
from Blinker import *  
  
Blinker.setMode(BLINKER_WIFI)  
Blinker.begin()
```  
  
MQTT:
```
from Blinker import *  
  
Blinker.setMode(BLINKER_MQTT)  
Blinker.begin()
```
<!-- > MQTT 支持的硬件: WiFiduino, WiFiduino32, ESP8266, ESP32   -->

**begin()** 主要完成以下配置:  
1.初始化硬件设置;  
2.连接网络并广播设备信息等待app连接;
## 连接管理
### Blinker.connect()
建立 **Blinker** 设备间连接并返回连接状态, 默认超时时间为10秒
```
result = Blinker.connect()  
  

timeout = 30000 # ms  
result = Blinker.connect(timeout)
```
### Blinker.disconnect()
断开 **Blinker** 设备间连接
```
Blinker.disconnect()
```
### Blinker.connected()
返回 **Blinker** 设备间连接状态
```
result = Blinker.connected()
```  
### Blinker.run()
此函数需要频繁调用以保持设备间连接及处理收到的数据, 建议放在 **main** 函数中
```
if __name__ == '__main__':  
    while True:  
        Blinker.run()
```
## 数据管理
### Blinker.available()
检测是否有接收到数据
```
if Blinker.available():  
    print('data available')  
else:  
    print('none data')
```
### Blinker.readString()
读取接收到的数据
```
data = Blinker.readString()
```
`*读取数据最大为 256 字节`
### Blinker.print()
发送数据
```
Blinker.print(data)
```
发送一个Json数据, 如 {text1:data}
```
Blinker.print(text1, data)
```  
发送一个带单位的Json数据, eg: {"temp":"30.2 °C"}
```
Blinker.print("temp", 30.2, "°C")
```
>发送的Json数据可以在 Blinker APP 的 TEXT 组件中显示  

`*发送数据最大为 128 字节`

### Blinker.notify()
使用 **notify** 时, 发送数据以感叹号开始, 将会发送消息通知到app, 否则将会发送Json数据到app  

发送通知
```
Blinker.notify("!notify")
```
发送Json数据, 如 {"notice":"notify"}
```
Blinker.notify("notify")
```

## App Widgets
### Blinker.wInit()
组件初始化, 建议在使用前初始化 **Button** 、**Slider** 、 **Toggle** 及 **RGB**
```
Blinker.wInit("ButtonName", W_BUTTON)  
Blinker.wInit("SliderName", W_SLIDER)  
Blinker.wInit("ToggleName", W_TOGGLE)
Blinker.wInit("RGBName", W_RGB)//键词, 类型  
```
>类型:  
>W_BUTTON 按键  
>W_SLIDER 滑动条  
>W_TOGGLE 开关  
>W_RGB    RGB调色板  


### Blinker.button() 
读取开关/按键数据, 按下(Pressed)时返回true, 松开(Released)时返回false
```
if Blinker.button("Button1"):  
    print('Button pressed!')  
else:  
    print('Button released!')
```
### Blinker.slider()
读取滑动条数据
```
result = Blinker.slider("Slider1")
```
### Blinker.toggle() 
读取拨动开关数据, 打开(ON)时返回true, 关闭(OFF)时返回false
```
if Blinker.toggle("Toggle1"):  
    print('Toggle1 on!')  
else:  
    print('Toggle1 off!')
```
### Blinker.joystick()
读取摇杆数据
```
result_X = Blinker.joystick(J_Xaxis)  
result_Y = Blinker.joystick(J_Yaxis)
```
### Blinker.ahrs()
开启手机 **AHRS** 功能
```
Blinker.attachAhrs()
```
读取 **AHRS** 数据
```
result_Yaw = Blinker.ahrs(Yaw)  
result_Roll = Blinker.ahrs(Roll)  
result_Pitch = Blinker.ahrs(Pitch)
```
关闭手机 **AHRS** 功能
```
Blinker.dettachAhrs()
```
### Blinker.gps()
<!-- 刷新手机 **GPS** 功能
```
Blinker.freshAhrs();
``` -->
读取 **GPS** 数据
```
result_LONG = Blinker.gps(LONG)  
result_LAT = Blinker.gps(LAT)
```
> LONG 经度  
> LAT 维度  

### Blinker.rgb()
读取 **RGB** 数据
```
result_R = Blinker.rgb("RGBKEY", R)
result_G = Blinker.rgb("RGBKEY", G)
result_B = Blinker.rgb("RGBKEY", B)
```
### Blinker.vibrate()
发送手机振动指令, 震动时间, 单位ms 毫秒, 数值范围0-1000, 默认为500
```
Blinker.vibrate();
Blinker.vibrate(255);  
```
## 设备延时
### Blinker.delay()
延时函数, 在延时过程中仍保持设备间连接及数据接收处理
```
Blinker.delay(500)
```
>*为了连接设备成功, 需要延时时务必使用该函数;  
>使用此函数可以在延时期间连接设备及接收数据并处理数据, 延时完成后才能执行后面的程序;  
## Debug
<!-- 将这行代码添加到你的工程文件第一行, 以启用串口调试输出功能:
```
#define BLINKER_PRINTER Serial
```
在 `void setup()` 中初始化串口Serial :
```
Serial.begin(115200);
```
你可以用额外的硬件串口 (HardWareSerial) 或者软串口 (SoftWareSerial) 来调试输出 (你需要额外的适配器将该串口连接到你的电脑上).  
   -->
如果你想调试输出更多细节信息 :
```
from Blinker import *

Blinker.setMode(BLINKER_WIFI)
Blinker.debugLevel(BLINKER_DEBUG_ALL)
Blinker.begin()
```
## LOG
开启调试输出 (Debug) 后可以使用 **BLINKER_LOG()** 打印输出调试信息:
```
BLINKER_LOG("detail message 1")  
BLINKER_LOG("detail message 1", " 2")    
```

# 感谢
[simple-websocket-server](https://github.com/dpallot/simple-websocket-server) - Blinker 用这个库建立了一个 websocket 服务器  
[python-zeroconf](https://github.com/jstasiak/python-zeroconf) - Blinker 用这个库建立了一个 mDNS 服务  
[paho.mqtt.python](https://github.com/eclipse/paho.mqtt.python) - Blinker 用这个库建立了一个 MQTT Client  
[requests](https://github.com/requests/requests) - Blinker 用这个库发送网络请求  

