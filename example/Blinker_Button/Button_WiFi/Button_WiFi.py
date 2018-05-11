from Blinker import *

Button1 = ('Button')

Blinker.setMode(BLINKER_WIFI)
Blinker.begin()
Blinker.wInit(Button1, W_BUTTON)
Blinker.wInit(Button1, W_BUTTON)

if __name__ == '__main__':
    while True:
        if Blinker.available() == True:
            BLINKER_LOG('Blinker.readString(): ', Blinker.readString())
            Blinker.Print(Blinker.times())
            Blinker.vibrate()

        if Blinker.button(Button1):
            Blinker.Print('Button pressed!')
