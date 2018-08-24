from Blinker import *

BUTTON_1 = 'ButtonKey'

Blinker.setMode(BLINKER_WIFI)
Blinker.begin()

button1 = BlinkerButton(BUTTON_1)


def button1_callback(btn, state):
    """ """

    BLINKER_LOG('get button state: ', state)

    btn.icon('icon_1')
    btn.color('#FFFFFF')
    btn.text('Your button name or describe')
    btn.print("on")


button1.attach(button1_callback)

if __name__ == '__main__':

    while True:
        Blinker.run()

        if Blinker.available() is True:
            BLINKER_LOG('Blinker.readString(): ', Blinker.readString())
            Blinker.print(Blinker.times())
            Blinker.vibrate()
            Blinker.print('millis', millis())

        # if Blinker.button(BUTTON_1):
        #     Blinker.print('Button pressed!')

        Blinker.delay(2000)
