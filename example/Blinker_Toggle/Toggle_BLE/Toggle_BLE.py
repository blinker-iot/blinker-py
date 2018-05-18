from Blinker import *

TOGGLE_1 = ('ToggleKey')

Blinker.setMode(BLINKER_BLE)
Blinker.begin()
Blinker.wInit(TOGGLE_1, W_TOGGLE)

if __name__ == '__main__':
    while True:
        Blinker.run()
        
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
