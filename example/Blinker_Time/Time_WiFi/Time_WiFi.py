from Blinker import *

BUTTON_1 = ('ButtonKey')

Blinker.setMode(BLINKER_WIFI)
Blinker.begin()
Blinker.wInit(BUTTON_1, W_BUTTON)

if __name__ == '__main__':
    while True:
        Blinker.run()
        
        if Blinker.available() == True:
            BLINKER_LOG('Blinker.readString(): ', Blinker.readString())
            Blinker.print(Blinker.times())
            Blinker.vibrate()
            Blinker.print('millis', millis())            

        if Blinker.button(BUTTON_1):
            Blinker.print('Button pressed!')
            BLINKER_LOG("Now second: ", Blinker.second())
            BLINKER_LOG("Now minute: ", Blinker.minute())
            BLINKER_LOG("Now hour: ", Blinker.hour())
            BLINKER_LOG("Now wday: ", Blinker.wday())
            BLINKER_LOG("Now month: ", Blinker.month())
            BLINKER_LOG("Now mday: ", Blinker.mday())
            BLINKER_LOG("Now year: ", Blinker.year())
            BLINKER_LOG("Now yday: ", Blinker.yday())
            BLINKER_LOG("Now time: ", Blinker.time())
        
        Blinker.delay(2000)
