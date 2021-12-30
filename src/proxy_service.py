from urllib.request import Request, urlopen


class ProxyService:
    def __init__(self):
        self.proxy_list = []

    def get_proxy_list(self):
        return self.proxy_list

    def fetchProxies():

        url = "https://github.com/TheSpeedX/PROXY-List/blob/master/http.txt"

        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})

        webpage = urlopen(req).read().decode("utf-8")
