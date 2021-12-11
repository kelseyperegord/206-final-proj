import requests
import json
import os
import sqlite3


# Query Covid Act Now API to obtain desired info
def getDataFromCOVID():
    uniq_key = []
    lst_of_date = []
    lst_of_new_cases = []
    lst_of_new_deaths = []
    lst_of_init = []
    lst_of_complete = []

    base_url = 'https://api.covidactnow.org/v2/country/US.timeseries.json?apiKey=058ae95db40f49de9aa59c9c3b5ca56e'
    data = requests.get(base_url)
    info = json.loads(data.text)
    reversed_lst = list(reversed(info['actualsTimeseries']))
    i = 102
    curr_initiated_vax = reversed_lst[103]['vaccinationsInitiated']
    curr_completed_vax = reversed_lst[103]['vaccinationsCompleted']
    x = 1
    while i >= 3:
        if reversed_lst[i]['vaccinationsInitiated'] == None:
            vax_init_per_day = 0
            vax_complete_per_day = 0
        else:
            vax_init_per_day = int(reversed_lst[i]['vaccinationsInitiated']) - int(curr_initiated_vax)
            vax_complete_per_day = int(reversed_lst[i]['vaccinationsCompleted']) - int(curr_completed_vax)
            curr_initiated_vax = reversed_lst[i]['vaccinationsInitiated']
            curr_completed_vax = reversed_lst[i]['vaccinationsCompleted']
        
        if reversed_lst[i]['newCases'] == None:
            new_cases = 0
            new_deaths = 0
        else:
            new_cases = int(reversed_lst[i]['newCases'])
            new_deaths = int(reversed_lst[i]['newDeaths'])
        date = reversed_lst[i]['date']
        split_date = date.split("-")
        new_date = int("".join(split_date))

        uniq_key.append(x)
        lst_of_date.append(new_date)
        lst_of_new_cases.append(new_cases)
        lst_of_new_deaths.append(new_deaths)
        lst_of_init.append(vax_init_per_day)
        lst_of_complete.append(vax_complete_per_day)
        x += 1
        i -= 1
    return uniq_key, lst_of_date, lst_of_new_cases, lst_of_new_deaths, lst_of_init, lst_of_complete


# def calculateQuarterAvg():
#     uniqs, dates, new_cases, new_deaths, vax_init, vax_complete = getDataFromCOVID()
#     lst_of_lsts = []
#     curr_lst = []
#     for i in range(len(uniqs)):
#         if (i + 1) % 25 == 0:
#             curr_date = dates[i]
#             curr_cases = new_cases[i]
#             curr_deaths = new_deaths[i]
#             init_vax = vax_init[i]
#             complete_vax = vax_complete[i]
#             tup = (curr_cases, curr_deaths, init_vax, complete_vax)
#             curr_lst.append(tup)
#             lst_of_lsts.append(curr_lst)
#             curr_lst = []
#             continue
#         curr_date = dates[i]
#         curr_cases = new_cases[i]
#         curr_deaths = new_deaths[i]
#         init_vax = vax_init[i]
#         complete_vax = vax_complete[i]
#         tup = (curr_cases, curr_deaths, init_vax, complete_vax)
#         curr_lst.append(tup)
#     avgs = {}
#     for x in range(len(lst_of_lsts)):
#         avgs[x] = []
#         counter = 0
#         tot_cases = 0
#         tot_deaths = 0
#         tot_init_vax = 0
#         tot_complete_vax = 0
#         for tup in lst_of_lsts[x]:
#             counter += 1
#             tot_cases += tup[0]
#             tot_deaths += tup[1]
#             tot_init_vax += tup[2]
#             tot_complete_vax += tup[3]
#         avgs[x].append(tot_cases/counter)
#         avgs[x].append(tot_deaths/counter)
#         avgs[x].append(tot_init_vax/counter)
#         avgs[x].append(tot_complete_vax/counter)
#     return avgs

# def calculationsFile():
#     path = os.path.dirname(os.path.abspath(__file__))
#     dct = calculateQuarterAvg()
#     quarters = ['25', '50', '75', '100']
#     with open (path+'/'+'calculations.txt', 'w') as f:
#         f.write('quarter, average new cases per day, average new deaths per day, average # of people initiating their vaccines per day, average # of people completing their vaccines per day')
#         f.write('\n')
#         for key in dct:
#             new_str = []
#             new_str.append(quarters[key])
#             for item in dct[key]:
#                 new_str.append(str(item))
#             f_string = ",".join(new_str)
#             f.write(f_string)
#             f.write('\n')


def setUpDb(f_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+f_name)
    cur = conn.cursor()
    return cur, conn

def createDb1(cur, conn, startIndex):
    uniqs, date, new_cases, new_deaths, vax_init, vax_complete = getDataFromCOVID()
    print(startIndex)
    for item in range(startIndex, startIndex + 25):
        cur.execute("INSERT INTO covidData (uniq, date, new_cases, new_deaths, vax_init, vax_complete) VALUES (?, ?, ?, ?, ?, ?)", (uniqs[item], date[item], new_cases[item], new_deaths[item], vax_init[item], vax_complete[item]))
    conn.commit()

def CalcStocktoCase(cur, conn, f):
    path = os.path.dirname(os.path.abspath(__file__))
    cur.execute("SELECT StocksInfo.stock_id, covidData.date, StocksInfo.high, StocksInfo.low, covidData.new_cases FROM StocksInfo JOIN covidData ON StocksInfo.date=covidData.date")
    data = cur.fetchall()
    with open (path+'/'+'calculations.txt', 'w') as f:
        f.write('stockName, date, High price per new COVID case')
        f.write('\n')
        for tup in data:
            cur.execute("SELECT Stocks.name FROM Stocks WHERE Stocks.id=?", (tup[0], ))
            stock_name = cur.fetchall()[0]
            date = tup[1]
            # stock_dif = tup[2] - tup[3]
            new_cases = tup[4]
            stock_price_to_cases = tup[2]/new_cases
            f.write(str(stock_name[0]) + ", " + str(date) + ", " + str(stock_price_to_cases))
            f.write('\n')

def main():
    cur, conn = setUpDb('covid.db')
    cur.execute('CREATE TABLE IF NOT EXISTS covidData (uniq INTEGER UNIQUE, date INTEGER, new_cases INTEGER, new_deaths INTEGER, vax_init INTEGER, vax_complete INTEGER)')
    cur.execute('SELECT max (uniq) from covidData')
    startIndex = cur.fetchone()[0]
    print(startIndex)
    if startIndex == None:
        startIndex = 0
    createDb1(cur, conn, startIndex)

    CalcStocktoCase(cur, conn, 'calculations.txt')
    

if __name__ == "__main__":
    main()
