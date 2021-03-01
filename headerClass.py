import json
import sessionClass
import logger


class Headers(object):
    encoding = "gzip, deflate"
    lang = "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7"
    userAgent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
   
    def __init__(self):
        self.json = {}

    # returns the header in dict/json format
    def GetJson(self):
        return self.json

    # returns a prettified header string
    def GetPrettyHeaders(self):
        prettyList = []
        for curKey in self.json.keys():
            curVal = self.json[curKey]
            prettyList.append('{}{}: {}\n'.format(logger.NEWLINE_DEBUG, curKey, curVal))
        
        return ''.join(prettyList)


# header for get-requests
class GetHeaders(Headers):
    accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    
    def __init__(self, connectType):
        self.connectType = connectType
        self.json = {
            'Connection': self.connectType,
            'Accept': GetHeaders.accept,
            'User-Agent': Headers.userAgent,
            'Accept-Encoding': Headers.encoding,
            'Accept-Language': Headers.lang
        }


# header for post-requests
class PostHeaders(Headers):
    contentType = "application/x-www-form-urlencoded"
    accept = "*/*"
    requestedWith = "XMLHttpRequest"
    #appId = '936619743392459'
    wwwClaim = '0'

    def __init__(self, connectType, session):
        self.connectType = connectType
        self.ajax = session.ajax
        self.token = session.token
        self.json = {
            'Connection': self.connectType,
            'X-Instagram-AJAX': self.ajax,
            'Content-Type': PostHeaders.contentType,
            'Accept': self.accept,
            'X-Requested-With': self.requestedWith,
            'User-Agent': Headers.userAgent,
            'X-CSRFToken': self.token,
            #'X-IG-App-ID': PostHeaders.appId,
            'X-IG-WWW-Claim': PostHeaders.wwwClaim,
            'Accept-Encoding': Headers.encoding,
            'Accept-Language': Headers.lang
        }