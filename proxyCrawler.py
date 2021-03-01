import requests
from bs4 import BeautifulSoup
from random import choice
import logger
import time
import random
import headerClass
import config as c


usedProxys = set()
def GetProxy():
    url = 'https://www.sslproxies.org/'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')

    sameProxyCnt = 0
    while True:
        proxy = {'https': choice(list(map(lambda x:x[0]+':'+x[1], list(zip(map(lambda x:x.text, soup.findAll('td')[::8]),
                                        map(lambda x:x.text, soup.findAll('td')[1::8]))))))}
        if proxy['https'] not in usedProxys:
            break
        elif sameProxyCnt == c.MAX_SAME_PROXY:
            if c.DEBUG1:
                logger.logEntry("critical", "Tryed to get the same proxy for {} times\n<---- QUITING PROGRAM ---->".format(c.MAX_SAME_PROXY))
            exit()
    usedProxys.add(proxy['https'])

    return proxy


def ProxyRequest(methode, baseUrl, urlPath, headers, body, workingProxy):
    url = "{}{}".format(baseUrl, urlPath)
    headers = headers.GetJson()
    changedWP = False

    while True:
        if workingProxy == '':
            try:
                proxy = GetProxy()
                if methode == 'post':
                    resp = requests.request(methode, url, headers=headers, data=body, proxies=proxy, timeout=c.NEW_PROXY_TIMEOUT)
                else:
                    resp = requests.request(methode, url, headers=headers, proxies=proxy, timeout=c.NEW_PROXY_TIMEOUT)
                if c.DEBUG2:
                    logger.logEntry("debug", "  Request send with proxy: {}".format(proxy["https"]))
                
                return (resp, proxy, changedWP)
            except:
                if c.DEBUG2:
                    logger.logEntry("warning", "Proxy {} failed. Trying another one...".format(proxy["https"]))
        else:
            for i in range(c.WORKING_PROXY_RETRYS, 0, -1):
                try:
                    resp = requests.request(methode, url, headers=headers, data=body, proxies=workingProxy, timeout=c.WORKING_PROXY_TIMEOUT)
                    if c.DEBUG2:
                        logger.logEntry("debug", "  Request send with the previous proxy")
                   
                    return (resp, workingProxy, changedWP)
                except:
                    if c.DEBUG2:
                        logger.logEntry("warning", "Previous proxy failed. {} more Trys...".format(i-1))
                    time.sleep(random.uniform(0.5, 1.0))
            if c.DEBUG2:
                logger.logEntry("warning", "Changing proxy...")
            workingProxy = ''
            changedWP = True