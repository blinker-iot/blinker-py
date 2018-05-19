from __future__ import absolute_import, print_function, unicode_literals

import os
import dbus
import dbus.mainloop.glib

import array

try:
    from gi.repository import GObject
    # from gi.repository import GLib
except ImportError:
    import gobject as GObject

from BlinkerAdapters.bluez_components import *
from random import randint

import sys
import re
from optparse import OptionParser, make_option
import BlinkerAdapters.bluezutils

# from threading import Thread
import threading
from Blinker.BlinkerConfig import *
from Blinker.BlinkerDebug import *
from BlinkerUtility.BlinkerUtility import *

class BLE_Proto():
    msgBuf = ''
    isRead = False
    state = CONNECTED
    debug = BLINKER_DEBUG
    BLE_Response = None

bleProto = BLE_Proto()

def isDebugAll():
    if bleProto.debug == BLINKER_DEBUG_ALL:
        return True
    else:
        return False

class CharacteristicUserDescriptionDescriptor(Descriptor):
    CUD_UUID = '2902'

    def __init__(self, bus, index, characteristic):
        self.writable = 'writable-auxiliaries' in characteristic.flags
        self.value = array.array('B', b'This is a characteristic for testing')
        self.value = self.value.tolist()
        Descriptor.__init__(
                self, bus, index,
                self.CUD_UUID,
                ['read', 'write'],
                characteristic)

    def ReadValue(self, options):
        if isDebugAll() is True:
            BLINKER_LOG('2902 Read: ' + str(self.value))
        return self.value

    def WriteValue(self, value, options):
        if not self.writable:
            raise NotPermittedException()
        self.value = value

class BLEMessageService(Characteristic):
    ROW_UUID = 'FFE1'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
            self, bus, index,
            self.ROW_UUID,
            ['read', 'write-without-response', 'notify'],
            service)
        self.notifying = False
        self.value = [0x00, 0x00]
        self.hr_ee_count = 0
        bleProto.BLE_Response = self

    def ReadValue(self, options):
        if isDebugAll() is True:
            BLINKER_LOG('FFE1 Read: ' + str(self.value))

        option_list = [
                        make_option("-i", "--device", action="store",
                                type="string", dest="dev_id"),
                        ]
        parser = OptionParser(option_list=option_list)

        return self.value

    def WriteValue(self, value, options):
        # BLINKER_LOG('FFE1 read: ' + str(value))

        bleProto.msgBuf = ''
        length = len(value)
        
        for i in range(0, length):
            bleProto.msgBuf = bleProto.msgBuf + str(value[i])

        if isDebugAll() is True:
            BLINKER_LOG('FFE1 read: ' + bleProto.msgBuf)

        bleProto.isRead = True

    def StartNotify(self):
        if self.notifying:
            if isDebugAll() is True:
                BLINKER_LOG('Already notifying, nothing to do')
            return
        else:
            if isDebugAll() is True:
                BLINKER_LOG('Already notifying!')
        self.notifying = True

    def StopNotify(self):
        if not self.notifying:
            if isDebugAll() is True:
                BLINKER_LOG('Not notifying, nothing to do')
            return
        self.notifying = False

class BLEService(Service):
    LED_SVC_UUID = 'FFE0'

    def __init__(self, bus, index):
        Service.__init__(self, bus, index, self.LED_SVC_UUID, True)
        self.add_characteristic(BLEMessageService(bus, 0, self))
        self.energy_expended = 0

class BLEApplication(Application):
    def __init__(self, bus):
        Application.__init__(self, bus)
        self.add_service(BLEService(bus, 0))

class BLEAdvertisement(Advertisement):
    def __init__(self, bus, index):
        Advertisement.__init__(self, bus, index, 'peripheral')
        p = os.popen('hciconfig')
        data = p.read()
        len = data.find('Address:')
        add = data[len+9:len+9+17]
        add1 = (int(add[0:2], 16))
        add2 = (int(add[3:5], 16))
        add3 = (int(add[6:8], 16))
        add4 = (int(add[9:11], 16))
        add5 = (int(add[12:14], 16))
        add6 = (int(add[15:17], 16))
        dbaddr = [add1, add2, add3, add4, add5, add6]
        self.add_service_uuid('FFE0')
        self.add_manufacturer_data(0xffff, dbaddr)
        self.add_local_name('BlinkerRaspi')
        self.include_tx_power = True


def register_ad_cb():
    """
    Callback if registering advertisement was successful
    """
    if isDebugAll() is True:
        BLINKER_LOG('Advertisement registered')


def register_ad_error_cb(error):
    """
    Callback if registering advertisement failed
    """
    if isDebugAll() is True:
        BLINKER_LOG('Failed to register advertisement: ' + str(error))
    mainloop.quit()


def register_app_cb():
    """
    Callback if registering GATT application was successful
    """
    if isDebugAll() is True:
        BLINKER_LOG('GATT application registered')


def register_app_error_cb(error):
    """
    Callback if registering GATT application failed.
    """
    if isDebugAll() is True:
        BLINKER_LOG('Failed to register application: ' + str(error))
    mainloop.quit()

def mainInit():
    os.system('sudo service bluetooth stop')

    global mainloop

    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SystemBus()

    service_manager = get_service_manager(bus)
    ad_manager = get_ad_manager(bus)

    app = BLEApplication(bus)

    # Create advertisement
    test_advertisement = BLEAdvertisement(bus, 0)

    mainloop = GObject.MainLoop()

    # Register gatt services
    service_manager.RegisterApplication(app.get_path(), {},
                                        reply_handler=register_app_cb,
                                        error_handler=register_app_error_cb)

    # Register advertisement
    ad_manager.RegisterAdvertisement(test_advertisement.get_path(), {},
                                     reply_handler=register_ad_cb,
                                     error_handler=register_ad_error_cb)

    try:
        mainloop.run()
    except KeyboardInterrupt:
        BLINKER_LOG ("exit")

# class BlinkerBLEService(Thread):
class BlinkerBLEService():
    def __init__(self):
        # Thread.__init__(self)
        self._isClosed = False
        self.thread = None

        os.system('sudo service bluetooth stop')

        global mainloop

        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

        bus = dbus.SystemBus()

        service_manager = get_service_manager(bus)
        ad_manager = get_ad_manager(bus)

        app = BLEApplication(bus)

        # Create advertisement
        test_advertisement = BLEAdvertisement(bus, 0)

        mainloop = GObject.MainLoop()
        # mainloop = GLib.MainLoop()

        # Register gatt services
        service_manager.RegisterApplication(app.get_path(), {},
                                            reply_handler=register_app_cb,
                                            error_handler=register_app_error_cb)

        # Register advertisement
        ad_manager.RegisterAdvertisement(test_advertisement.get_path(), {},
                                        reply_handler=register_ad_cb,
                                        error_handler=register_ad_error_cb)

    def start(self):
        BLINKER_LOG('Blinker BLE service init')
        

    def run(self):
        mainloop.run()

    def stop(self):
        self._isClosed = True

    def response(self, msg):
        if isDebugAll() is True:
            BLINKER_LOG('FFE1 Write: ' + msg)

        msg = json.dumps(msg)
        msg = msg + '\n'
        length = len(msg)
        a = []
        b = []
        for i in range(0, length):
            a.append(dbus.Byte(ord(msg[i])))
            b.append(msg[i])
        # if isDebugAll() is True:
        #     BLINKER_LOG(len(msg))
        #     BLINKER_LOG(a)
        #     BLINKER_LOG(b)

        msg = dbus.Array(a, signature=dbus.Signature('y'))
        bleProto.BLE_Response.PropertiesChanged(GATT_CHRC_IFACE, { 'Value': msg }, [])
        # if isDebugAll() is True:
        #     BLINKER_LOG('FFE1 Write: ' + str(msg))
