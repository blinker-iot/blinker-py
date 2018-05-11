from Blinker import *

RGB_1 = ('RGBKey')

Blinker.setMode(BLINKER_WIFI)
Blinker.begin()
Blinker.wInit(RGB_1, W_RGB)

if __name__ == '__main__':
    while True:
        if Blinker.available() == True:
            BLINKER_LOG('Blinker.readString(): ', Blinker.readString())
            Blinker.print(Blinker.times())
            Blinker.vibrate()
            Blinker.print('millis', millis())            

        BLINKER_LOG("Red color: ", Blinker.rgb(RGB_1,R))
        BLINKER_LOG("Green color: ", Blinker.rgb(RGB_1,G))
        BLINKER_LOG("Blue color: ", Blinker.rgb(RGB_1,B))

        Blinker.delay(2000)
