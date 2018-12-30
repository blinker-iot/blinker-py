from Blinker import *

BLINKER_DEBUG.debugAll()

Blinker.mode(BLINKER_BLE)
Blinker.begin()

text1 = BlinkerText("TextKey")

def data_callback(data):
    BLINKER_LOG("Blinker readString: ", data)
    text1.print("os time", millis())

Blinker.attachData(data_callback)

if __name__ == '__main__':

    while True:
        Blinker.run()
