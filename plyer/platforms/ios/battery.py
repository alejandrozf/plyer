'''
Module of iOS API for plyer.battery.
'''

from pyobjus import autoclass  # pylint: disable=import-error
from pyobjus.dylib_manager import load_framework  # pylint:disable=import-error
from plyer.facades import Battery

load_framework('/System/Library/Frameworks/UIKit.framework')
UIDEVICE = autoclass('UIDevice')


class IOSBattery(Battery):
    '''
    Implementation of iOS battery API.
    '''

    def __init__(self):
        super(IOSBattery, self).__init__()
        self.device = UIDEVICE.currentDevice()

    def _get_state(self):
        status = {"isCharging": None, "percentage": None}

        if not self.device.batteryMonitoringEnabled:
            self.device.setBatteryMonitoringEnabled_(True)

        if self.device.batteryState == 0:
            is_charging = None
        elif self.device.batteryState == 2:
            is_charging = True
        else:
            is_charging = False

        percentage = self.device.batteryLevel * 100.

        status['isCharging'] = is_charging
        status['percentage'] = percentage

        return status


def instance():
    '''
    Instance for facade proxy.
    '''
    return IOSBattery()
