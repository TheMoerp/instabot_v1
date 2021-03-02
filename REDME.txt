--- Python Dependencies ---

> pip install pycryptodomex
> pip install PyNaCl
> pip install beautifulsoup4
> pip install coloredlogs
> pip install requests
> pip install pyyaml


--- configs ---

account-data -> mail, username, password, birthday
max_same_proxy -> if the same proxy is choosen for max_same_proxy the program quits
new_proxy_timeout -> timeout time for new proxy in seconds
working_proxy_timeout -> timeout time for previous proxy in seconds
working_proxy_retrys -> trying to reach a previous proxy for working_proxy_retrys times
max_same_proxy -> changing proxy after max_same_proxy spam detections
max_session_proxy -> initiating new session after max_session_proxy fails
log-colors -> display color of log-levels
debug-log-level -> 1: successes & errors
                -> 2: 1 & proxy connection infos
                -> 3: 2 & sent requests & received replies
backup-logs -> how many backups to save before overwriting them

--- usage ---


run:
> python3 igSignup

logs:
1. change LOG_PATH in logger.py to a folder of your choise
2. view the latest log type:
> Get-Content isSignUp.log
