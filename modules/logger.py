import coloredlogs
import logging
import logging.handlers
import os
import config as c

######################################################
FIELD_STYLES = {
    'levelname': {'bold': True, 'color': 'black'}
}
LEVEL_STYLES = {
    'critical': {'bold': True, 'color': c.CRITICAL_COLOR},
    'error': {'bold': True, 'color': c.ERROR_COLOR},
    'warning': {'color': c.WARNING_COLOR},
    'info': {'bold': True, 'color': c.INFO_COLOR},
    'debug': {'color': c.DEBUG_COLOR}
}
LOG_FORMAT = '[%(levelname)s]: %(message)s'
LOG_PATH = r'C:\Users\matth\Documents\Workspace\Instagram_Bot\Logs/igSignUp.log'
NEWLINE_DEBUG = "            "
NEWLINE_ERROR = "            "
NEWLINE_INFO = "            "
######################################################


rollOver = os.path.isfile(LOG_PATH)
file = logging.handlers.RotatingFileHandler(LOG_PATH, mode='a', backupCount=c.BACKUP_LOGS)
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
    elif level == 'critical':
        logger.critical(message)

