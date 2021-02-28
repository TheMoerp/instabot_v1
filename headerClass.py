import json


class Headers(object):
    contentType = "application/x-www-form-urlencoded"
    encoding = "gzip, deflate"
    lang = "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7"
    userAgent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
    accept = "*/*"
    requestedWith = "XMLHttpRequest"

    def __init__(self, connectType, ajax, token, appId):
        self.connectType = connectType
        self.ajax = ajax
        self.token = token
        self.appId = appId

    def GetJson(self):
        self.json = {
            'Connection': self.connectType,
            'X-Instagram-AJAX': self.ajax,
            'Content-Type': Headers.contentType,
            'Accept': Headers.accept,
            'X-Requested-With': Headers.requestedWith,
            'User-Agent': Headers.userAgent,
            'X-CSRFToken': self.token,
            'X-IG-App-ID': self.appId,
            'Accept-Encoding': Headers.encoding,
            'Accept-Language': Headers.lang
        }
        return self.json

    # def GetPrettyHeaders(self):
