import os
from src.RatingsService import Ratings
from src.DailyQueue import (
    clearQueueFile,
    populateQueueFile,
    archiveQueueFile,
)
from src.BestValue import findBestValue
from src.DailyInsight import generateInsight, clearInsightFile
from src.ProxyService import ProxyService

ratingsOutputPath = os.path.join("Data", "Rating")

## SETUP AND DATA MODELS
AllProxies = []


if __name__ == "__main__":

    # # # read proxy.txt file
    proxies = ProxyService().fetchProxies()

    # clear queue if one is filled
    clearQueueFile()
    clearInsightFile()

    # obtain new ratings and update
    Ratings(ratingsOutputPath, proxies)

    # populate queue with new ratings that are of date today
    populateQueueFile()

    # generate insights
    generateInsight()

    # generate monthly insights best value
