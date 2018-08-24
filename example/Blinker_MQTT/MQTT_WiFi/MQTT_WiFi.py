from Blinker import *

BUTTON_1 = 'ButtonKey'
auth = "57fcb3a53ab3"

blinker = Blinker.setMode(BLINKER_MQTT)
blinker.begin(auth)
blinker.wInit(BUTTON_1, W_BUTTON)

if __name__ == '__main__':
    while True:
        blinker.run()
        
        if blinker.available() is True:
            BLINKER_LOG('Blinker.readString(): ', blinker.readString())

            blinker.beginFormat()
            blinker.print(blinker.times())
            blinker.vibrate()
            blinker.print('millis', millis())
            blinker.endFormat()

        if blinker.button(BUTTON_1):
            blinker.print('Button pressed!')
