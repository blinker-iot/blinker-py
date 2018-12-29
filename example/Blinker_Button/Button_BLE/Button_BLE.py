from Blinker import *

BUTTON_1 = 'ButtonKey'
auth = "bc5a991c7ec4"

Blinker.mode(BLINKER_BLE)
Blinker.begin(auth)

button1 = BlinkerButton(BUTTON_1)


def button1_callback(state):
    """ """

    BLINKER_LOG('get button state: ', state)

    button1.icon('icon_1')
    button1.color('#FFFFFF')
    button1.text('Your button name or describe')
    button1.print("on")


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
