import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import json
import time
import random
import re
import uuid
import os
import datetime
from dateutil.parser import parse
import pandas as pd
import copy


class Ratings:
    def __init__(self, dest_dir, proxies):
        self.dest_dir = dest_dir
        self.proxies = proxies
        self.schema = {
            "Ticker": None,
            "Company": None,
            "Sector": None,
            "Updated": None,
            "Rating": {},
        }
        self.rating_shemas = {
            "Date": None,
            "Rating": None,
            "organization": None,
            "Rating_Change": None,
            "Target_Change": None,
        }
        self.main()

    def main(self):
        ticker_dir = os.path.join("Data", "Tickers", "ticker_list.csv")

        # import ticker data from ticker_list.csv
        df = pd.read_csv(ticker_dir)

        tickers = df["Symbol"].tolist()
        tickerNames = df["Name"].tolist()
        tickerSector = df["Sector"].tolist()

        for index, ticker in enumerate(tickers):
            print(ticker)
            # get raw data
            soup = self.get_raw_data(ticker)
            new_ticker_data = self.extract_table_data(soup)

            companyName = tickerNames[index]
            CompanySector = tickerSector[index]

            # if ticker file does not exist in data directory
            if not os.path.exists(os.path.join(self.dest_dir, ticker + ".json")):
                self.create_new_data_file(
                    new_ticker_data, ticker, companyName, CompanySector
                )
            else:
                # if file exists, open and load data
                with open(os.path.join(self.dest_dir, ticker + ".json"), "r") as infile:
                    existing_ticker_data = json.load(infile)

                # compare rating data of old_data and add new data that is not in old_data
                self.update_existing_data(existing_ticker_data, new_ticker_data, ticker)

    def get_raw_data(self, ticker):
        webpage = None
        url = "https://finviz.com/quote.ashx?t=" + str(ticker)

        # get random proxy
        proxy = random.choice(self.proxies)
        # make request to url via random random proxy if response is ok, get soup else try again with new proxy
        while webpage is None:
            try:
                print("Using proxy: " + str(proxy) + " ticker " + str(ticker))

                response = requests.get(
                    url,
                    headers={"User-Agent": "Mozilla/5.0"},
                    proxies={"http": proxy},
                    timeout=5,
                )
                webpage = response.content
                time.sleep(random.randint(2, 5))

            except Exception as e:
                print(e)
                proxy = random.choice(self.proxies)
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

    def extract_table_data(self, webpage):

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

    def create_new_data_file(self, table_data, ticker, companyName, CompanySector):

        # create a ne schema object

        tickerObject = self.format_data(table_data, ticker, companyName, CompanySector)

        # write to file
        with open(os.path.join(self.dest_dir, ticker + ".json"), "w") as outfile:
            json.dump(tickerObject, outfile)

        tickerObject = None

    def format_data(self, table_data, ticker, companyName, CompanySector):
        # create a ne schema object
        tickerObject = copy.deepcopy(self.schema)
        print(tickerObject)
        tickerObject["Ticker"] = ticker
        tickerObject["Updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
        tickerObject["Company"] = companyName
        tickerObject["Sector"] = CompanySector

        for row in table_data:

            if len(row) > 1:
                rating_schema = self.rating_shemas.copy()
                rating_schema["Date"] = str(
                    datetime.datetime.strptime(
                        str(parse(row[0])), "%Y-%m-%d %H:%M:%S"
                    ).date()
                )
                rating_schema["Rating"] = row[1]
                rating_schema["organization"] = row[2]
                rating_schema["Rating_Change"] = row[3].replace("\u2192", "to")
                rating_schema["Target_Change"] = row[4].replace("\u2192", "to")
                tickerObject["Rating"][uuid.uuid4()] = rating_schema

        tickerObject["Rating"] = list(tickerObject["Rating"].values())

        return tickerObject

    def format_existing_data(self, table_data):
        # create a ne schema object
        tickerObject = copy.deepcopy(self.schema)

        tickerObject["Updated"] = time.strftime("%Y-%m-%d %H:%M:%S")

        for row in table_data:

            if len(row) > 1:
                rating_schema = self.rating_shemas.copy()
                rating_schema["Date"] = str(
                    datetime.datetime.strptime(
                        str(parse(row[0])), "%Y-%m-%d %H:%M:%S"
                    ).date()
                )
                rating_schema["Rating"] = row[1]
                rating_schema["organization"] = row[2]
                rating_schema["Rating_Change"] = row[3].replace("\u2192", "to")
                rating_schema["Target_Change"] = row[4].replace("\u2192", "to")
                tickerObject["Rating"][uuid.uuid4()] = rating_schema

        tickerObject["Rating"] = list(tickerObject["Rating"].values())

        return tickerObject

    def update_existing_data(self, existing_ticker_data, new_ticker_data, ticker):

        # update existing data
        existing_ticker_data["Updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
        existing = existing_ticker_data["Rating"]
        new = self.format_existing_data(new_ticker_data)["Rating"]

        # append missing data to existing data
        for new_rating in new:
            if new_rating not in existing:
                existing.append(new_rating)

        # sort existing data by date turn date into datetime object
        for rating in existing:
            rating["Date"] = datetime.datetime.strptime(
                rating["Date"], "%Y-%m-%d"
            ).date()

        # sort by date
        existing.sort(key=lambda x: x["Date"], reverse=True)

        for rating in existing:
            rating["Date"] = str(rating["Date"])

        # write to file and save in data folder

        with open(os.path.join(self.dest_dir, ticker + ".json"), "w") as outfile:
            json.dump(existing_ticker_data, outfile)

    def __str__(self):
        return str(self.rating)
