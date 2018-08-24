from Blinker import *

BUTTON_1 = 'ButtonKey'

Blinker.setMode(BLINKER_BLE)
Blinker.begin()

button1 = BlinkerButton(BUTTON_1)


def button1_callback(btn1, state):
    """ """

    BLINKER_LOG('get button state: ', state)

    btn1.icon('icon_1')
    btn1.color('#FFFFFF')
    btn1.text('Your button name or describe')
    btn1.print("on")


button1.attach(button1_callback)

if __name__ == '__main__':
    while True:
        Blinker.run()

        if Blinker.available() is True:
            BLINKER_LOG('Blinker.readString(): ', Blinker.readString())
            Blinker.print(Blinker.times())
            Blinker.vibrate()
            Blinker.print('millis', millis())

        Blinker.delay(2000)
