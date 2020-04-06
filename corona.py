#!/usr/local/bin/python3

import json
import locale
import sys
import urllib3
from datetime import date

locale.setlocale(locale.LC_ALL, '')
today = date.today()

http = urllib3.PoolManager()
args = sys.argv


class cli_colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class api_endpoints():
    GLOBAL = 'https://covidapi.info/api/v1/global'
    COUNTRY = 'https://covidapi.info/api/v1/country/{iso}/latest'
    COUNTRY_INFO = 'https://restcountries.eu/rest/v2/alpha/{iso}'


def result(url):
    res = http.request('GET', url)
    if res.status is not 200:
        raise Exception("Cannot read from the given url")

    return json.loads(str(res.data.decode('utf-8')))


def syserr(message):
    sys.stderr.write(cli_colors.FAIL + message + '\n')


def sysout(output=''):
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

        sysout(cli_colors.OKBLUE + 'Confirmed\t: ' + '{:,}'.format(confirmed))
        sysout(cli_colors.FAIL + 'Deaths\t\t: ' + '{:,}'.format(deaths))
        sysout(cli_colors.OKGREEN + 'Recovered\t: ' + '{:,}'.format(recovered))
    except Exception as e:
        syserr(str(e))


def country_info(country):
    return result(api_endpoints.COUNTRY_INFO.format(iso=country))


if len(args) == 1:
    stats(api_endpoints.GLOBAL)
elif len(args) == 2:
    try:
        info = country_info(args.pop().lower())
        sysout(cli_colors.HEADER + 'Statistics for ' + info['name'])
        sysout()
        stats(api_endpoints.COUNTRY.format(iso=info['alpha3Code']))
    except Exception as e:
        syserr(str(e))
