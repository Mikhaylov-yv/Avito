import requests
from lxml import html

class Proxy(object):
    proxy_list = ['40.134.138.222','107.190.148.178']


    def get_proxy(self):
        for proxy in self.proxy_list:
            url = 'http://' + proxy
            try:
                r = requests.get('https://www.avito.ru',proxies = {'http': url})
                if r.status_code == 200:
                    return url
            except requests.exceptions.ConnectionError:
                continue
def Proxy_next(url):
    proxy = Proxy()
    proxy = proxy.get_proxy()
    print(proxy)
    html = requests.get(url, proxies={'http': proxy}).content
    print(html)
    # r = requests.get('http://speed-tester.info/check_ip.php',proxies = {'http': proxy})
    # print(r.content)