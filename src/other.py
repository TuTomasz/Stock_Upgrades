import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import json
import os
import datetime
from dateutil.parser import parse
import pandas as pd
import copy


def readQueueFile():
    """
    Reads a Queue.json file and returns a list of all the lines.
    """
    with open("Data/Queue/Queue.json", "r") as f:
        lines = f.readlines()
    return lines


def appendQueueFile(lines):
    """
    Appends a list of lines to a Queue.json  file.
    """
    with open("Data/Queue/Queue.json", "a") as f:
        f.write(lines)


def clearQueueFile():
    """
    Clears a Queue.json  file.
    """
    with open("Data/Queue/Queue.json", "w") as f:
        f.write("")


def populateQueueFile(file):

    ticker_dir = os.path.join("Data", "Tickers", "ticker_list.csv")
    rating_dir = os.path.join("Data", "Rating")
    df = pd.read_csv(ticker_dir)
    # tickers = df["Symbol"].tolist()

    ticker_dir = os.path.join("Data", "Tickers", "ticker_list.csv")

    # import ticker data from ticker_list.csv
    df = pd.read_csv(ticker_dir)

    tickers = df["Symbol"].tolist()

    for ticker in tickers:

        try:

            with open(rating_dir + "/" + ticker + ".json", "r") as f:
                data = json.load(f)

                ratings = data["Rating"]

                schema = {
                    "Ticker": data["Ticker"],
                    "Company": data["Company"],
                    "Sector": data["Sector"],
                    "Updated": data["Updated"],
                    "Rating": {},
                }
                print(ticker)
                for rating in ratings:
                    if rating["Date"] == datetime.datetime.today().strftime("%Y-%m-%d"):

                        rating_shemas = {
                            "Date": rating["Date"],
                            "Rating": rating["Rating"],
                            "Organization": rating["Organization"],
                            "Rating_Change": rating["Rating_Change"],
                            "Target_Change": rating["Target_Change"],
                        }

                        schema["Rating"] = rating_shemas

                        appendQueueFile(json.dumps(schema) + "\n")
        except Exception as e:
            print(e)


if __name__ == "__main__":

    # populate queue with new ratings that are of date today
    populateQueueFile("data/queue/Queue.json")
