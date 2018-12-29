from Blinker import *

auth = 'Your Device Secret Key'

BLINKER_DEBUG.debugAll()

Blinker.mode(BLINKER_WIFI)
Blinker.begin(auth)

button1 = BlinkerButton("btn-abc")
number1 = BlinkerNumber("num-abc")

counter = 0

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
            BLINKER_LOG("Blinker.readString(): ", Blinker.readString())
            counter += 1
            number1.print(counter)
