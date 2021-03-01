import yaml

filename = 'config.yml'
with open(filename) as f:
    configDict = yaml.load(f, Loader=yaml.FullLoader)

accConf = configDict['account-data']
proxyConf = configDict['proxy-config']
logConf = configDict['log-colors']
debuglvl = configDict['debug-log-level']

# debug config
DEBUG1 = False
DEBUG2 = False
DEBUG3 = False
if debuglvl == 1:
    DEBUG1 = True
elif debuglvl == 2:
    DEBUG2 = True
    DEBUG1 = True
elif debuglvl == 3:
    DEBUG3 = True
    DEBUG2 = True
    DEBUG1 = True


# Account config
MAIL = accConf['mail']
USERNAME = accConf['username']
NAME = accConf['name']
PASSWORD = accConf['password']
bDay = accConf['birthday'].split('.')
DAY = bDay[0]
MONTH = bDay[1]
YEAR = bDay[2]

# Proxy config
MAX_SAME_PROXY = proxyConf['max_same_proxy']
NEW_PROXY_TIMEOUT = proxyConf['new_proxy_timeout']
WORKING_PROXY_TIMEOUT = proxyConf['working_proxy_timeout']
WORKING_PROXY_RETRYS = proxyConf['working_proxy_retrys']
MAX_PROXY_SPAM = proxyConf['max_proxy_spam']

# log colors
DEBUG_COLOR = logConf['debug']
INFO_COLOR = logConf['info']
WARNING_COLOR = logConf['warning']
ERROR_COLOR = logConf['error']
CRITICAL_COLOR = logConf['critical']
