from Blinker import *

Blinker.setMode(BLINKER_WIFI)
Blinker.begin()
Blinker.wInit(TOGGLE_1, W_TOGGLE)

if __name__ == '__main__':
    while True:
        if Blinker.available() == True:
            BLINKER_LOG('Blinker.readString(): ', Blinker.readString())
            Blinker.print(Blinker.times())
            Blinker.vibrate()
            Blinker.print('millis', millis())            

        if Blinker.toggle(TOGGLE_1):
            Blinker.print('Toggle on!')
        else:
            Blinker.print('Toggle off!')

        Blinker.delay(2000)
