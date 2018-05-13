from Blinker import *

BUTTON_1 = ('ButtonKey')
auth = ('Your AuthKey')

Blinker.setMode(BLINKER_MQTT)
Blinker.begin(auth)
Blinker.wInit(BUTTON_1, W_BUTTON)

if __name__ == '__main__':
    while True:
        Blinker.run()
        
        if Blinker.available() == True:
            BLINKER_LOG('Blinker.readString(): ', Blinker.readString())
            Blinker.print(Blinker.times())
            Blinker.delay(1000)
            Blinker.vibrate()
            Blinker.delay(1000)
            Blinker.print('millis', millis())        

        if Blinker.button(BUTTON_1):
            Blinker.print('Button pressed!')
        
        Blinker.delay(2000)
