#!/usr/local/bin/python3

import sys, urllib3, json, locale
from datetime import date

locale.setlocale(locale.LC_ALL, '')
today = date.today()

http = urllib3.PoolManager()
args = sys.argv

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class api():
    GLOBAL = 'https://covidapi.info/api/v1/global'
    COUNTRY = 'https://covidapi.info/api/v1/country/{iso}/latest'
    COUNTRY_INFO = 'https://restcountries.eu/rest/v2/alpha/co'

def result(url):
    res = http.request('GET', url)
    if res.status is not 200:
        raise Exception("Cannot read from the given url")

    return json.loads(str(res.data.decode('utf-8')))

def syserr(message):
    sys.stderr.write(bcolors.FAIL + message + '\n')

def sysout(output = ''):
    sys.stdout.write(output + '\n')

def stats(api):
    try:
        res = result(api)
        res = res['result']

        if 'confirmed' not in res:
            item = list(res)[0]
            res = res[item]

        confirmed = int(res['confirmed'])
        deaths = int(res['deaths'])
        recovered = int(res['recovered'])

        sysout(bcolors.OKBLUE + 'Confirmed\t: ' + '{:,}'.format(confirmed))
        sysout(bcolors.FAIL + 'Deaths\t\t: ' + '{:,}'.format(deaths))
        sysout(bcolors.OKGREEN + 'Recovered\t: ' + '{:,}'.format(recovered))
    except Exception as e:
        syserr(str(e))

def country_info(country):
    return result('https://restcountries.eu/rest/v2/alpha/' + country)

if len(args) == 1:
    stats(api.GLOBAL)
elif len(args) == 2:
    try:
        info = country_info(args.pop().lower())
        sysout(bcolors.HEADER + 'Statistics for ' + info['name'])
        sysout()
        stats(api.COUNTRY.format(iso=info['alpha3Code']))
    except Exception as e:
        sysout(str(e))

