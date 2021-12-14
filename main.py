import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import json
import time
import random
import re
import uuid
import os


tickers = ["DIS", "AAPL"]

## SETUP AND DATA MODELS
proxies = [
    "http://88.255.102.98:8080",
    # "http://34.145.126.174:80",
    # "http://52.149.152.236:80",
    # "http://167.71.199.228:8080",
    # "http://96.95.164.41:3128",
    # "http://20.94.230.158:80",
    # "http://34.145.126.174:80",
    # "http://96.9.69.164:53281",
]
schema = {"Ticker": None, "Updated": None, "Rating": {}}
rating_shemas = {
    "Date": None,
    "Rating": None,
    "organization": None,
    "Rating_Change": None,
    "Target_Change": None,
}


def get_raw_data(ticker):
    webpage = None
    url = "https://finviz.com/quote.ashx?t=" + str(ticker)

    # get random proxy
    proxy = random.choice(proxies)
    # make request to url via random random proxy if response is ok, get soup else try again with new proxy
    while webpage is None:
        try:
            print("Using proxy: " + proxy + " ticker " + ticker)

            response = requests.get(
                url,
                headers={"User-Agent": "Mozilla/5.0"},
                proxies={"http": proxy},
                timeout=5,
            )
            webpage = response.content

        except Exception as e:
            print(e)
            proxy = random.choice(proxies)
            time.sleep(10)

    print(
        "Successfully connected to url: "
        + url
        + " via proxy: "
        + proxy
        + "extracted "
        + str(len(webpage))
        + " bytes"
    )
    return webpage


def extract_table_data(webpage):

    soup = BeautifulSoup(webpage, "html.parser")

    table_data = []
    ## find table by class name
    table = soup.find("table", {"class": "fullview-ratings-outer"})

    # extract text from each row and append as new list in table_data and remove all /n
    for row in table.findAll("tr"):
        row_data = []
        for cell in row.findAll("td"):
            text = cell.text.replace("\n", "")
            row_data.append(text)
        if len(row_data[0]) > 10:
            pass
        else:
            table_data.append(row_data)

    return table_data


def create_new_data_file(table_data, ticker):
    for row in table_data:
        if len(row) > 1:
            rating_schema = rating_shemas.copy()
            rating_schema["Date"] = row[0]
            rating_schema["Rating"] = row[1]
            rating_schema["organization"] = row[2]
            rating_schema["Rating_Change"] = row[3].replace("\u2192", "to")
            rating_schema["Target_Change"] = row[4].replace("\u2192", "to")
            tickerObject["Rating"][uuid.uuid4()] = rating_schema

    tickerObject["Rating"] = list(tickerObject["Rating"].values())

    # write to file
    with open(ticker + ".json", "w") as outfile:
        json.dump(tickerObject, outfile)


if __name__ == "__main__":
    for ticker in tickers:

        # get raw data
        soup = get_raw_data(ticker)
        table_data = extract_table_data(soup)

        # create a ne schema object
        tickerObject = schema.copy()
        tickerObject["Ticker"] = ticker
        tickerObject["Updated"] = time.strftime("%Y-%m-%d %H:%M:%S")

        # if ticker file does not exist in data directory
        if not os.path.exists(ticker + ".json"):
            create_new_data_file(table_data, ticker)
        else:
            # if file exists, open and load data
            with open(ticker + ".json", "r") as infile:
                old_data = json.load(infile)

            print(old_data)
            # compare rating data of old_data and add new data that is not in old_data

        print("Finished processing ticker: " + ticker)
