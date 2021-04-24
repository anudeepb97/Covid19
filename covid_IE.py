import requests
import json
from datetime import date, datetime, timedelta
import time
import pandas as pd

url = "https://covid-193.p.rapidapi.com/history"
headers = {
#visit https://rapidapi.com/api-sports/api/COVID-19 and get yourself a rapidapi-key to access more!
    'x-rapidapi-key': "###############################",
    'x-rapidapi-host': "covid-193.p.rapidapi.com"
}

start = date(2020,3,21)
end = date(2021,4,24)
delta = timedelta(days=1)

# Response<tag> related
continent, country = [], []
# Cases
population, new_cases, active, critical, recovered, total_cases, cases_1M_pop = [], [], [], [], [], [], []
# Deaths
new_deaths, deaths_1M_pop, total_deaths = [], [], []
# Tests
tests_1M_pop, total_tests = [], []
# Datetime
dday, dtime = [], []

# my = pd.DataFrame()
try:
    while start <= end:
        date2 = start + delta
        querystring = {"country": "Ireland", "day": date2}
        res = requests.request("GET", url, headers=headers, params=querystring)
        data = res.text
        parsed = json.loads(data)
        print(json.dumps(parsed, indent=4))

        continent.append(parsed["response"][-1]["continent"])
        country.append(parsed["response"][-1]["country"])
        population.append(parsed["response"][-1]["population"])
        # Cases
        new_cases.append(parsed["response"][-1]["cases"]["new"])
        active.append(parsed["response"][-1]["cases"]["active"])
        critical.append(parsed["response"][-1]["cases"]["critical"])
        recovered.append(parsed["response"][-1]["cases"]["recovered"])
        cases_1M_pop.append(parsed["response"][-1]["cases"]["1M_pop"])
        total_cases.append(parsed["response"][-1]["cases"]["total"])
        # Deaths
        new_deaths.append(parsed["response"][-1]["deaths"]["new"])
        deaths_1M_pop.append(parsed["response"][-1]["deaths"]["1M_pop"])
        total_deaths.append(parsed["response"][-1]["deaths"]["total"])
        # Tests
        tests_1M_pop.append(parsed["response"][-1]["tests"]["1M_pop"])
        total_tests.append(parsed["response"][-1]["tests"]["total"])
        # Datetime
        dday.append(parsed["response"][-1]["day"])
        dtime.append(parsed["response"][-1]["time"])

        # continent.append(data['response'][0]['continent'])
        # print(parsed['response'][0])
        print('Success')
        time.sleep(1)
        start = date2
except IndexError:
    print('Out of bound')

print(continent, country, population, new_cases, active, critical, recovered, total_cases)
print('Deaths\n')
print(new_deaths, deaths_1M_pop, total_deaths)
print('Tests\n')
print(tests_1M_pop, total_tests)
print('Datetime\n')
print(dday, dtime)

covid_data = pd.DataFrame(data={'continent': continent, 'country': country, 'population': population,
                                'new_cases': new_cases, 'active_cases': active, 'critical': critical,
                                'recovered': recovered, 'cases_1M_pop': cases_1M_pop, 'total_cases': total_cases,
                                'new_deaths': new_deaths, 'deaths_1M_pop': deaths_1M_pop, 'total_deaths': total_deaths,
                                'tests_1M_pop': tests_1M_pop, 'total_tests': total_tests,
                                'dday': dday, 'dtime': dtime
                                })

ttime = []
for i in range(len(covid_data)):
    head, i, tail = str(covid_data['dtime'][i]).partition('T')
    ttime.append(tail)
print(ttime)
covid_data['dtime'] = ttime
print(covid_data.head())

covid_data.to_csv('data.csv')
