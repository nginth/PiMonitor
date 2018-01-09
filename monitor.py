import time
from configparser import ConfigParser
from clearblade.ClearBladeCore import System
from psutil import cpu_percent
from exiter import Exiter


def system_from_cfg(config):
    if 'system' not in config:
        raise KeyError('System key not found in clearblade.ini.')

    return System(config['system']['key'], config['system']['secret'])


def device_from_cfg(config, system):
    if 'device' not in config:
        raise KeyError('Device key not found in clearblade.ini.')

    return system.Device(config['device']['name'], config['device']['active_key'])


def cpu_utilization():
    cpu_percent_strs = [str(percent) for percent in cpu_percent(percpu=True)]
    return ','.join(cpu_percent_strs)


def messaging_from_cfg(config, system, device):
    if 'messaging' not in config:
        raise KeyError('Messaging key not found in clearblade.ini.')

    return system.Messaging(device)

config = ConfigParser()
config.read('clearblade.ini')
system = system_from_cfg(config)
device = device_from_cfg(config, system)
msg_client = messaging_from_cfg(config, system, device)
delay = int(config['messaging']['delay']) if 'delay' in config[
    'messaging'] else 5

msg_client.connect()

exiter = Exiter()
while not exiter.should_exit:
    msg_client.publish(config['messaging']['channel'], cpu_utilization())
    time.sleep(delay)

msg_client.disconnect()
