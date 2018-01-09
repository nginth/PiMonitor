from configparser import ConfigParser
from clearblade.ClearBladeCore import System


def systemFromCfg(config):
    if 'system' not in config:
        raise KeyError('System key not found in clearblade.ini.')

    return System(config['system']['key'], config['system']['secret'])


def deviceFromCfg(config, system):
    if 'device' not in config:
        raise KeyError('Device key not found in clearblade.ini.')

    return system.Device(config['device']['name'], config['device']['active_key'])

config = ConfigParser()
config.read('clearblade.ini')
system = systemFromCfg(config)
device = deviceFromCfg(config, system)
print(device)
