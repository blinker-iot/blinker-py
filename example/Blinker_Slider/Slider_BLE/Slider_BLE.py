from Blinker import *

SLIDER_1 = ('SliderKey')

Blinker.setMode(BLINKER_BLE)
Blinker.begin()
Blinker.wInit(SLIDER_1, W_SLIDER)

if __name__ == '__main__':
    while True:
        Blinker.run()
        
        if Blinker.available() == True:
            BLINKER_LOG('Blinker.readString(): ', Blinker.readString())
            Blinker.print(Blinker.times())
            Blinker.vibrate()
            Blinker.print('millis', millis())
        
        BLINKER_LOG("Slider read: ", Blinker.slider(SLIDER_1))

        Blinker.delay(2000)
