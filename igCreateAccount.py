import requests
import json

from igPwdEncrypt import encrypt_password


key_id = 190
pub_key = "bd0475b2c92847a475d5d59b682be0752aadb6777f6b5b6c2ed1b7eb4411717b"


urlCmdPart = "/accounts/web_create_ajax/attempt/"

token = "QEXVwVm7jC29tJ2GaqEBSL5NbCnJuGjb"
igAjax = "df8e0d63baeb"
contentType = "application/x-www-form-urlencoded"
baseUrl = "https://www.instagram.com"
connectionType = "close"

opt_into_one_tap = "false"

mail = "geborgenphantastischerluchs@datenschutz.ru"
pwd = "daspasswordistsicher"
username = "testnasdas"
#first_name = "testman"



#encPwd = encrypt_password(key_id, pub_key, pwd, version=10)

#body = "email={}&enc_password={}&username={}&firstname={}&opt_into_one_tap=false".format(mail, encPwd, username, first_name)


def BuildCredentialsBody(mail, firstName, keyId, pubKey):
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



def PostRequest(baseUrl, urlCmdPart, connectionType, token, igAjax, contentType, body):
    url = "{}{}".format(baseUrl, urlCmdPart)
    headers = {
        "Connection": connectionType,
        "X-Instagram-AJAX": igAjax,
        "Content-Type": contentType,
        "X-CSRFToken": token,
    }

    response = requests.post(url, headers=headers, data=body)
    #print("Status Code: {}\nText: {}".format(response.status_code, response.text))
    jsonObject = json.loads(response.text)
    status = jsonObject["status"]
    #print(jsonObject["status"])
    return status


def CreateAccountOnIG():
    credBody = BuildCredentialsBody(mail, firstName, keyId, pubKey)
    credUrlCmdPart = "/accounts/web_create_ajax/attempt/"
    status = PostRequest(baseUrl, credUrlCmdPart, connectionType, token, igAjax, contentType, credBody)
    
    if status == "ok":
        ageBody = BuildAgeBody()
        ageUrlCmdPart = "/web/consent/check_age_eligibility/"
        status == PostRequest(baseUrl, ageUrlCmdPart, connectionType, token, igAjax, conentType, ageBody)

        if status == "ok":
            print("An confermation code has been send to the following mail-address:\n{}".format(mail))
            confCode = input("Enter the confirmation code: ")
            






PostRequest(baseUrl, urlCmdPart, connectionType, token, igAjax, contentType, body)