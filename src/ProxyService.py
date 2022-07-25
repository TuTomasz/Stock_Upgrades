from urllib.request import Request, urlopen
from bs4 import BeautifulSoup


class ProxyService:
    def __init__(self):
        self.proxy_list = []

    def getProxyList(self):
        return self.proxy_list

    def fetchProxies(self):

        url = "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"

        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})

        response = urlopen(req).read()

        proxy = BeautifulSoup(response, "html.parser")

        for line in proxy.text.splitlines():
            self.proxy_list.append("http://" + line)

        return self.proxy_list

    def writeProxies(self):
        with open("data/proxy/proxy.txt", "w") as f:
            for i in self.proxy_list:
                f.write(i + "\n")

    def readProxies(self):
        with open("data/proxy/proxy.txt", "r") as f:
            for i in f.readlines():
                self.proxy_list.append(i.replace("\n", ""))

        return self.proxy_list


if __name__ == "__main__":

    proxies = ProxyService()
    proxies.fetchProxies()
    proxies.writeProxies()
