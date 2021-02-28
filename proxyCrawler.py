import requests
from bs4 import BeautifulSoup
from random import choice
import logger
import time
import random
import headerClass

SAME_PROXY_RETRYS = 5
NEW_PROXY_TIMEOUT = 5
WORKING_PROXY_TIMEOUT = 7
WORKING_PROXY_RETRYS = 5

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
        elif sameProxyCnt == SAME_PROXY_RETRYS:
            logger.logEntry("critical", "Tryed to get the same proxy for {} times\n<---- QUITING PROGRAM ---->".format(SAME_PROXY_RETRYS))
            exit()
    usedProxys.add(proxy['https'])

    return proxy


def ProxyRequest(methode, baseUrl, urlPath, headers, body, workingProxy):
    url = "{}{}".format(baseUrl, urlPath)
    headers = headers.GetJson()

    while True:
        if workingProxy == '':
            try:
                proxy = GetProxy()
                resp = requests.request(methode, url, headers=headers, data=body, proxies=proxy, timeout=NEW_PROXY_TIMEOUT)
                logger.logEntry("debug", "  Request send with proxy: {}".format(proxy["https"]))
                
                return (resp, proxy)
            except:
                logger.logEntry("warning", "Proxy {} failed. Trying another one...".format(proxy["https"]))
        else:
            for i in range(WORKING_PROXY_RETRYS, 0, -1):
                try:
                    resp = requests.request(methode, url, headers=headers, data=body, proxies=workingProxy, timeout=WORKING_PROXY_TIMEOUT)
                    logger.logEntry("debug", "  Request send with the previous proxy")
                   
                    return (resp, workingProxy)
                except:
                    logger.logEntry("warning", "Previous Proxy failed. {} more Trys...".format(i-1))
                    time.sleep(random.uniform(0.5, 1.0))
            workingProxy = ''





# def proxyRequest(requerstType, url, headers, body, workingProxy):
#     while True:
#         try:
#             if workingProxy == '':
#                 proxy = get_proxy()
#                 resp = requests.request(requerstType, url, headers=headers, data=body, proxies=proxy, timeout=5)
#             else:
#                 proxy = workingProxy
#                 time.sleep(random.uniform(1.0, 2.0))
#                 resp = requests.request(requerstType, url, headers=headers, data=body, proxies=workingProxy, timeout=10)
#             logger.logEntry("debug", "  Request send with Proxy: {}".format(proxy["https"]))
#             break
#         except:
#             logger.logEntry("warning", "Proxy {} failed. Trying another one...".format(proxy["https"]))

#     return (resp, proxy)