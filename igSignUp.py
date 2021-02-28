import requests
import json
import time
import logging
import random
from proxyCrawler import proxy_request
from igPwdEncrypt import encrypt_password
import logger

############################
keyId = 27
pubKey = "bca94a55472cbb9fdd02b0061e9463c5e9e291a2634015eb4dc5eb658d8d221d"
token = "pLEmAyYn7jrEkNhPXwahtlgdf3QBce6L"
igAjax = "0edc1000e5e7"
appId = "124024574287414"
deviceId = "2EFA9BF1062E477FB5378D8237117041"
clientId = "1nx0f6mnkzzwl1uahxu6uvmcvov474nr1ytlsk11rrwhxl6smora" # woher kommt die?????????
############################

#### URL Path ####
USERDATA_PATH = "/accounts/web_create_ajax/attempt/"
AGE_PATH = "/web/consent/check_age_eligibility/"
SEND_PATH = "/api/v1/accounts/send_verify_email/"
CONF_PATH = "/api/v1/accounts/check_confirmation_code/"

SIGNON_PATH = "/accounts/web_create_ajax/"
##################

#### User Data ####
MAIL = "istaisteinhurensohn@oida.icu"
USERNAME = "1chb1ne1nb0t138251231"
PASSWORD = "e1nzig@rt1gesP@5sw0rd"
FIRSTNAME = "IchBinKeinBot"
AGE = {
    'day': '6',
    'month': '9',
    'year': '1969'
}
###################



BASE_URL = "https://www.instagram.com"


def BuildUserDataBody(mail, keyId, pubKey, username):
    encPwd = encrypt_password(keyId, pubKey, PASSWORD, version=10)
    body = "email={}&enc_password={}&username={}&firstname={}&seamless_login_enabled=1&opt_into_one_tap=false".format(mail, encPwd, username, FIRSTNAME)
    return body


def BuildAgeBody():
    body = "day={}&month={}&year={}".format(AGE['day'], AGE['month'], AGE['year'])
    return body

def BuildSendMailBody(mail, deviceId):
    body = "device_id={}&email={}".format(deviceId, mail)
    return body


def BuildConfermationBody(mail, deviceId, confCode):
    body = "code={}&device_id={}&email={}".format(confCode, deviceId, mail)
    return body

def BuildCreateBody(keyId, pubKey, mail, password, username, clientId, signUpCode):
    encPwd = encrypt_password(keyId, pubKey, PASSWORD, version=10)
    body = "email={}&enc_password={}&username={}&first_name={}&month={}&day={}&year={}&client_id={}&searmless_login_enabled=1&tos_version=eu&force_sign_up_code={}".format(
            mail, encPwd, username, FIRSTNAME, AGE['month'], AGE['day'], AGE['year'], clientId, signUpCode)
    return body


def PostRequest(baseUrl, urlCmdPart, token, igAjax, body, appId, workingProxy):    
    url = "{}{}".format(baseUrl, urlCmdPart)
    headers = {
        "Connection": "close",
        "X-Instagram-AJAX": igAjax,
        "Content-Type": "application/x-www-form-urlencoded",
        "X-CSRFToken": token,
        "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
        "X-IG-App-ID": appId
    }

    respTuple = proxy_request('post', url, headers, body, workingProxy)
    resp = respTuple[0]
    proxy = respTuple[1]

    logHeaders = "Connection: close\n{}Content-Type: application/x-www-form-urlencoded\n{}X-Instagram-AJAX: {}\n{}X-CSRFToken: {}\n{}X-IG-APP-ID: {}".format(
                  logger.NEWLINE_DEBUG, logger.NEWLINE_DEBUG,  igAjax, logger.NEWLINE_DEBUG, token, logger.NEWLINE_DEBUG, appId)
    logger.logEntry("debug", "  --- Request ---\n{}URL: {}\n{}Methode: post\n\n{}--- Headers ---\n{}{}\n{}--- Body ---\n\n{}{}".format(
                  logger.NEWLINE_DEBUG, url, logger.NEWLINE_DEBUG, logger.NEWLINE_DEBUG, logger.NEWLINE_DEBUG, logHeaders,logger.NEWLINE_DEBUG, logger.NEWLINE_DEBUG, body))
    logger.logEntry("debug", "--- Response ---\n{}{}".format(logger.NEWLINE_DEBUG, resp.text))

    jsonObject = json.loads(resp.text)
    status = jsonObject["status"]
    signUpCode = ""
    try:
        signUpCode = jsonObject["signup_code"]
        logger.logEntry("info", "   The signupcode is: {}".format(signUpCode))
    except:
        pass
    
    return (status, proxy, signUpCode)


def SpamDetectionCheck(status, spamDedCnt):
    if status == "fail":
        spamDedCnt += 1
        logger.logEntry("error", "  Request marked as spam. Spam-detections: {}".format(spamDedCnt))
    return spamDedCnt


def CreateAccountOnIG():
    logger.logEntry("info", "   <---- STARTING TO CREATE AN INSTAGRAM ACCOUNT ---->\n")
    status = ''
    spamDedCnt = 0

    while status != "ok":
        userDataBody = BuildUserDataBody(MAIL, keyId, pubKey, USERNAME)
        statusTuple = PostRequest(BASE_URL, USERDATA_PATH, token, igAjax, userDataBody, appId, "")
        status = statusTuple[0]
        proxy = statusTuple[1]
        spamDedCnt = SpamDetectionCheck(status, spamDedCnt)

    logger.logEntry("info", "   The user data has been entered successfully")
    status = ''
    time.sleep(random.uniform(1.0, 2.0))

    while status != "ok":
        ageBody = BuildAgeBody()
        statusTuple = PostRequest(BASE_URL, AGE_PATH, token, igAjax, ageBody, appId, proxy)
        status = statusTuple[0]
        proxy = statusTuple[1]
        spamDedCnt = SpamDetectionCheck(status, spamDedCnt)

    logger.logEntry("info", "   The age has been entered successfully")
    status = ''
    time.sleep(random.uniform(1.0, 2.0))

    while status != "ok":
        baseUrl = "https://i.instagram.com"
        mailBody = BuildSendMailBody(MAIL, deviceId)
        statusTuple = PostRequest(baseUrl, SEND_PATH, token, igAjax, mailBody, appId, proxy)
        status = statusTuple[0]
        proxy = statusTuple[1]
        spamDedCnt = SpamDetectionCheck(status, spamDedCnt)

    logger.logEntry("info", "   An confermation code has been send to the following mail address\n{}--Mail: {}".format(logger.NEWLINE_INFO, MAIL))
    status = ''

    while status != "ok":
        confCode = input("\nEnter the confirmation code: ")
        print("")
        time.sleep(random.uniform(1.0, 2.0))
        baseUrl = "https://i.instagram.com"
        confBody = BuildConfermationBody(MAIL, deviceId, confCode)
        statusTuple = PostRequest(baseUrl, CONF_PATH, token, igAjax, confBody, appId, proxy)
        status = statusTuple[0]
        proxy = statusTuple[1]
        signUpCode = statusTuple[2]
        spamDedCnt = SpamDetectionCheck(status, spamDedCnt)
    
    logger.logEntry("info", "   The confermation code has been accepted")
    
    status = ''
    time.sleep(random.uniform(2.0, 3.0))

    while status != "ok":
        signOnBody = BuildCreateBody(keyId, pubKey, MAIL, PASSWORD, USERNAME, clientId, signUpCode)
        statusTuple = PostRequest(BASE_URL, SIGNON_PATH, token, igAjax, signOnBody, appId, proxy)
        status = statusTuple[0]
        proxy = statusTuple[1]
        spamDedCnt = SpamDetectionCheck(status, spamDedCnt)
    
    logger.logEntry("info", "   The account has been signed up successfully\n{}Try to login with the following credentials\n{}--Username: {}\n{}--Password: {}\n".format(
                    logger.NEWLINE_INFO, logger.NEWLINE_INFO, USERNAME, logger.NEWLINE_INFO, PASSWORD))
    status = ''
    time.sleep(random.uniform(1.0, 2.0))






    logger.logEntry("info", "   <---- QUITING PROGRAM ---->")
    exit()


CreateAccountOnIG()