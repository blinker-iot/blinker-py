from Blinker import *

Blinker.mode(BLINKER_WIFI)
Blinker.begin()

joy1 = BlinkerJoystick('JOY_1')


def joystick_callback(xAxis, yAxis):
    BLINKER_LOG('Joystick1 X axis: ', xAxis)
    BLINKER_LOG('Joystick1 Y axis: ', yAxis)


joy1.attach(joystick_callback)

if __name__ == '__main__':
    while True:
        Blinker.run()

        if Blinker.available() is True:
            BLINKER_LOG('Blinker.readString(): ', Blinker.readString())
            Blinker.print(Blinker.times())
            Blinker.vibrate()
            Blinker.print('millis', millis())

        Blinker.delay(2000)
