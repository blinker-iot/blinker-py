from Blinker import *

SLIDER_1 = ('SliderKey')
TOGGLE_1 = ('ToggleKey')
TEXT_1 = ('millis')

Blinker.setMode(BLINKER_WIFI)
Blinker.begin()
Blinker.wInit(SLIDER_1, W_SLIDER)
Blinker.wInit(TOGGLE_1, W_TOGGLE)

s_value = 0
on_off = 'on'

if __name__ == '__main__':
    while True:
        Blinker.run()
        
        if Blinker.available() == True:
            BLINKER_LOG('Blinker.readString(): ', Blinker.readString())
            Blinker.print(Blinker.times())
            Blinker.vibrate()
            Blinker.print('millis', millis())            

        Blinker.print(SLIDER_1, s_value)
        Blinker.print(TOGGLE_1, on_off)
        Blinker.print(TEXT_1, millis())

        if s_value is 255:
            s_value = 0
        else:
            s_value = s_value + 1

        if on_off is 'on':
            on_off = 'off'
        else:
            on_off = 'on'

        Blinker.delay(2000)
