# Using the following API: https://aqicn.org/api/
# Supporting info: https://aqicn.org/data-platform/token-confirm/e12775d2-4859-4f24-85d4-84496895705b 
# Documentation: https://aqicn.org/json-api/doc/ 

import sqlite3
import requests
import json
import os

def getWeather():
    cities_list = ['New York City', 'Detroit', 'Los Angeles']
    api_token = '9187b27bfa98fa2802c18766633f291fdfefb9bb'
    cleaned_cities_dict = {}

    for i in range(len(cities_list)):
        base_url = "https://api.waqi.info/feed/{}/?token={}"
        new_url = base_url.format(cities_list[i], api_token)
        data = requests.get(new_url)
        info_dict = json.loads(data.text)

        city = cities_list[i]
        metrics_of_interest = {'status':'', 'carbon_monoxide':0, 'ozone':0, 'pm25':0}
        metrics_of_interest['status'] = info_dict['status']
        metrics_of_interest['carbon_monoxide'] = info_dict['data']['iaqi']['co']['v']
        metrics_of_interest['ozone'] = info_dict['data']['iaqi']['o3']['v']
        metrics_of_interest['pm25'] = info_dict['data']['iaqi']['pm25']['v']

        cleaned_cities_dict[city] = metrics_of_interest
    
    return cleaned_cities_dict
    


def main():
    cleaned_cities_dict = getWeather()
    print(cleaned_cities_dict)

if __name__ == "__main__":
    main()