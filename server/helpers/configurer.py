from os import path
from helpers.envs import exec_dir
from helpers.loggers import logging
from configparser import ConfigParser


def config(section: str, option: str = None):
    try:
        configs = ConfigParser()
        configs.read(path.join(exec_dir(), 'configurations.ini'))
        return configs.get(section, option) if option else configs.items(section)
    except Exception as e:
        logging(e)
