from Blinker import Blinker, BlinkerSlider, BlinkerText, BUILTIN_SWITCH
from Blinker import BLINKER_LOG, BLINKER_WIFI
from Blinker import millis

SLIDER_1 = 'SliderKey'
TEXT_1 = 'millis'

Blinker.setMode(BLINKER_WIFI)
Blinker.begin()
# Blinker.wInit(SLIDER_1, W_SLIDER)
# Blinker.wInit(TOGGLE_1, W_TOGGLE)

slider1 = BlinkerSlider(SLIDER_1)
text1 = BlinkerText(TEXT_1)

s_value = 0
on_off = 'on'

if __name__ == '__main__':
    while True:
        Blinker.run()

        if Blinker.available() is True:
            BLINKER_LOG('Blinker.readString(): ', Blinker.readString())
            Blinker.print(Blinker.times())
            Blinker.vibrate()
            Blinker.print('millis', millis())

        Blinker.print(slider1.name, s_value)
        Blinker.print(BUILTIN_SWITCH.name, on_off)
        Blinker.print(text1.name, millis())

        if s_value is 255:
            s_value = 0
        else:
            s_value = s_value + 1

        if on_off is 'on':
            on_off = 'off'
        else:
            on_off = 'on'

        Blinker.delay(2000)
