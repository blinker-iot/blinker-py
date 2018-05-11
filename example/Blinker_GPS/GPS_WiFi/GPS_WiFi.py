from Blinker import *

Blinker.setMode(BLINKER_WIFI)
Blinker.begin()

if __name__ == '__main__':
    while True:
        Blinker.run()
        
        if Blinker.available() == True:
            BLINKER_LOG('Blinker.readString(): ', Blinker.readString())
            Blinker.print(Blinker.times())
            Blinker.vibrate()
            Blinker.print('millis', millis())
        
        BLINKER_LOG('GPS LONG: ', Blinker.gps(LONG))
        BLINKER_LOG('GPS LAT: ', Blinker.gps(LAT))

        Blinker.delay(2000)
