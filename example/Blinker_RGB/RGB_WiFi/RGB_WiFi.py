from Blinker import *

RGB_1 = 'RGBKey'

Blinker.mode(BLINKER_WIFI)
Blinker.begin()

rgb1 = BlinkerRGB(RGB_1)


def rgb1_callback(r_value, g_value, b_value, bright_value):
    BLINKER_LOG("R value: ", r_value)
    BLINKER_LOG("G value: ", g_value)
    BLINKER_LOG("B value: ", b_value)
    BLINKER_LOG("Brightness value: ", bright_value)


rgb1.attach(rgb1_callback)

if __name__ == '__main__':
    while True:
        Blinker.run()

        if Blinker.available() is True:
            BLINKER_LOG('Blinker.readString(): ', Blinker.readString())
            Blinker.print(Blinker.times())
            Blinker.vibrate()
            Blinker.print('millis', millis())

        Blinker.delay(2000)
