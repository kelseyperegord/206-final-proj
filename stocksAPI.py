# Using the following API: Alpha Vantage
# with this documentation: https://www.alphavantage.co/documentation/ 

import sqlite3
import requests
import json
import os
import numpy as np
import matplotlib.pyplot as plt

# Query Alpha Vantage API to collect desired PFE and MRNA stock info for past 100 days
def getStockInfo():
    stocks_list = ['PFE', 'MRNA']
    api_token = 'OE6TF62A0XRAYG2F'
    cleaned_stocks_list = []
    uniq = 1

    for i in range(len(stocks_list)):
        base_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&outputsize=compact&apikey={}"
        new_url = base_url.format(stocks_list[i], api_token)
        data = requests.get(new_url)
        info_dict = json.loads(data.text)
        stock = stocks_list[i]

        # Collect daily info for each stock
        for date in info_dict["Time Series (Daily)"]:
            new_date = date.replace("-", '')
            metrics_of_interest = {}
            metrics_of_interest['uniq'] = uniq
            metrics_of_interest['stock'] = stock
            metrics_of_interest['date'] = int(new_date)
            metrics_of_interest['high'] = float(info_dict["Time Series (Daily)"][date]["2. high"])
            metrics_of_interest['low'] = float(info_dict["Time Series (Daily)"][date]["3. low"])
            metrics_of_interest['volume'] = int(info_dict["Time Series (Daily)"][date]["5. volume"])

            # Add new day to stock info list
            cleaned_stocks_list.append(metrics_of_interest)
            uniq += 1
    
    return cleaned_stocks_list


# Set up database
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn    


# Create table with stock name and an id to avoid duplicate string data
def createStocksTable(cur,conn):
    stocks = ['PFE', 'MRNA']

    cur.execute("CREATE TABLE IF NOT EXISTS Stocks (id INTEGER PRIMARY KEY, name TEXT)")
    for i in range(len(stocks)):
        cur.execute("INSERT OR IGNORE INTO Stocks (id,name) VALUES (?,?)",(i,stocks[i]))
    conn.commit()


# Create table that details daily info for each of the 2 stocks for past 100 days
def setUpStocks(stocks_info, cur, conn, startIndex):

    for x in stocks_info[startIndex:startIndex + 25]:
        if x['stock'] == 'PFE':
            stock_id = 0
        else:
            stock_id = 1
        uniq = x['uniq']
        date = x['date']
        high = x['high']
        low = x['low']
        volume = x['volume'] 
        cur.execute("INSERT OR IGNORE INTO StocksInfo (uniq, date, stock_id, high, low, volume) VALUES(?, ?, ?, ?, ?, ?)", (uniq, date, stock_id, high, low, volume))
    
    conn.commit()


def main():
    cur, conn = setUpDatabase('covid.db')

    # Create StocksInfo table in db
    cur.execute("CREATE TABLE IF NOT EXISTS StocksInfo (uniq NUMBER PRIMARY KEY, date NUMBER, stock_id NUMBER, high NUMBER, low NUMBER, volume NUMBER)")
    cur.execute('SELECT max (uniq) from StocksInfo')
    
    # Gather data from Alpha Vantage API
    cleaned_stocks_dict = getStockInfo()
    print(cleaned_stocks_dict)

    # Get current row in db
    startIndex = cur.fetchone()[0]
    print(startIndex)
    if startIndex == None:
        startIndex = 0

    # Set up both tables, which share a key
    setUpStocks(cleaned_stocks_dict, cur, conn, startIndex)
    createStocksTable(cur, conn)



if __name__ == "__main__":
    main()