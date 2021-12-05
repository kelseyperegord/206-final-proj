import requests
import json
import re

def getDataFromAPIs():
    cbsa_codes = ['12060', '19100', '19740']
    airport_codes = ['ATL', 'DFW', 'DEN']
    lst_of_lsts = []
    for i in range(len(cbsa_codes)):
        base_url = 'https://api.covidactnow.org/v2/cbsa/{}.timeseries.json?apiKey={}'
        new_url = base_url.format(cbsa_codes[i], '058ae95db40f49de9aa59c9c3b5ca56e')
        print(new_url)
        data = requests.get(new_url)
        info = json.loads(data.text)
        curr_lst = []
        for day in info['metricsTimeseries']:
            regex = r'\d{4}\-\d{2}\-15'
            if day['date'] == '2021-04-15':
                break
            if_true = re.findall(regex, day['date'])
            if len(if_true) > 0:
                curr_day = if_true[0]
                curr_testPositive = day['testPositivityRatio']
                curr_caseDens = day['caseDensity']
                tup = (airport_codes[i], curr_day, curr_testPositive, curr_caseDens)
                curr_lst.append(tup)
        lst_of_lsts.append(curr_lst)
    return lst_of_lsts




data = getDataFromAPIs()
for stuff in data:
    print(stuff)
    print('\n')




    

    

    
