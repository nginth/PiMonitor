import os
from unittest import TestCase, mock
from configparser import ConfigParser
from monitor.monitor import Monitor

TEST_CONFIG = 'test_config.ini'


class TestMonitor(TestCase):

    def setUp(self):
        config = ConfigParser()
        with open(TEST_CONFIG, 'w') as f:
            config.write(f)

    def tearDown(self):
        os.remove(TEST_CONFIG)

    def test_new_monitor_system_not_found(self):
        config = ConfigParser()
        config['device'] = {'name': 'testname', 'active_key': 'testactivekey'}
        config['messaging'] = {'channel': '/test/channel'}
        with open(TEST_CONFIG, 'w') as f:
            config.write(f)

        with mock.patch('clearblade.ClearBladeCore.System', MockSystem) as m:
            with self.assertRaises(KeyError):
                monitor = Monitor(TEST_CONFIG)

    def test_new_monitor_device_not_found(self):
        config = ConfigParser()
        config['system'] = {'key': 'testkey', 'secret': 'testsecret'}
        config['messaging'] = {'channel': '/test/channel'}
        with open(TEST_CONFIG, 'w') as f:
            config.write(f)

        with mock.patch('clearblade.ClearBladeCore.System', MockSystem) as m:
            with self.assertRaises(KeyError):
                monitor = Monitor(TEST_CONFIG)

    def test_new_monitor_messaging_not_found(self):
        config = ConfigParser()
        config['system'] = {'key': 'testkey', 'secret': 'testsecret'}
        config['device'] = {'name': 'testname', 'active_key': 'testactivekey'}

        with mock.patch('clearblade.ClearBladeCore.System', MockSystem) as m:
            with self.assertRaises(KeyError):
                monitor = Monitor(TEST_CONFIG)


class MockSystem:

    def __init__(self, *args):
        pass

    def Device(self, *args):
        pass

    def Messaging(self, *args):
        pass
