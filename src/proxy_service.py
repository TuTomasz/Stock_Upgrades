from urllib.request import Request, urlopen
from bs4 import BeautifulSoup


class ProxyService:
    def __init__(self):
        self.proxy_list = []

    def getProxyList(self):
        return self.proxy_list

    def fetchProxies(self):

        url = "https://github.com/TheSpeedX/PROXY-List/blob/master/http.txt"

        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})

        response = urlopen(req).read()

        proxy = BeautifulSoup(response, "html.parser")

        for i in proxy.findAll("tr"):
            self.proxy_list.append("http://" + i.text.replace("\n", ""))

        return self.proxy_list

    def writeProxies(self):
        with open("data/proxy/proxy.txt", "w") as f:
            for i in self.proxy_list:
                f.write(i + "\n")


if __name__ == "__main__":

    proxies = ProxyService()
    proxies.fetchProxies()
    proxies.writeProxies()
