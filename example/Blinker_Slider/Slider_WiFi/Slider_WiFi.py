from Blinker import *

SLIDER_1 = 'SliderKey'

Blinker.mode(BLINKER_WIFI)
Blinker.begin()

slider1 = BlinkerSlider(SLIDER_1)


def slider1_callback(value):
    BLINKER_LOG('get slider value: ', value)


slider1.attach(slider1_callback)

if __name__ == '__main__':
    while True:
        Blinker.run()

        if Blinker.available() is True:
            BLINKER_LOG('Blinker.readString(): ', Blinker.readString())
            Blinker.print(Blinker.times())
            Blinker.vibrate()
            Blinker.print('millis', millis())

        # BLINKER_LOG("Slider read: ", Blinker.slider(SLIDER_1))

        Blinker.delay(2000)
