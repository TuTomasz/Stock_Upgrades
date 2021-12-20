import os
from src.other import Test

from src.ratings import Ratings


dest_dir = os.path.join("Data", "Rating")

## SETUP AND DATA MODELS
proxies = [
    "http://88.255.102.98:8080",
    "http://34.145.126.174:80",
    "http://52.149.152.236:80",
    "http://167.71.199.228:8080",
    "http://96.95.164.41:3128",
    "http://20.94.230.158:80",
    "http://34.145.126.174:80",
    "http://96.9.69.164:53281",
]

if __name__ == "__main__":

    Ratings(dest_dir, proxies)
