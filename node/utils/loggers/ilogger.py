from os import path
from datetime import datetime
from utils.helpers.envs import res_dir
from logging import basicConfig, DEBUG, getLogger

logger = None


def __setup__():
    global logger

    logfile_name = datetime.now().strftime('%B-%Y')
    basicConfig(filename=path.join(res_dir(), 'logs', logfile_name + '.log'),
                format='%(asctime)s :: %(levelname)s :: %(name)s :: %(message)s')
    logger = getLogger('syai-blue-chat')
    logger.setLevel(DEBUG)


def logging(message, what_: str = 'e'):
    if what_ == 'i':
        logger.info(repr(message))
    elif what_ == 'c':
        logger.critical(repr(message))
    elif what_ == 'w':
        logger.warning(repr(message))
    else:
        logger.error(repr(message))


__setup__()
