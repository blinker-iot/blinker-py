from Blinker.BlinkerConfig import *

def BLINKER_LOG(arg1, *vartuple):
    # timeInfo = time.strftime("%H:%M:%S %Y", time.localtime())
    data = str(arg1)
    for var in vartuple:
        data = data + str(var)
    data = '[' + now() + ']' + data
    print(data)

def BLINKER_ERR_LOG(arg1, *vartuple):
    # timeInfo = time.strftime("%H:%M:%S %Y", time.localtime())
    data = str(arg1)
    for var in vartuple:
        data = data + str(var)
    data = '[' + now() + '] Error: ' + data
    print(data)
    