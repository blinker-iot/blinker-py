from Blinker import *

BUTTON_1 = ('ButtonKey')
SLIDER_1 = ('SliderKey')
TOGGLE_1 = ('ToggleKey')
RGB_1 = ('RGBKey')
TEXT_1 = ('millis')

Blinker.setMode(BLINKER_WIFI)
Blinker.begin()
Blinker.wInit(BUTTON_1, W_BUTTON)
Blinker.wInit(SLIDER_1, W_SLIDER)
Blinker.wInit(TOGGLE_1, W_TOGGLE)
Blinker.wInit(RGB_1, W_RGB)
# Blinker.attachAhrs()

s_value = 0
on_off = 'on'

if __name__ == '__main__':
    while True:
        if Blinker.available() == True:
            BLINKER_LOG('Blinker.readString(): ', Blinker.readString())
            Blinker.print(Blinker.times())
            Blinker.vibrate()
            Blinker.print('millis', millis())            

        if Blinker.button(BUTTON_1):
            Blinker.print('Button pressed!')
            Blinker.notify('!Button pressed!')

        # if Blinker.toggle(TOGGLE_1):
        #     Blinker.print('Toggle on!')
        # else:
        #     Blinker.print('Toggle off!')

        Blinker.print(SLIDER_1, s_value)
        Blinker.print(TOGGLE_1, on_off)
        Blinker.print(TEXT_1, millis())

        if s_value is 255:
            s_value = 0
        else:
            s_value = s_value + 1

        if on_off is 'on':
            on_off = 'off'
        else:
            on_off = 'on'

        # BLINKER_LOG("Joystick X axis: ", Blinker.joystick(J_Xaxis))
        # BLINKER_LOG("Joystick Y axis: ", Blinker.joystick(J_Yaxis))
        # BLINKER_LOG("AHRS Yaw: ", Blinker.ahrs(Yaw))
        # BLINKER_LOG("AHRS Roll: ", Blinker.ahrs(Roll))
        # BLINKER_LOG("AHRS Pitch: ", Blinker.ahrs(Pitch))
        # BLINKER_LOG("Slider read: ", Blinker.slider(SLIDER_1))
        # BLINKER_LOG("Red color: ", Blinker.rgb(RGB_1,R))
        # BLINKER_LOG("Green color: ", Blinker.rgb(RGB_1,G))
        # BLINKER_LOG("Blue color: ", Blinker.rgb(RGB_1,B))

        Blinker.delay(2000)
