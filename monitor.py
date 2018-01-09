from configparser import ConfigParser
from clearblade.ClearBladeCore import System
from psutil import cpu_percent
import time


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

    msg_client = system.Messaging(device)

    def on_connect(client, userdata, flags, rc):
        client.publish(config['messaging']['channel'], cpu_utilization())

    msg_client.on_connect = on_connect

    return msg_client


config = ConfigParser()
config.read('clearblade.ini')
system = system_from_cfg(config)
device = device_from_cfg(config, system)

msg_client = messaging_from_cfg(config, system, device)

msg_client.connect()
time.sleep(10)
msg_client.disconnect()
