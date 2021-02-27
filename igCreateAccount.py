import requests
import json
from proxyCrawler import proxy_request
from igPwdEncrypt import encrypt_password


keyId = 212
pubKey = "fd1b44ee842e66d2178f3b406a8468b7739cc14752a7c827fe77a46270437512"


urlCmdPart = "/accounts/web_create_ajax/attempt/"

token = "RHgkBu4tUfBVWMXFm1K456MnSaLZzurT"
igAjax = "0edc1000e5e7"

contentType = "application/x-www-form-urlencoded"
baseUrl = "https://www.instagram.com"
connectionType = "close"

opt_into_one_tap = "false"

mail = "EntzueckendUnfassbarerSkorpion@existiert.net"
pwd = "daspasswordistsicher"
username = "testnasdas"
#first_name = "testman"



#encPwd = encrypt_password(key_id, pub_key, pwd, version=10)

#body = "email={}&enc_password={}&username={}&firstname={}&opt_into_one_tap=false".format(mail, encPwd, username, first_name)


def BuildCredentialsBody(mail, keyId, pubKey):
    pwd = "e1nzig@rt1gesP@5sw0rd"
    firstName = "IchBinKeinBot"
    encPwd = encrypt_password(keyId, pubKey, pwd, version=10)
    body = "email={}&enc_password={}&username={}&firstname={}&opt_into_one_tap=false".format(mail, encPwd, username, firstName)

    return body


def BuildAgeBody():
    day = "6"
    month = "9"
    year = "1969"
    body = "day={}&month={}&year={}".format(day, month, year)

    return body


def PostRequest(baseUrl, urlCmdPart, connectionType, token, igAjax, contentType, body, workingProxy):
    url = "{}{}".format(baseUrl, urlCmdPart)
    headers = {
        "Connection": connectionType,
        "X-Instagram-AJAX": igAjax,
        "Content-Type": contentType,
        "X-CSRFToken": token,
    }

    respTuple = proxy_request('post', url, headers, body, workingProxy)
    resp = respTuple[0]
    proxy = respTuple[1]
    print(resp.text)

    jsonObject = json.loads(resp.text)
    status = jsonObject["status"]
    return (status, proxy)


def CreateAccountOnIG():
    status = ''
    spamDedCnt = 0

    while status != "ok":
        credBody = BuildCredentialsBody(mail, keyId, pubKey)
        credUrlCmdPart = "/accounts/web_create_ajax/attempt/"

        statusTuple = PostRequest(baseUrl, credUrlCmdPart, connectionType, token, igAjax, contentType, credBody, '')
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
    
    while status != "ok":
        ageBody = BuildAgeBody()
        ageUrlCmdPart = "/web/consent/check_age_eligibility/"

        statusTuple = PostRequest(baseUrl, ageUrlCmdPart, connectionType, token, igAjax, contentType, ageBody, proxy)
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

    while status != "ok":
        print("An confermation code has been send to the following mail-address:\n{}".format(mail))
        confCode = input("Enter the confirmation code: ")

            



CreateAccountOnIG()


#PostRequest(baseUrl, urlCmdPart, connectionType, token, igAjax, contentType, body)