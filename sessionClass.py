import requests
import json
import logger
import headerClass
import proxyCrawler
#from igSignup import RespChecker


class Session(object):
    baseUrl = 'https://www.instagram.com'
    urlPathSD = '/data/shared_data/?__a=1'
    urlPathCI = '/web/__mid/'
    h = headerClass.GetHeaders('close')

    def __init__(self):
        logger.logEntry('debug', '  Creating a new Session...')
        self.respTuple = proxyCrawler.ProxyRequest('get', Session.baseUrl, Session.urlPathSD, Session.h, '', '')
        self.respJson = json.loads(self.respTuple[0].text)
        self.cryptVersion = int(self.respJson['encryption']['version'])
        self.keyId = int(self.respJson['encryption']['key_id'])
        self.pubKey = self.respJson['encryption']['public_key']
        self.ig_did = self.respJson['device_id']
        self.ajax = self.respJson['rollout_hash']
        self.token = self.respJson['config']['csrf_token']
        logger.logEntry('debug', '  Shared data has been scraped')
        self.respTuple = proxyCrawler.ProxyRequest('get', Session.baseUrl, Session.urlPathCI, Session.h, '', self.respTuple[1])
        self.clientId = self.respTuple[0].text
        self.proxy = self.respTuple[1]
        logger.logEntry('debug', '  Client_ID has been scraped')
        logger.logEntry('info', '   A new session has been created successfully.')

    def GetWorkingProxy(self):
        return self.proxy