from __future__ import absolute_import, print_function, unicode_literals

import os
import dbus
import dbus.mainloop.glib

import array

try:
    from gi.repository import GObject
except ImportError:
    import gobject as GObject

from bluez_components import *
from random import randint

# mainloop = None

import sys
import re
from optparse import OptionParser, make_option
import bluezutils


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

    def ReadValue(self, options):
        print('Read: ' + str(self.value))

        option_list = [
                        make_option("-i", "--device", action="store",
                                type="string", dest="dev_id"),
                        ]
        parser = OptionParser(option_list=option_list)
        print(parser)

        return self.value

    def WriteValue(self, value, options):
        print('Write: ' + str(value))

        self.PropertiesChanged(GATT_CHRC_IFACE, { 'Value': value }, [])

    def StartNotify(self):
        if self.notifying:
            print('Already notifying, nothing to do')
            return
        else:
            print('Already notifying!')
        self.notifying = True

    def StopNotify(self):
        if not self.notifying:
            print('Not notifying, nothing to do')
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
    print('Advertisement registered')


def register_ad_error_cb(error):
    """
    Callback if registering advertisement failed
    """
    print('Failed to register advertisement: ' + str(error))
    mainloop.quit()


def register_app_cb():
    """
    Callback if registering GATT application was successful
    """
    print('GATT application registered')


def register_app_error_cb(error):
    """
    Callback if registering GATT application failed.
    """
    print('Failed to register application: ' + str(error))
    mainloop.quit()


def main():
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
        print ("exit")


if __name__ == '__main__':
    main()