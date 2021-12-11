import sqlite3
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
    
    days_ago_list = []
    high_list = []
    info = cur.fetchall()

    i = 0
    for date in info:
        days_ago_list.append(i)
        high_list.append(date[1])
        i += 1

    x = days_ago_list
    y = high_list
    ax1.plot(x, y, label='PFE stock', linestyle=':', color='blue')

    cur.execute('SELECT date,high FROM StocksInfo where stock_id = ?', (1, ))
    
    dates_list2 = []
    high_list2 = []
    info2 = cur.fetchall()

    j = 0
    for date in info2:
        dates_list2.append(j)
        high_list2.append(date[1])
        j += 1

    x2 = dates_list2
    y2 = high_list2
    ax1.plot(x2, y2, label='MRNA stock', color='purple')
    
    ax1.set(xlabel='Days Ago', ylabel='Stock Price',
       title='PFE & MRNA High Price for Past 100 Days')
    ax1.legend()
    ax1.grid()


    # Visualization 2
    # Daily change in stock price by new COVID case (per 5000 Americans) for past 30 days
    ax2 = fig.add_subplot(131)
    cur.execute("SELECT StocksInfo.stock_id, StocksInfo.high, StocksInfo.low, covidData.new_cases FROM StocksInfo JOIN covidData ON StocksInfo.date=covidData.date")
    data = cur.fetchall()
    PFE = []
    MRNA = []
    lst_cases = []
    days = []
    for i in range(len(data)):
        print(data[i])
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
    ax2.set(xlabel="Days Ago", ylabel="Change in Stock Price", title=('\n'.join(wrap('''Daily Change in Stock Price
                                                by new COVID Case (per 5000 Americans)''',60))))


    # Visualization 3
    # Stock price:COVID cases (per 5000 Americans) for the past 30 days
    ax3 = fig.add_subplot(133)
    cur.execute("SELECT StocksInfo.stock_id, StocksInfo.high, StocksInfo.low, covidData.new_cases FROM StocksInfo JOIN covidData ON StocksInfo.date=covidData.date")
    data = cur.fetchall()
    PFE = []
    MRNA = []
    days = []
    for i in range(len(data)):
        print(data[i])
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
    ax3.set(xlabel="Days Ago",ylabel="Stock Price:Cases Ratio",title=('\n'.join(wrap('''Stock Price:COVID Cases (per 5000 Americans) 
                                                                            for the past 30 days''', 60))))

    plt.show() 




if __name__ == "__main__":
    main()