import requests
from bs4 import BeautifulSoup
from random import choice
import logger

WORKING_PROXY_TRYS = 10


triedProxys = set()

def get_proxy():
    url = 'https://www.sslproxies.org/'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')

    proxy = {'https': choice(list(map(lambda x:x[0]+':'+x[1], list(zip(map(lambda x:x.text, soup.findAll('td')[::8]),
                                    map(lambda x:x.text, soup.findAll('td')[1::8]))))))}

    return proxy


def proxy_request(requerstType, url, headers, body, workingProxy):
    while True:
        try:
            if workingProxy == '':
                proxy = get_proxy()
                resp = requests.request(requerstType, url, headers=headers, data=body, proxies=proxy, timeout=5)
            else:
                proxy = workingProxy
                resp = requests.request(requerstType, url, headers=headers, data=body, proxies=workingProxy, timeout=10)
            logger.logEntry("debug", "  Request send with Proxy: {}".format(proxy["https"]))
            break
        except:
            logger.logEntry("warning", "Proxy {} failed. Trying another one...".format(proxy["https"]))

    return (resp, proxy)