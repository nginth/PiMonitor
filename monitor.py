import time
from configparser import ConfigParser
from clearblade.ClearBladeCore import System
from psutil import cpu_percent
from exiter import Exiter


class Monitor:

    def __init__(self, filename='clearblade.ini'):
        self.config = ConfigParser()
        self.config.read(filename)
        self.system = self._system_from_cfg()
        self.device = self._device_from_cfg()
        self.msg_client = self._messaging_from_cfg()
        self.channel = self.config['messaging']['channel']

    def _system_from_cfg(self):
        if 'system' not in self.config:
            raise KeyError('System key not found in clearblade.ini.')

        return System(self.config['system']['key'], self.config['system']['secret'])

    def _device_from_cfg(self):
        if 'device' not in self.config:
            raise KeyError('Device key not found in clearblade.ini.')

        return self.system.Device(self.config['device']['name'], self.config['device']['active_key'])

    def _messaging_from_cfg(self):
        if 'messaging' not in self.config:
            raise KeyError('Messaging key not found in clearblade.ini.')

        return self.system.Messaging(self.device)

    def publish(self, message):
        self.msg_client.publish(self.channel, message)

    def connect(self):
        self.msg_client.connect()

    def disconnect(self):
        self.msg_client.disconnect()


def cpu_utilization():
    cpu_percent_strs = [str(percent) for percent in cpu_percent(percpu=True)]
    return ','.join(cpu_percent_strs)


if __name__ == '__main__':
    monitor = Monitor()

    monitor.connect()

    exiter = Exiter()
    while not exiter.should_exit:
        monitor.publish(cpu_utilization())
        time.sleep(5)

    monitor.disconnect()
