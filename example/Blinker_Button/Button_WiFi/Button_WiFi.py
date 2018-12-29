from Blinker import *

auth = 'bc5a991c7ec4'

BLINKER_DEBUG.debugAll()

Blinker.mode(BLINKER_WIFI)
# Blinker.debugLevel(BLINKER_DEBUG_ALL)
Blinker.begin(auth)

BUTTON_1 = 'btn-abc'

button1 = BlinkerButton(BUTTON_1)


def button1_callback(state):
    """ """

    BLINKER_LOG('get button state: ', state)

    button1.icon('icon_1')
    button1.color('#FFFFFF')
    button1.text('Your button name or describe')
    button1.print(state)


button1.attach(button1_callback)

if __name__ == '__main__':

    while True:
        Blinker.run()

        if Blinker.available() is True:
            BLINKER_LOG('Blinker.readString(): ', Blinker.readString())
            Blinker.print(Blinker.times())
            # Blinker.vibrate()
            # Blinker.print('millis', millis())

        # if Blinker.button(BUTTON_1):
        #     Blinker.print('Button pressed!')

        # Blinker.delay(2000)
