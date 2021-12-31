import os
from src.ratings import Ratings
from src.other import readQueueFile, appendQueueFile, clearQueueFile, populateQueueFile
from src.proxy_service import ProxyService

dest_dir = os.path.join("Data", "Rating")

## SETUP AND DATA MODELS
AllProxies = []


if __name__ == "__main__":

    # read proxy.txt file
    proxies = ProxyService().fetchProxies()
    print(proxies)

    # clear queue if one is filled
    clearQueueFile()

    # obtain new ratings and update
    Ratings(dest_dir, proxies)

    # populate queue with new ratings that are of date today
    populateQueueFile("Data/queue/rating_queue.txt")
