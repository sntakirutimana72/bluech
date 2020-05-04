from os import path
from configparser import ConfigParser
from utils.helpers.envs import exec_dir
from utils.loggers.ilogger import logging


def config(section: str, option: str = None):
    try:
        configs = ConfigParser()
        configs.read(path.join(exec_dir(), 'configurations.ini'))
        return configs.get(section, option) if option else configs.items(section)
    except Exception as e:
        logging(e)
