# Using the following API: 
# with this documentation: https://www.alphavantage.co/documentation/ 

import sqlite3
import requests
import json
import os

def getStockInfo():
    stocks_list = ['PFE', 'MRNA']
    api_token = 'OE6TF62A0XRAYG2F'
    cleaned_stocks_list = []

    for i in range(len(stocks_list)):
        base_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&outputsize=compact&apikey={}"
        new_url = base_url.format(stocks_list[i], api_token)
        data = requests.get(new_url)
        info_dict = json.loads(data.text)
        stock = stocks_list[i]

        for date in info_dict["Time Series (Daily)"]:
            metrics_of_interest = {}

            metrics_of_interest['stock'] = stock
            metrics_of_interest['date'] = date
            metrics_of_interest['high'] = float(info_dict["Time Series (Daily)"][date]["2. high"])
            metrics_of_interest['low'] = float(info_dict["Time Series (Daily)"][date]["3. low"])
            metrics_of_interest['volume'] = int(info_dict["Time Series (Daily)"][date]["5. volume"])

            cleaned_stocks_list.append(metrics_of_interest)
    
    return cleaned_stocks_list


def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn    


def setUpStocks(stocks_info, cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Stocks (stock_id NUMBER PRIMARY KEY, stock TEXT, date TEXT, high NUMBER, low NUMBER, volume NUMBER)")

    #select max id (last one put in db)
    cur.execute('SELECT stock_id FROM Stocks WHERE stock_id  = (SELECT MAX(stock_id) FROM Stocks)')
    start = cur.fetchone()
    if (start!=None):
        start = start[0] + 1
    else:
        start = 1

    for x in stocks_info[start:start+25]:
        stock = x['stock']
        date = x['date']
        high = x['high']
        low = x['low']
        volume = x['volume'] 
        cur.execute("INSERT INTO Stocks (stock, date, high, low, volume) VALUES(?, ?, ?, ?, ?)", (stock, date, high, low, volume))
    
    conn.commit()
    


def main():
    cur, conn = setUpDatabase('covid_stocks.db')

    cleaned_stocks_dict = getStockInfo()
    print(cleaned_stocks_dict)

    setUpStocks(cleaned_stocks_dict, cur, conn)



if __name__ == "__main__":
    main()