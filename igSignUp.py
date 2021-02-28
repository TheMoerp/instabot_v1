import requests
import json
import time
import random
import logger
import headerClass
import accountClass
from proxyCrawler import ProxyRequest
from igPwdEncrypt import encrypt_password

############################
keyId = 27
pubKey = "bca94a55472cbb9fdd02b0061e9463c5e9e291a2634015eb4dc5eb658d8d221d"
token = "pLEmAyYn7jrEkNhPXwahtlgdf3QBce6L"
igAjax = "0edc1000e5e7"
appId = "124024574287414"
deviceId = "2EFA9BF1062E477FB5378D8237117041"
clientId = "1CE070D14F" # woher kommt die?????????
############################


#### User Data ####
MAIL = "BesondersIntelligenterFlamingo@papierkorb.me"
USERNAME = "1chb1ne1nb0t138251231"
PASSWORD = "e1nzig@rt1gesP@5sw0rd"
FIRSTNAME = "IchBinKeinBot"
AGE = {
    'day': '6',
    'month': '9',
    'year': '1969'
} 
###################

nAcc = accountClass.Account(MAIL, FIRSTNAME, USERNAME, PASSWORD, AGE['day'], AGE['month'], AGE['year'])
h = headerClass.Headers('close', igAjax, token, appId)

spamCnt = 0
def RespChecker(resp):
    global spamCnt
    respJson = json.loads(resp.text)
    if respJson['status'] == 'ok':
        return True
    else:
        try:
            if respJson['spam']:
                spamCnt += 1
                logger.logEntry("error", "  Request marked as spam. Spam-detections: {}".format(spamCnt))
        except:
            logger.logEntry("error", "  Something went wrong.\n{}--- Response ---\n{}http-status-code: {}\n{}".format(
                logger.NEWLINE_ERROR, resp.status, logger.NEWLINE_ERROR, resp.text))
    return False


def EnterFunction(baseUrl, urlPath, h, body, proxy, confCheck):
    respCheck = False
    while not respCheck:
        time.sleep(random.uniform(1.0, 2.0))
        respTuple = ProxyRequest('post', baseUrl, urlPath, h, body, proxy)
        respCheck = RespChecker(respTuple[0])
    return respTuple


def SignUpNewAccount(nAcc, pubKey, keyId, deviceId, clientId, h):
    logger.logEntry("info", "   <---- STARTING TO CREATE AN INSTAGRAM ACCOUNT ---->\n")

    # UserData
    baseUrl = "https://www.instagram.com"
    urlPath = "/accounts/web_create_ajax/attempt/"
    encPassword = encrypt_password(keyId, pubKey, nAcc.password, version=10)
    body = "email={}&enc_password={}&username={}&firstname={}&seamless_login_enabled=1&opt_into_one_tap=false".format(
                  nAcc.mail, encPassword, nAcc.username, nAcc.name)

    respTuple = EnterFunction(baseUrl, urlPath, h, body, '', False)
    logger.logEntry("info", "   The user data has been entered successfully")

    time.sleep(random.uniform(1.0, 2.0))

    # Age
    baseUrl = "https://www.instagram.com"
    urlPath = "/web/consent/check_age_eligibility/"
    body = "day={}&month={}&year={}".format(nAcc.day, nAcc.month, nAcc.year)

    respTuple = EnterFunction(baseUrl, urlPath, h, body, respTuple[1], False)
    logger.logEntry("info", "   The age has been entered successfully")

    time.sleep(random.uniform(1.0, 2.0))

    # send mail
    baseUrl = "https://i.instagram.com"
    urlPath = "/api/v1/accounts/send_verify_email/"
    body = "device_id={}&email={}".format(deviceId, nAcc.mail)

    respTuple = EnterFunction(baseUrl, urlPath, h, body, respTuple[1], False)
    logger.logEntry("info", "   An confermation code has been send to the following mail address\n{}--Mail: {}".format(
                    logger.NEWLINE_INFO, nAcc.mail))
    
    time.sleep(random.uniform(1.0, 2.0))

    # check confermation code
    baseUrl = "https://i.instagram.com"
    urlPath = "/api/v1/accounts/check_confirmation_code/"
    respCheck = False
    while not respCheck:
        confCode = input("\nEnter the confirmation code: ")
        print("")
        body = "code={}&device_id={}&email={}".format(confCode, deviceId, nAcc.mail)
        time.sleep(random.uniform(1.0, 2.0))
        respTuple = ProxyRequest('post', baseUrl, urlPath, h, body, respTuple[1])
        respCheck = RespChecker(respTuple[0])

    respJson = json.loads(respTuple[0].text)
    signUpCode = respJson['signup_code']
    logger.logEntry("info", "   The confermation code has been accepted")
    time.sleep(random.uniform(2.0, 3.0))

    # create account
    baseUrl = "https://www.instagram.com"
    urlPath = "/accounts/web_create_ajax/"
    encPassword = encrypt_password(keyId, pubKey, nAcc.password, version=10)
    body = "email={}&enc_password={}&username={}&first_name={}&month={}&day={}&year={}&client_id={}&searmless_login_enabled=1&tos_version=eu&force_sign_up_code={}".format(
            nAcc.mail, encPassword, nAcc.username, nAcc.name, nAcc.month, nAcc.day, nAcc.year, clientId, signUpCode)
    
    respTuple = EnterFunction(baseUrl, urlPath, h, body, respTuple[1], False)
    logger.logEntry("error", "  Something went wrong.\n{}--- Response ---\n{}http-status-code: {}\n{}".format(
                logger.NEWLINE_ERROR, respTuple[0].status, logger.NEWLINE_ERROR, respTuple[0].text))
    print("")
    logger.logEntry("critical", "<---- QUITING PROGRAM ---->")


SignUpNewAccount(nAcc, pubKey, keyId, deviceId, clientId, h)




# def EnterUserData(nAcc, h, keyId, pubKey):
#     baseUrl = "https://www.instagram.com"
#     urlPath = "/accounts/web_create_ajax/attempt/"
#     respCheck = False

#     while not respCheck:
#         encPassword = encrypt_password(keyId, pubKey, nAcc.password, version=10)
#         body = "email={}&enc_password={}&username={}&firstname={}&seamless_login_enabled=1&opt_into_one_tap=false".format(
#                 nAcc.mail, encPassword, nAcc.username, nAcc.name)

#         respTuple = ProxyRequest('post', baseUrl, urlPath, h, body, '')
#         respCheck = RespChecker(respTuple[0])

#     logger.logEntry("info", "   The user data has been entered successfully")
#     return respTuple[1]


# def EnterAge(nAcc, proxy):
#     baseUrl = "https://www.instagram.com"
#     urlPath = "/web/consent/check_age_eligibility/"
#     respCheck = False

#     while not respCheck:
#         body = "day={}&month={}&year={}".format(nAcc.day, nAcc.month, nAcc.year)

#         respTuple = ProxyRequest('post', baseUrl, urlPath, h, body, proxy)
#         respCheck = RespChecker(respTuple[0])

    









