from configparser import ConfigParser
from clearblade.ClearBladeCore import System


def systemFromCfg(filename):
    config = ConfigParser()
    config.read(filename)
    if 'system' not in config:
        raise KeyError('System key not found in clearblade.ini.')

    return System(config['system']['key'], config['system']['secret'])

system = systemFromCfg('clearblade.ini')
