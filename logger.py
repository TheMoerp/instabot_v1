import coloredlogs
import logging


######################################################
FIELD_STYLES = {
    'levelname': {'bold': True, 'color': 'black'}
}
LEVEL_STYLES = {
    'critical': {'bold': True, 'color': 'red'},
    'error': {'bold': True, 'color': 'red'},
    'warning': {'color': 'red'},
    'info': {'bold': True, 'color': 'green'},
    'debug': {'color': 'white'}
}
LOG_FORMAT = '[%(levelname)s]: %(message)s'
LOG_PATH = 'Logs/CreateAccount.log'
NEWLINE_DEBUG = "           "
######################################################

logging.getLogger("urllib3.connectionpool").disabled = True

formatter = coloredlogs.ColoredFormatter(fmt=LOG_FORMAT, field_styles=FIELD_STYLES, level_styles=LEVEL_STYLES)
coloredlogs.install(fmt=LOG_FORMAT, level=logging.DEBUG, field_styles=FIELD_STYLES, level_styles=LEVEL_STYLES)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file = logging.FileHandler(LOG_PATH)
file.setLevel(logging.DEBUG)
file.setFormatter(formatter)
logger.addHandler(file)


def logEntry(level, message):
    if level == 'debug':
        logger.debug(message)
    elif level == 'info':
        logger.info(message)
    elif level == 'warning':
        logger.warning(message)
    elif level == 'error':
        logger.error(message)
    elif level == 'critival':
        logger.critical(message)

