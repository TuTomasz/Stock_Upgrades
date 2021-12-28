import os
from src.ratings import Ratings
from src.other import readQueueFile, appendQueueFile, clearQueueFile, populateQueueFile


dest_dir = os.path.join("Data", "Rating")

## SETUP AND DATA MODELS
AllProxies = []


if __name__ == "__main__":

    # read proxy.txt file
    with open("Data/proxy/proxy.txt", "r") as infile:
        proxies = infile.read().splitlines()

    for proxy in proxies:
        AllProxies.append("http://" + proxy)

    # clear queue if one is filled
    clearQueueFile()

    # obtain new ratings and update
    Ratings(dest_dir, AllProxies)

    # populate queue with new ratings that are of date today
    populateQueueFile("Data/queue/rating_queue.txt")
