# from testconfig import config
import os
import unittest

from awlib.androiddevice import AndroidDevice
from awlib.adb import Adb
from awlib.awserial import AWSerial
from awlib.log import Logger

from caseproperty import cproperty as CaseConfig
from testconfig import config as TopoConfig

from awlib.cylix import USBSwitch1in8out
from MSSwitcher import DevMSSwitcher
from awlib.cylix import USBSwitch8in8out



class CylixUSB8in8outUtil(unittest.TestCase):
    PRE_INSTALL_APK = []
    PRE_INSTALL_JAR = []
    PRE_INSTALL_RES = []

    def __init__(self, *args, **kargs):
        super(CylixUSB8in8outUtil, self).__init__(*args, **kargs)
        self.logger = Logger(self.__class__.__name__)

        self.config = CaseConfig
        self.topoconfig = TopoConfig

        self.ats_home = TopoConfig['Topo']['ats_home']

        self.dut_serial_name = TopoConfig['Device']['dut_serial_name']
        self.dut_serial = None

        self.cylix_serial_name = TopoConfig['Topo']['cylix_serial_name']
        self.cylix_line = int(TopoConfig['Device']['cylix_line'])
        self.cylix = None

        self.serial_log_filename = os.path.join(
            str(TopoConfig['Device']['log_path']),
            '%s_%s.log' % (
                self.__class__.__name__,
                self.dut_serial_name.replace(os.sep, ''))
            )

    def setUp(self):
        self.logger.info('Testcase setup.')
        self.dut_serial = AWSerial(
            self.dut_serial_name,
            filename=self.serial_log_filename,
            )


        self.switch = USBSwitch8in8out(
            self.cylix_serial_name)
        self.switch.switch2usb(self.cylix_line)

        self.device = AndroidDevice(adb=Adb(
            device_name=str(TopoConfig['Device']['name'])))
        self.device.adb.wait_for_device()

        # install apk
        for path, package in self.PRE_INSTALL_APK:
            self.device.adb.install(os.path.join(self.ats_home, path), 
                                    reinstall=True)
            assert self.device.adb.get_output().count("Success") > 0, \
                "Fail to install apk %s" % path

        # push java jar file
        for jar in self.PRE_INSTALL_JAR:
            self.device.adb.push(os.path.join(self.ats_home, jar), 
                                 "/data/local/tmp/")

        for local, remote_path, remote_file in self.PRE_INSTALL_RES:
            self.device.adb.push(os.path.join(self.ats_home, local),
                                 remote_path + remote_file)

    def tearDown(self):
        self.logger.info('Testcase teardown.')
        self.dut_serial.close()
        self.switch.switch2usb(self.cylix_line)
        self.device.adb.wait_for_device()
        self.atTestCaseExit()
        for path, package in self.PRE_INSTALL_APK:
            self.device.adb.uninstall(package)
        if len(self.PRE_INSTALL_JAR) > 0:
            self.device.adb.shell("rm /data/local/tmp/*.jar")
        for local, remote_path, remote_file in self.PRE_INSTALL_RES:
            self.device.adb.shell("rm %s%s" % (remote_path, remote_file))
        self.switch.switch2power(self.cylix_line)
        
    def atTestCaseExit(self):
        pass

class CylixUSB8in8out1in8outUtil(unittest.TestCase):
    """
    The different between CylixUSB8in8out1in8outUtil and CylixUSB8in8outUtil
    is that the Topology of CylixUSB8in8out1in8outUtil includes both
    8in8out and 1in8out switcher. But user will not use OTG
    function, DUT only acts as 'usb device'
    """
    PRE_INSTALL_APK = []
    PRE_INSTALL_JAR = []
    PRE_INSTALL_RES = []

    def __init__(self, *args, **kargs):
        super(CylixUSB8in8out1in8outUtil, self).__init__(*args, **kargs)
        self.logger = Logger(self.__class__.__name__)

        self.config = CaseConfig
        self.topoconfig = TopoConfig

        self.ats_home = TopoConfig['Topo']['ats_home']

        self.dut_serial_name = TopoConfig['Device']['dut_serial_name']
        self.dut_serial = None

        self.cylix_serial_name = TopoConfig['Topo']['cylix_serial_name']
        self.cylix_line = int(TopoConfig['Device']['cylix_line'])
        self.cylix = None

        if TopoConfig['Topo'].has_key('1in8out_slot'):
            self.cylix_1in8out_slot = str(TopoConfig['Topo']['1in8out_slot'])
        else:
            self.cylix_1in8out_slot = 'U27'

        self.serial_log_filename = os.path.join(
            str(TopoConfig['Device']['log_path']),
            '%s_%s.log' % (
                self.__class__.__name__,
                self.dut_serial_name.replace(os.sep, ''))
            )

    def setUp(self):
        self.logger.info('Testcase setup.')
        self.dut_serial = AWSerial(
            self.dut_serial_name,
            filename=self.serial_log_filename,
            )


        self.switch = USBSwitch8in8out(
            self.cylix_serial_name)
        self.ms_switch = USBSwitch1in8out(
            self.cylix_serial_name,
            self.cylix_1in8out_slot)
        # initialize the 1in8out switcher, so that
        # user only need to care about 8in8out switcher
        # step 1: high voltage for OTG line
        # step 2: disconnect all line for 1in8out
        # step 3: connect line 8 to provide power
        # step 4: connect line 1 for PC/Power
        high_volt = '1'
        self.switch.ctr_volt(self.cylix_line, high_volt)
        for i in range(8):
            self.ms_switch.disconnect(i+1)
        self.ms_switch.connect(8)
        self.ms_switch.connect(1)
        self.switch.switch2usb(self.cylix_line)

        self.device = AndroidDevice(adb=Adb(
            device_name=str(TopoConfig['Device']['name'])))
        self.device.adb.wait_for_device()

        # install apk
        for path, package in self.PRE_INSTALL_APK:
            self.device.adb.install(os.path.join(self.ats_home, path), 
                                    reinstall=True)
            assert self.device.adb.get_output().count("Success") > 0, \
                "Fail to install apk %s" % path

        # push java jar file
        for jar in self.PRE_INSTALL_JAR:
            self.device.adb.push(os.path.join(self.ats_home, jar), 
                                 "/data/local/tmp/")

        for local, remote_path, remote_file in self.PRE_INSTALL_RES:
            self.device.adb.push(os.path.join(self.ats_home, local),
                                 remote_path + remote_file)

    def setUpWithoutConnectToUSB(self):
        self.logger.info('Testcase setup.')
        self.dut_serial = AWSerial(
            self.dut_serial_name,
            filename=self.serial_log_filename,
            )


        self.switch = USBSwitch8in8out(
            self.cylix_serial_name)
        self.ms_switch = USBSwitch1in8out(
            self.cylix_serial_name,
            self.cylix_1in8out_slot)
        # initialize the 1in8out switcher, so that
        # user only need to care about 8in8out switcher
        # step 1: high voltage for OTG line
        # step 2: disconnect all line for 1in8out
        # step 3: connect line 8 to provide power
        # step 4: connect line 1 for PC/Power
        high_volt = '1'
        self.switch.ctr_volt(self.cylix_line, high_volt)
        for i in range(8):
            self.ms_switch.disconnect(i+1)
        self.ms_switch.connect(8)
        self.ms_switch.connect(1)
        self.switch.switch2usb(self.cylix_line)

        self.device = AndroidDevice(adb=Adb(
            device_name=str(TopoConfig['Device']['name'])))

    def tearDown(self):
        self.logger.info('Testcase teardown.')
        self.dut_serial.close()
        self.switch.switch2usb(self.cylix_line)
        self.device.adb.wait_for_device()
        self.atTestCaseExit()
        for path, package in self.PRE_INSTALL_APK:
            self.device.adb.uninstall(package)
        if len(self.PRE_INSTALL_JAR) > 0:
            self.device.adb.shell("rm /data/local/tmp/*.jar")
        for local, remote_path, remote_file in self.PRE_INSTALL_RES:
            self.device.adb.shell("rm %s%s" % (remote_path, remote_file))
        self.switch.switch2power(self.cylix_line)
        
    def atTestCaseExit(self):
        pass


class CylixUSB8in8out1in8outOTGUtil(unittest.TestCase):
    """
    The different between CylixUSB8in8out1in8outOTGUtil and 
    CylixUSB8in8out1in8outUtil is that the Topology of 
    CylixUSB8in8out1in8outOTGUtil includes both
    8in8out and 1in8out switcher. And user will use OTG function.
    """
    PRE_INSTALL_APK = []
    PRE_INSTALL_JAR = []
    PRE_INSTALL_RES = []

    def __init__(self, *args, **kargs):
        super(CylixUSB8in8out1in8outOTGUtil, self).__init__(*args, **kargs)
        self.logger = Logger(self.__class__.__name__)

        self.config = CaseConfig
        self.topoconfig = TopoConfig

        self.ats_home = TopoConfig['Topo']['ats_home']

        self.dut_serial_name = TopoConfig['Device']['dut_serial_name']
        self.dut_serial = None

        self.cylix_serial_name = TopoConfig['Topo']['cylix_serial_name']
        self.cylix_line = int(TopoConfig['Device']['cylix_line'])
        self.cylix = None

        if TopoConfig['Topo'].has_key('1in8out_slot'):
            self.cylix_1in8out_slot = str(TopoConfig['Topo']['1in8out_slot'])
        else:
            self.cylix_1in8out_slot = 'U27'

        self.serial_log_filename = os.path.join(
            str(TopoConfig['Device']['log_path']),
            '%s_%s.log' % (
                self.__class__.__name__,
                self.dut_serial_name.replace(os.sep, ''))
            )

    def setUp(self):
        self.logger.info('Testcase setup.')
        self.dut_serial = AWSerial(
            self.dut_serial_name,
            filename=self.serial_log_filename,
            )

        self.switch = DevMSSwitcher(
            self.cylix_serial_name,
            u_slot=self.cylix_1in8out_slot)
        self.switch.switch2SlaveUsb(self.cylix_line)

        self.device = AndroidDevice(adb=Adb(
            device_name=str(TopoConfig['Device']['name'])))
        self.device.adb.wait_for_device()

        # install apk
        for path, package in self.PRE_INSTALL_APK:
            self.device.adb.install(os.path.join(self.ats_home, path), 
                                    reinstall=True)
            assert self.device.adb.get_output().count("Success") > 0, \
                "Fail to install apk %s" % path

        # push java jar file
        for jar in self.PRE_INSTALL_JAR:
            self.device.adb.push(os.path.join(self.ats_home, jar), 
                                 "/data/local/tmp/")

        for local, remote_path, remote_file in self.PRE_INSTALL_RES:
            self.device.adb.push(os.path.join(self.ats_home, local),
                                 remote_path + remote_file)

    def tearDown(self):
        self.logger.info('Testcase teardown.')
        self.dut_serial.close()
        self.switch.switch2SlaveUsb(self.cylix_line)
        self.device.adb.wait_for_device()
        self.atTestCaseExit()
        for path, package in self.PRE_INSTALL_APK:
            self.device.adb.uninstall(package)
        if len(self.PRE_INSTALL_JAR) > 0:
            self.device.adb.shell("rm /data/local/tmp/*.jar")
        for local, remote_path, remote_file in self.PRE_INSTALL_RES:
            self.device.adb.shell("rm %s%s" % (remote_path, remote_file))
        self.switch.switch2SlavePower(self.cylix_line)

    def atTestCaseExit(self):
        pass

# CylixUSB8in8outUtil: only 8in8out in topo
# CylixUSB8in8out1in8outUtil: one 8in8out + one 1in8out ,but without OTG 
#                             function
# CylixUSB8in8out1in8outOTGUtil: one 8in8out + one 1in8out, 1in8out has
#                                OTG function
if TopoConfig['Topo']['topo_name'] == "CylixUSB8in8outUtil":
    CylixUtilTestCase = CylixUSB8in8outUtil
elif TopoConfig['Topo']['topo_name'] == "CylixUSB8in8out1in8outUtil":
    CylixUtilTestCase = CylixUSB8in8out1in8outUtil
elif TopoConfig['Topo']['topo_name'] == "CylixUSB8in8out1in8outOTGUtil":
    CylixUtilTestCase = CylixUSB8in8out1in8outOTGUtil
else:
    raise Exception("Not found that topo named:%s" %
                    TopoConfig['Topo']['topo_name'])