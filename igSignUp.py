import requests
import json
import time
import random
import logger
import sessionClass
import headerClass
import accountClass
import config as c
from proxyCrawler import ProxyRequest
from igPwdEncrypt import encrypt_password


# quick checks the response to known issues
spamCnt = 0
def RespChecker(baseUrl, urlPath, h, body, proxy, resp, curSpamCnt, curProxySpamCnt):
    global spamCnt
    respDict = json.loads(resp.text)
    try:
        if respDict['status'] == 'ok':
            return True
        else:
            try:
                # check for spam-detection
                if respDict['spam']:
                    spamCnt += 1
                    logger.logEntry("error", "  Request with {} marked as spam.\n{}> Total spamcounter: {}\n{}> Request spamcounter: {}\n{}> Proxy spamcounter: {}".format(
                                    proxy['https'], logger.NEWLINE_ERROR, spamCnt, logger.NEWLINE_ERROR, curSpamCnt, logger.NEWLINE_ERROR, curProxySpamCnt))
            except:
                # unknown issue
                debugOutput('error', baseUrl, urlPath, h, body, proxy, resp.text)
    except:
                # unknown issue
                debugOutput('error', baseUrl, urlPath, h, body, proxy, resp.text)
    return False

# function to log prettified request & response
def debugOutput(level, baseUrl, urlPath, h, body, proxy, resp):
    global spamCnt
    url = "{}{}".format(baseUrl, urlPath)

    # pretify response
    respDict = json.loads(resp)
    prettyResp = []
    for curKey in respDict.keys():
        curVal = respDict[curKey]
        prettyResp.append('{}{}: {}\n'.format(logger.NEWLINE_DEBUG, curKey, curVal))
    prettyResp = ''.join(prettyResp)

    # prettify response
    prettyBody = ['{}{}\n'.format('&', x) for x in body.split('&') if x]
    prettyBody[0] = prettyBody[0][1::]
    prettyBody = ['{}{}'.format(logger.NEWLINE_DEBUG, x) for x in prettyBody]
    prettyBody = ''.join(prettyBody)
    
    # debug log: connection-data, headers, body, response
    logger.logEntry(level, "   --- Debug output ---\n{}URL: {}\n{}Proxy: {}\n\n{}-- Headers --\n{}\n{}-- Body --\n{}\n{}-- Response --\n{}".format(logger.NEWLINE_DEBUG, 
                    url, logger.NEWLINE_DEBUG, proxy['https'], logger.NEWLINE_DEBUG, h.GetPrettyHeaders(), logger.NEWLINE_DEBUG, prettyBody, logger.NEWLINE_DEBUG, prettyResp))


def EnterFunction(baseUrl, urlPath, h, body, proxy, confCheck):
    respCheck = False
    curSpamCnt = 0
    curProxySpamCnt = 0
    while not respCheck:
        # checks if the current function is 'check confermation code'
        if confCheck:
            confCode = input("\nEnter the confirmation code: ")
            print("")
            body = "code={}{}".format(confCode, body)

        curSpamCnt += 1
        curProxySpamCnt += 1
        time.sleep(random.uniform(1.0, 2.0))

        # check if the proxy has to be changed due to too frequent spam detections
        if curProxySpamCnt <= c.MAX_PROXY_SPAM:
            respTuple = ProxyRequest('post', baseUrl, urlPath, h, body, proxy)
            if respTuple[2]:
                curProxySpamCnt = 0
        else:
            if c.DEBUG2:
                logger.logEntry("warning", "Changing proxy...")
            respTuple = ProxyRequest('post', baseUrl, urlPath, h, body, '')
            proxy = respTuple[1]
            curProxySpamCnt = 0
        if c.DEBUG3:
            debugOutput('debug', baseUrl, urlPath, h, body, proxy, respTuple[0].text)

        # quick checks the response to known issues
        respCheck = RespChecker(baseUrl, urlPath, h, body, proxy, respTuple[0], curSpamCnt, curProxySpamCnt)
    return respTuple


def SignUpNewAccount():
    if c.DEBUG1:
        logger.logEntry("info", "   <---- STARTING TO CREATE AN INSTAGRAM ACCOUNT ---->\n")

    # creating objects
    nAcc = accountClass.Account(c.MAIL, c.NAME, c.USERNAME, c.PASSWORD, c.DAY, c.MONTH, c.YEAR)
    s = sessionClass.Session()
    h = headerClass.PostHeaders('close', s)
    proxy = s.GetWorkingProxy()
    time.sleep(random.uniform(1.0, 2.0))

    # UserData
    baseUrl = "https://www.instagram.com"
    urlPath = "/accounts/web_create_ajax/attempt/"
    encPassword = encrypt_password(s.keyId, s.pubKey, nAcc.password, version=s.cryptVersion)
    body = "email={}&enc_password={}&username={}&firstname={}&seamless_login_enabled=1&opt_into_one_tap=false".format(
                  nAcc.mail, encPassword, nAcc.username, nAcc.name)
    respTuple = EnterFunction(baseUrl, urlPath, h, body, proxy, False)
    if c.DEBUG1:
        logger.logEntry("info", "   The user data has been entered successfully")
    time.sleep(random.uniform(1.0, 2.0))

    # Age
    baseUrl = "https://www.instagram.com"
    urlPath = "/web/consent/check_age_eligibility/"
    body = "day={}&month={}&year={}".format(nAcc.day, nAcc.month, nAcc.year)
    respTuple = EnterFunction(baseUrl, urlPath, h, body, respTuple[1], False)
    if c.DEBUG1:
        logger.logEntry("info", "   The age has been entered successfully")
    time.sleep(random.uniform(1.0, 2.0))

    # send mail
    baseUrl = "https://i.instagram.com"
    urlPath = "/api/v1/accounts/send_verify_email/"
    body = "device_id={}&email={}".format(s.mid, nAcc.mail)
    respTuple = EnterFunction(baseUrl, urlPath, h, body, respTuple[1], False)

    if c.DEBUG1:
        logger.logEntry("info", "   An confermation code has been send to the following mail address\n{}> Mail: {}".format(
                        logger.NEWLINE_INFO, nAcc.mail))
    time.sleep(random.uniform(1.0, 2.0))

    # check confermation code
    baseUrl = "https://i.instagram.com"
    urlPath = "/api/v1/accounts/check_confirmation_code/"
    bodyPart = "&device_id={}&email={}".format(s.mid, nAcc.mail)
    respTuple = EnterFunction(baseUrl, urlPath, h, bodyPart, respTuple[1], True)
    respDict = json.loads(respTuple[0].text)
    signUpCode = respDict['signup_code']
    if c.DEBUG1:
        logger.logEntry("info", "   The confermation code has been accepted")
    time.sleep(random.uniform(2.0, 3.0))

    # create account
    baseUrl = "https://www.instagram.com"
    urlPath = "/accounts/web_create_ajax/"
    #encPassword = encrypt_password(s.keyId, s.pubKey, nAcc.password, version=s.cryptVersion)
    body = "email={}&enc_password={}&username={}&first_name={}&month={}&day={}&year={}&client_id={}&searmless_login_enabled=1&tos_version=eu&force_sign_up_code={}".format(
            nAcc.mail, encPassword, nAcc.username, nAcc.name, nAcc.month, nAcc.day, nAcc.year, s.mid, signUpCode)
    respTuple = EnterFunction(baseUrl, urlPath, h, body, respTuple[1], False)
    if c.DEBUG3:
        debugOutput('error', baseUrl, urlPath, h, body, proxy, respTuple[0].text)
    print("")
    if c.DEBUG1:
        logger.logEntry("critical", "<---- QUITING PROGRAM ---->")


SignUpNewAccount()