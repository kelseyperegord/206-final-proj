import requests
import json
import re
import os
import sqlite3


def getDataFromCOVID():
    # Los Angeles, San Diego, San Jose
    # Chicago, Detroit, Minneapolis
    # New York City, Philadelphia, Charlotte
    # city information, for that city, at that month what the total amount of cases

    lst_of_lsts = []
    
    base_url = 'https://api.covidactnow.org/v2/country/US.timeseries.json?apiKey=058ae95db40f49de9aa59c9c3b5ca56e'
    data = requests.get(base_url)
    info = json.loads(data.text)
    reversed_lst = list(reversed(info['actualsTimeseries']))
    i = 102
    curr_initiated_vax = reversed_lst[101]['vaccinationsInitiated']
    curr_completed_vax = reversed_lst[101]['vaccinationsCompleted']

    while i >= 3:
        if reversed_lst[i]['vaccinationsInitiated'] == None:
            vax_init_per_day = 0
            vax_complete_per_day = 0
        else:
            vax_init_per_day = int(curr_initiated_vax) - int(reversed_lst[i]['vaccinationsInitiated'])
            vax_complete_per_day = int(curr_completed_vax) - int(reversed_lst[i]['vaccinationsCompleted'])
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
        tup = (new_date, new_cases, new_deaths, vax_init_per_day, vax_complete_per_day)
        lst_of_lsts.append(tup)
        i -= 1
    return lst_of_lsts
            
            
        # curr_lst = []
        # for day in info['metricsTimeseries']:
        #     regex = r'\d{4}\-\d{2}\-15'
        #     if day['date'] == '2021-04-15':
        #         break
        #     if_true = re.findall(regex, day['date'])
        #     if len(if_true) > 0:
        #         curr_day = if_true[0]
        #         curr_mon = if_true[0][6]
        #         curr_testPositive = day['testPositivityRatio']
        #         curr_caseDens = day['caseDensity']
        #         tup = (airport_codes[i], curr_day, curr_mon, curr_testPositive, curr_caseDens)
        #         curr_lst.append(tup)
        # lst_of_lsts.append(curr_lst)
    #return lst_of_lsts
    pass

data = getDataFromCOVID()
print(len(data))
print(data[0])

def getDataFromHoliday():
    years = ['2020','2021']
    holidays = {}
    for year in years:
        if year == '2020':
            for month in range(3,13):
                base_url = 'https://holidays.abstractapi.com/v1/?api_key={}country=US&year=2020&month={}'
                new_url = base_url.format('d8bb9016fdd749ebb81a779a4f9a93ba', month)
                data = requests.get(new_url)
                info = json.loads(data.text)
                count = 0
                curr_lst = []
                for holiday in info:
                    return holiday
                    if holiday['type'] == 'Observance':
                        count += 1
                        curr_date = holiday['date']
                        curr_lst.append(curr_date)
                new_lst = []
                new_lst.append(count)
                new_lst.append(curr_lst)
                holidays[month] = new_lst
        if year == '2021':
            for month in range(1,3):
                base_url = 'https://holidays.abstractapi.com/v1/?api_key={}country=US&year=2021&month={}'
                new_url = base_url.format('d8bb9016fdd749ebb81a779a4f9a93ba', month)
                data = requests.get(new_url)
                info = json.loads(data.text)
                count = 0
                curr_lst = []
                for holiday in info:
                    if holiday['type'] == 'Observance':
                        count += 1
                        curr_date = holiday['date']
                        curr_lst.append(curr_date)
                new_lst = []
                new_lst.append(count)
                new_lst.append(curr_lst)
                holidays[month] = new_lst
    return holidays

    #     new_url = base_url.format('bb6334af-eaa6-4707-846e-3224f9a0d460', year)
    #     base_url = 'https://holidayapi.com/v1/holidays?pretty&key={}&country=US&year={}'
    #     new_url = base_url.format('bb6334af-eaa6-4707-846e-3224f9a0d460', year)
    #     data = requests.get(new_url)
    #     info = json.loads(data.text)
    #     for holiday in info['holidays']:
    #         if year == '2020':
    #             regex_str = r'\d{4}\-\b(?:0[3-9]|1[0-2])\b\-\d{2}'
    #             if_true = re.findall(regex_str, holiday['date'])
    #             if len(if_true) > 0:
    #                 if holiday['public'] == True:
    #                     curr_date = holiday['date']
    #                     curr_name = holiday['name']
    #                     curr_month = holiday['date'][6:8]
    #                     tup = (curr_month, curr_date, curr_name)
    #                     holidays.append(tup)
    #         elif year == '2021':
    #             regex_str = r'\d{4}\-\d{2}-\d{2}'
    #             if_true = re.findall(regex_str, holiday['date'])
    #             print(if_true)
    #             if len(if_true) > 0:
    #                 if holiday['public'] == True:
    #                     curr_date = holiday['date']
    #                     curr_name = holiday['name']
    #                     curr_month = holiday['date'][6:8]
    #                     tup = (curr_month, curr_date, curr_name)
    #                     holidays.append(tup)
    return holidays

        


def setUpDb(f_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+f_name)
    cur = conn.cursor()
    pass
    return cur, conn

def createDb(curr, conn, startIndex):
    pass

def main():
    pass
    #getDataFromAPI()
    cur, conn = setUpDb('covid.db')
    cur.execute('CREATE TABLE IF NOT EXISTS ')

    




    

    

    
