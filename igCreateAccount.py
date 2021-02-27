import requests
import json
import time
import logging
from proxyCrawler import proxy_request
from igPwdEncrypt import encrypt_password

############################
keyId = 212
pubKey = "fd1b44ee842e66d2178f3b406a8468b7739cc14752a7c827fe77a46270437512"
token = "MbpnYnqPmQZON1CzRcz2QXFfrbgsha2i"
igAjax = "0edc1000e5e7"
appId = "936619743392459"
deviceId = "YDp6mgALAAE0Qu8WOeOqQlZ_xEP9" # new
############################


#### URL Path ####
USERDATA_PATH = "/accounts/web_create_ajax/attempt/"
AGE_PATH = "/web/consent/check_age_eligibility/"
SEND_PATH = "/api/v1/accounts/send_verify_email/"
CONF_PATH = "/api/v1/accounts/check_confirmation_code/"
##################



contentType = "application/x-www-form-urlencoded"
BASE_URL = "https://www.instagram.com"

mail = "matthias@hottis.de"
pwd = "daspasswordistsicher"
username = "tesadstnasdas"




logging.basicConfig(filename='Logs/igLogon.log', level=logging.DEBUG)


def BuildUserDataBody(mail, keyId, pubKey, username):
    pwd = "e1nzig@rt1gesP@5sw0rd"
    firstName = "IchBinKeinBot"
    encPwd = encrypt_password(keyId, pubKey, pwd, version=10)
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

    debugHeaders = "Connection: close\nContent-Type: application/x-www-form-urlencoded\nX-Instagram-AJAX: {}\nX-CSRFToken: {}\nX-IG-APP-ID: {}".format(igAjax, token, appId)

    respTuple = proxy_request('post', url, headers, body, workingProxy)
    resp = respTuple[0]
    proxy = respTuple[1]

    logging.debug('\nURL: {}\nMethode: post\n\n--- Headers ---\n{}\n\n--- Body ---\n{}\n\n--- Response ---\n{}\n'.format(url, debugHeaders, body, resp.text))

    jsonObject = json.loads(resp.text)
    status = jsonObject["status"]

    return (status, proxy)






def CreateAccountOnIG():
    status = ''
    spamDedCnt = 0

    while status != "ok":
        userDataBody = BuildUserDataBody(mail, keyId, pubKey, username)

        statusTuple = PostRequest(BASE_URL, USERDATA_PATH, token, igAjax, userDataBody, "")
        status = statusTuple[0]
        proxy = statusTuple[1]

        if status == "fail":
            spamDedCnt += 1
            print("Instagram marked this request as spam. The Spam-detection is {}. Trying another proxy...\n".format(spamDedCnt))
        elif status != "ok":
            print("An unknown error has been received.")
            exit()

    print("--- the user data has been entered successfully ---")
    status = ''
    time.sleep(1.0)

    while status != "ok":
        ageBody = BuildAgeBody()

        statusTuple = PostRequest(BASE_URL, AGE_PATH, token, igAjax, ageBody, proxy)
        status = statusTuple[0]
        proxy = statusTuple[1]

        if status == "fail":
            spamDedCnt += 1
            print("Instagram marked this request as spam. The Spam-detection is {}. Trying another proxy...\n".format(spamDedCnt))
        elif status != "ok":
            print("An unknown error has been received.")
            exit()

    print("--- The age has been entered successfully ---")
    status = ''
    time.sleep(1.0)

    while status != "ok":
        baseUrl = "https://i.instagram.com"

        mailBody = BuildSendMailBody(mail, deviceId)

        statusTuple = PostRequest(baseUrl, SEND_PATH, token, igAjax, mailBody, proxy)
        status = statusTuple[0]
        proxy = statusTuple[1]

        print(statusTuple)
        if status == "fail":
            spamDedCnt += 1
            print("Instagram marked this request as spam. The Spam-detection is {}. Trying another proxy...\n".format(spamDedCnt))
        elif status != "ok":
            print("An unknown error has been received.")
            exit()

    print("--- An Confermation code has been send to {} ---".format(mail))
    status = ''
    time.sleep(1.0)

    while status != "ok":
        confCode = input("Enter the confirmation code: ")
        baseUrl = "https://i.instagram.com"

        confBody = BuildConfermationBody(mail, deviceId, confCode)
        
        statusTuple = PostRequest(baseUrl, CONF_PATH, token, igAjax, confBody, proxy)
        status = statusTuple[0]
        proxy = statusTuple[1]

        if status == "fail":
            spamDedCnt += 1
            print("Instagram marked this request as spam. The Spam-detection is {}. Trying another proxy...\n".format(spamDedCnt))
        elif status != "ok":
            print("An unknown error has been received.")
    
    print("--- the confermation code has been accepted ---")
    status = ''
    time.sleep(1.0)




CreateAccountOnIG()


#PostRequest(baseUrl, urlCmdPart, connectionType, token, igAjax, contentType, body)