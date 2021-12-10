import sqlite3
import requests
import json
import os
import numpy as np
import matplotlib.pyplot as plt
from textwrap import wrap


def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/covid.db')
    cur = conn.cursor()

    # Visualization 1
    # make a line chart for the PFE and MRNA prices over past 100 days
    fig = plt.figure(figsize=(15,5))
    ax1 = fig.add_subplot(132)
    cur.execute('SELECT date,high FROM StocksInfo where stock_id = ?', (0, ))
    
    dates_list = []
    high_list = []
    info = cur.fetchall()

    for date in info:
        dates_list.append(date[0])
        high_list.append(date[1])

    x = dates_list
    y = high_list
    ax1.plot(x, y)
    
    ax1.set(xlabel='Date', ylabel='Stock Price',
       title='PFE High Price for Past 100 Days')
    ax1.grid()


    # Visualization 2
    ax2 = fig.add_subplot(131)
    cur.execute("SELECT StocksInfo.stock_id, StocksInfo.high, StocksInfo.low, covidData.new_cases FROM StocksInfo JOIN covidData ON StocksInfo.date=covidData.date")
    data = cur.fetchall()
    PFE = []
    MRNA = []
    lst_cases = []
    days = []
    for i in range(len(data)):
        print(data[i])
        #cur.execute("SELECT Stocks.name FROM Stocks WHERE Stocks.id=?", (data[i][0], ))
        dif = data[i][1] - data[i][2]
        cases = (data[i][3])/5000
        if data[i][0] == 0:
            PFE.append(dif)
        if data[i][0] == 1:
            MRNA.append(dif)
        lst_cases.append(cases)
        days.append(i)
    
    segment_PFE = PFE[:30]
    segment_MRNA = MRNA[:30]
    segment_cases = lst_cases[:30]
    segment_days = days[:30]

    ax2.plot(segment_days, segment_PFE, label = "PFE stock", linestyle=":", color='#FF94E1')
    ax2.plot(segment_days, segment_MRNA, label = "MRNA stock", linestyle=":", color='#6a0dad')
    ax2.plot(segment_days, segment_cases, label = "New COVID cases", linestyle="-", color='#007E42')
    ax2.legend()
    ax2.set(xlabel="Days", ylabel="Units", title=('\n'.join(wrap('''New COVID-19 Cases (per 5000 Americans) 
                                                    vs Daily Stock Averages for the past 30 days''',60))))


    # Visualization 3
    ax3 = fig.add_subplot(133)
    cur.execute("SELECT StocksInfo.stock_id, StocksInfo.high, StocksInfo.low, covidData.new_cases FROM StocksInfo JOIN covidData ON StocksInfo.date=covidData.date")
    data = cur.fetchall()
    PFE = []
    MRNA = []
    days = []
    for i in range(len(data)):
        print(data[i])
        #cur.execute("SELECT Stocks.name FROM Stocks WHERE Stocks.id=?", (data[i][0], ))
        high = data[i][1]
        cases = (data[i][3])
        if data[i][0] == 0:
            ratio = high/cases
            PFE.append(ratio)
        if data[i][0] == 1:
            ratio = high/cases
            MRNA.append(ratio)
        days.append(i)
    
    segment_PFE = PFE[:30]
    segment_MRNA = MRNA[:30]
    segment_days = days[:30]

    ax3.plot(segment_days, segment_PFE, label = "PFE stock", linestyle="-", color='#FF94E1')
    ax3.plot(segment_days, segment_MRNA, label = "MRNA stock", linestyle="-", color='#007E42')
    
    ax3.legend()
    ax3.set(xlabel="Days",ylabel="Units",title=('\n'.join(wrap('''New COVID-19 Cases (per 5000 Americans) 
                                            vs Daily Stock Averages for the past 30 days''', 60))))

    plt.show() 




if __name__ == "__main__":
    main()