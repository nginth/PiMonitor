from configparser import ConfigParser
from clearblade.ClearBladeCore import System
import time


def system_from_cfg(config):
    if 'system' not in config:
        raise KeyError('System key not found in clearblade.ini.')

    return System(config['system']['key'], config['system']['secret'])


def device_from_cfg(config, system):
    if 'device' not in config:
        raise KeyError('Device key not found in clearblade.ini.')

    return system.Device(config['device']['name'], config['device']['active_key'])


def messaging_from_cfg(config, system, device):
    return system.Messaging(device)


config = ConfigParser()
config.read('clearblade.ini')
system = system_from_cfg(config)
device = device_from_cfg(config, system)

msg_client = messaging_from_cfg(config, system, device)


def on_connect(client, userdata, flags, rc):
    client.publish('/rpi/cpu_usage', 'test')

msg_client.on_connect = on_connect
msg_client.connect()
time.sleep(10)
msg_client.disconnect()
