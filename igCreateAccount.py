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
token = "JKoMWa3poBvcADgpTqpoYkcXJ6cv7Zyu"
igAjax = "0edc1000e5e7"
appId = "936619743392459"
deviceId = "6DDFB88795C3-445798DA5FB778C8C94C" # new
############################


#### URL Path ####
USERDATA_PATH = "/accounts/web_create_ajax/attempt/"
AGE_PATH = "/web/consent/check_age_eligibility/"
SEND_PATH = "/api/v1/accounts/send_verify_email/"
CONF_PATH = "/api/v1/accounts/check_confirmation_code/"
##################

#### User Data ####
MAIL = "meingottklappdochentlich@dsgvo.ru"
USERNAME = "1chb1ne1nb0t1382"
PASSWORD = "e1nzig@rt1gesP@5sw0rd"
###################

BASE_URL = "https://www.instagram.com"



def BuildUserDataBody(mail, keyId, pubKey, username):
    firstName = "IchBinKeinBot"
    encPwd = encrypt_password(keyId, pubKey, PASSWORD, version=10)
    body = "email={}&enc_password={}&username={}&firstname={}&seamless_login_enabled=1&opt_into_one_tap=false".format(mail, encPwd, username, firstName)

    return body


def BuildAgeBody():
    day = "6"
    month = "9"
    year = "1969"
    body = "day={}&month={}&year={}".format(day, month, year)

    return body

def BuildSendMailBody(mail, deviceId):
    body = "device_id={}&email={}".format(deviceId, mail)

    return body


def BuildConfermationBody(mail, deviceId, confCode):
    body = "code={}&device_id={}&email={}".format(confCode, deviceId, mail)

    return body


def PostRequest(baseUrl, urlCmdPart, token, igAjax, body, workingProxy):
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


    # logHeaders = "Connection: close\n{}Content-Type: application/x-www-form-urlencoded\n{}X-Instagram-AJAX: {}\n{}X-CSRFToken: {}\n{}X-IG-APP-ID: {}".format(
    #               logger.NEWLINE_DEBUG, logger.NEWLINE_DEBUG,  igAjax, logger.NEWLINE_DEBUG, token, logger.NEWLINE_DEBUG, appId)
    # logger.logEntry("debug", "  --- Request ---\n{}URL: {}\n{}Methode: post\n\n{}--- Headers ---\n{}{}".format(
    #               logger.NEWLINE_DEBUG, url, logger.NEWLINE_DEBUG, logger.NEWLINE_DEBUG, logger.NEWLINE_DEBUG, logHeaders))
    # logger.logEntry("debug", "--- Response ---\n{}{}".format(logger.NEWLINE_DEBUG, resp.text))

    jsonObject = json.loads(resp.text)
    status = jsonObject["status"]

    return (status, proxy)


def CreateAccountOnIG():
    status = ''
    spamDedCnt = 0

    while status != "ok":
        userDataBody = BuildUserDataBody(MAIL, keyId, pubKey, USERNAME)

        statusTuple = PostRequest(BASE_URL, USERDATA_PATH, token, igAjax, userDataBody, "")
        status = statusTuple[0]
        proxy = statusTuple[1]

        if status == "fail":
            spamDedCnt += 1
            logger.logEntry("error", "  Request marked as spam. Spam-detections: {}".format(spamDedCnt))

    logger.logEntry("info", "   --- The user data has been entered successfully ---")
    status = ''
    time.sleep(random.uniform(1.0, 2.0))

    while status != "ok":
        ageBody = BuildAgeBody()

        statusTuple = PostRequest(BASE_URL, AGE_PATH, token, igAjax, ageBody, proxy)
        status = statusTuple[0]
        proxy = statusTuple[1]

        if status == "fail":
            spamDedCnt += 1
            logger.logEntry("error", "  Request marked as spam. Spam-detections: {}".format(spamDedCnt))

    logger.logEntry("info", "   --- The age has been entered successfully ---")
    status = ''
    time.sleep(random.uniform(1.0, 2.0))

    while status != "ok":
        baseUrl = "https://i.instagram.com"

        mailBody = BuildSendMailBody(MAIL, deviceId)

        statusTuple = PostRequest(baseUrl, SEND_PATH, token, igAjax, mailBody, proxy)
        status = statusTuple[0]
        proxy = statusTuple[1]

        if status == "fail":
            spamDedCnt += 1
            logger.logEntry("error", "  Request marked as spam. Spam-detections: {}".format(spamDedCnt))

    logger.logEntry("info", "   --- An confermation code has been send to {} ---".format(MAIL))
    status = ''
    time.sleep(random.uniform(1.0, 2.0))

    while status != "ok":
        confCode = input("\nEnter the confirmation code: ")
        baseUrl = "https://i.instagram.com"

        confBody = BuildConfermationBody(MAIL, deviceId, confCode)
        
        statusTuple = PostRequest(baseUrl, CONF_PATH, token, igAjax, confBody, proxy)
        status = statusTuple[0]
        proxy = statusTuple[1]

        if status == "fail":
            spamDedCnt += 1
            logger.logEntry("error", "  Request marked as spam. Spam-detections: {}".format(spamDedCnt))
    
    print("--- the confermation code has been accepted ---\n--- Try to login with the following credentials ---\nUsername: {}\nPassword: {}\n".format(USERNAME, PASSWORD))
    status = ''
    time.sleep(random.uniform(1.0, 2.0))
    logging.info("\n\n#### QUITING PROGRAM ####")
    exit()



CreateAccountOnIG()


#PostRequest(baseUrl, urlCmdPart, connectionType, token, igAjax, contentType, body)