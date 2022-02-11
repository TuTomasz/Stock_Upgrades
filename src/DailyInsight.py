from DailyQueue import readQueueFile
import json
import copy

ratings = {"Downgrade": -1, "Initiated": 0, "Reiterated": 0, "Upgrade": 1, "Resumed": 0}

ratingChanges = {
    "Sector Outperform to Neutral": -2,
    "Buy to Gradually Accumulate": -1,
    "Overweight to Neutral": -2,
    "Underweight to Equal-Weight": 1,
    "Hold to Buy": 1,
    "Outperform to Buy": -1,
    "Hold to Underperform": -1,
    "Buy to Hold": -1,
    "Sector Weight": 0,
    "Under Perform to Market Perform": 1,
    "Neutral to Sell": -1,
    "Buy to Underperform": -1,
    "Sector Perform to Sector Outperform": 1,
    "Equal Weight to Overweight": 1,
    "In-line to Outperform": 1,
    "Perform to Outperform": 1,
    "Market Perform": 0,
    "Buy": 2,
    "Buy to Accumulate": -1,
    "Sector Perform to Underperform": -1,
    "Sector Underperform to Sector Outperform": 2,
    "Accumulate": 0,
    "Market Outperform to Market Perform": -1,
    "Sell to Neutral": 1,
    "Underperform to Mkt Perform": 1,
    "Sector Perform to Outperform": 1,
    "Sector Underperform": -1,
    "Underweight to Overweight": 2,
    "Overweight to Equal-Weight": -1,
    "Underperform to Perform": 1,
    "Mkt Perform": 0,
    "In-line": 0,
    "Outperform to Sell": -5,
    "Hold": 0,
    "Sector Outperform": 1,
    "Perform": 1,
    "Neutral to Negative": -1,
    "Equal-Weight to Underweight": -2,
    "Underperform to Buy": 3,
    "Neutral to Buy": 2,
    "Equal Weight to Underweight": -2,
    "Accumulate to Hold": 0,
    "Negative to Positive": 0,
    "Sector Weight to Overweight": 2,
    "Neutral to Reduce": -1,
    "Underperform to Outperform": 3,
    "Accumulate to Buy": 1,
    "Gradually Accumulate to Hold": -1,
    "Buy to Outperform": 1,
    "Market Perform to Outperform": 2,
    "Reduce to Hold": 1,
    "Strong Buy to Outperform": 1,
    "Neutral to Long-term Buy": 1,
    "Outperform to Underperform": -3,
    "Underperform": -1,
    "Outperform to Strong Buy": 1,
    "Outperform to Top Pick": 1,
    "Underperform to In-line": 2,
    "Neutral": 0,
    "Equal-Weight to Overweight": 2,
    "Underweight to Equal Weight": 2,
    "Outperform to Market Perform": -2,
    "Neutral to Sector Outperform": 2,
    "Hold to Accumulate": 1,
    "Sector Perform": 0,
    "Equal Weight": 0,
    "Underperform to Neutral": 2,
    "Strong Buy": 1,
    "Buy to Sell": -3,
    "Outperform to Peer Perform": -2,
    "Neutral to Underperform": -2,
    "Mkt Perform to Underperform": -2,
    "Top Pick to Outperform": 1,
    "Positive to Neutral": -2,
    "Sell": -2,
    "Sell to Outperform": 5,
    "Negative to Neutral": 1,
    "Strong Buy to Mkt Perform": -2,
    "In-line to Underperform": -1,
    "Sector Weight to Underweight": -1,
    "Buy to Strong Buy": 1,
    "Neutral to Underweight": -1,
    "Underweight to Neutral": 1,
    "Market Perform to Underperform": -1,
    "Overweight to Underweight": -3,
    "Mkt Outperform to Mkt Perform": -2,
    "Underweight": -1,
    "Outperform to Perform": -1,
    "Reduce": -1,
    "Hold to Gradually Accumulate": 1,
    "Mkt Perform to Strong Buy": 2,
    "Underperform to Peer Perform": 1,
    "Buy to Neutral": -1,
    "Underperform to Hold": 1,
    "Overweight to Equal Weight": -2,
    "Neutral to Overweight": 2,
    "Overweight to Sector Weight": -2,
    "Sell to Hold": 2,
    "Outperform to Sector Perform": -2,
    "Neutral to Outperform": 2,
    "Equal-Weight": 0,
    "Sell to Buy": 3,
    "Top Pick": 5,
    "Peer Perform": 0,
    "Positive": 1,
    "Sector Perform to Sector Underperform": -2,
    "Mkt Perform to Mkt Outperform": 2,
    "Overweight": 2,
    "Hold to Reduce": -1,
    "Sector Underperform to Sector Perform": 2,
    "Underperform to Sector Perform": 2,
    "Outperform to Neutral": -2,
    "Mkt Outperform": 2,
    "Neutral to Positive": 1,
    "Outperform to Mkt Perform": -2,
    "Hold to Sell": -2,
    "Peer Perform to Outperform": 2,
    "Outperform to In Line": -2,
    "Outperform to In-line": -2,
    "Mkt Perform to Outperform": 2,
    "Underweight to Sector Weight": 2,
    "Sector Outperform to Sector Perform": -2,
    "Strong Buy to Buy": -1,
    "Underperform to Market Perform": 2,
    "Peer Perform to Underperform": -2,
    "Outperform": 2,
}


schema = {
    "Ticker": "",
    "Updated": "",
    "Company": "",
    "Sector": "",
    "Analists": [],
    "Rating": "",
    "Target": "",
    "Score": 0,
}


def generateInsight():

    # read the queue file
    lines = readQueueFile()

    stocks = dict()

    for line in lines:

        # parse json line
        json_line = json.loads(line)

        stock = schema.copy()

        stock["Ticker"] = json_line["Ticker"]
        stock["Updated"] = json_line["Updated"]
        stock["Company"] = json_line["Company"]
        stock["Sector"] = json_line["Sector"]

        stocks[stock["Ticker"]] = stock

    for line in lines:
        # parse json line
        json_line = json.loads(line)

        # add reviewing organizations
        stock = stocks[json_line["Ticker"]]
        list = stock["Analists"]
        print(list)
        stock["Analists"] = list.append(json_line["Rating"]["Organization"])
        # compute score
        if json_line["Rating"]["Rating_Change"] in ratingChanges:

            stocks[stock["Ticker"]]["Score"] += ratingChanges[
                json_line["Rating"]["Rating_Change"]
            ]

        else:
            pass

    for stock in stocks:

        # write to file
        print(stocks[stock])


if __name__ == "__main__":

    generateInsight()
