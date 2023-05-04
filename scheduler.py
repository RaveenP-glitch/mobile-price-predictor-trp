from datetime import date

import pandas as pd
import schedule
import time

from os import system

from Tools.scripts.dutree import display


#
# def printName():
#     print("Raveen Panditha")
#
# def job():
#     # system("python3 Amazon_price_tracker.py")
#     printName()
#
#
# schedule.every(4).seconds.do(job)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)


# def job():
# # Define variables
#   tickers = "AAPL GOOGL"
#   start = "2021-08-01"
#   end = date.today()
#   tickers_split = tickers.split()
#   df = pd.DataFrame()
#   tickers_split
#   # for ticker in tickers_split:
#   #     data = pdr.get_data_yahoo(ticker, start=start, end=end, interval='d')
#   #     df[ticker] = data['Adj Close']
#   print(df.shape)
#   display(df)
#   df.to_csv(r'path.csv')
#
# schedule.every().day.at("11:10").do(job)
# while True:
#    schedule.run_pending()
#    time.sleep(1)


# Schedule Library imported
import schedule
import time


# Functions setup
def sudo_placement():
    print("Get ready for Sudo Placement at Geeksforgeeks")


def good_luck():
    print("Good Luck for Test")


def work():
    print("Study and work hard")


def bedtime():
    print("It is bed time go rest")


def geeks():
    print("Shaurya says Geeksforgeeks")


# Task scheduling
# After every 10mins geeks() is called.
schedule.every(5).seconds.do(geeks)