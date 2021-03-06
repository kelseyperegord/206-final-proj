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
    # Reverses the list so that the subtractions will be correct
    reversed_lst = list(reversed(info['actualsTimeseries']))
    i = 102
    curr_initiated_vax = reversed_lst[103]['vaccinationsInitiated']
    curr_completed_vax = reversed_lst[103]['vaccinationsCompleted']
    x = 1
    # loops through the COVID time series and stores the date, new cases, vaccinations initiated, and vaccinations completed
    while i >= 3:
        if reversed_lst[i]['vaccinationsInitiated'] == None:
            vax_init_per_day = 0
            vax_complete_per_day = 0
        else:
            vax_init_per_day = abs(int(reversed_lst[i]['vaccinationsInitiated']) - int(curr_initiated_vax))
            vax_complete_per_day = abs(int(reversed_lst[i]['vaccinationsCompleted']) - int(curr_completed_vax))
            curr_initiated_vax = abs(reversed_lst[i]['vaccinationsInitiated'])
            curr_completed_vax = abs(reversed_lst[i]['vaccinationsCompleted'])
        
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

def setUpDb(f_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+f_name)
    cur = conn.cursor()
    return cur, conn

# Creates a table of the data from the COVID API
def createDb1(cur, conn, startIndex):
    uniqs, date, new_cases, new_deaths, vax_init, vax_complete = getDataFromCOVID()
    print(startIndex)
    for item in range(startIndex, startIndex + 25):
        cur.execute("INSERT INTO covidData (uniq, date, new_cases, new_deaths, vax_init, vax_complete) VALUES (?, ?, ?, ?, ?, ?)", (uniqs[item], date[item], new_cases[item], new_deaths[item], vax_init[item], vax_complete[item]))
    conn.commit()

def main():
    cur, conn = setUpDb('covid.db')
    cur.execute('CREATE TABLE IF NOT EXISTS covidData (uniq INTEGER UNIQUE, date INTEGER, new_cases INTEGER, new_deaths INTEGER, vax_init INTEGER, vax_complete INTEGER)')
    cur.execute('SELECT max (uniq) from covidData')
    startIndex = cur.fetchone()[0]
    print(startIndex)
    if startIndex == None:
        startIndex = 0
    createDb1(cur, conn, startIndex)

if __name__ == "__main__":
    main()



    




    

    

    
