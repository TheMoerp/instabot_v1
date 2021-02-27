import requests
from bs4 import BeautifulSoup
from random import choice


triedProxys = set()

def get_proxy():
    url = 'https://www.sslproxies.org/'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')

    # sameProxyCnt = 0
    # while True:
    proxy = {'https': choice(list(map(lambda x:x[0]+':'+x[1], list(zip(map(lambda x:x.text, soup.findAll('td')[::8]),
                                    map(lambda x:x.text, soup.findAll('td')[1::8]))))))}
        # if tuple(proxy) not in triedProxys:
        #     break
        # sameProxyCnt += 1
        # print("Got the same Proxy for the {} time. Choosing another one...".format(sameProxyCnt))
    
    # triedProxys.add(tuple(proxy))

    return proxy


def proxy_request(requerstType, url, headers, body, workingProxy):
    while True:
        try:
            if workingProxy == '':
                proxy = get_proxy()
            else:
                proxy = workingProxy
            resp = requests.request(requerstType, url, headers=headers, data=body, proxies=proxy, timeout=5)
            print("\nRequest send with Proxy: {}".format(proxy))
            break
        except:
            print("Proxy {} failed. Trying another one...".format(proxy))

    return (resp, proxy)