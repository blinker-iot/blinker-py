from Blinker import *

Blinker.mode(BLINKER_BLE)
Blinker.begin()

if __name__ == '__main__':
    while True:
        Blinker.run()
        
        if Blinker.available() == True:
            BLINKER_LOG('Blinker.readString(): ', Blinker.readString())
            Blinker.print(Blinker.times())
            Blinker.vibrate()
            Blinker.print('millis', millis())            

        BLINKER_LOG("Joystick X axis: ", Blinker.joystick(J_Xaxis))
        BLINKER_LOG("Joystick Y axis: ", Blinker.joystick(J_Yaxis))

        Blinker.delay(2000)
