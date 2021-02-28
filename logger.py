import coloredlogs
import logging
import logging.handlers
import os


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
LOG_PATH = 'Logs/igSignUp.log'
BACKUP_COUNT = 2
NEWLINE_DEBUG = "           "
NEWLINE_ERROR = "           "
NEWLINE_INFO = "           "
######################################################

rollOver = os.path.isfile(LOG_PATH)
file = logging.handlers.RotatingFileHandler(LOG_PATH, mode='a', backupCount=BACKUP_COUNT)
if rollOver:
    file.doRollover()

logging.getLogger("urllib3.connectionpool").disabled = True

formatter = coloredlogs.ColoredFormatter(fmt=LOG_FORMAT, field_styles=FIELD_STYLES, level_styles=LEVEL_STYLES)
coloredlogs.install(fmt=LOG_FORMAT, level=logging.DEBUG, field_styles=FIELD_STYLES, level_styles=LEVEL_STYLES)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
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

