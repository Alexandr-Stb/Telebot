from exchangeRates import exchangeRatesMenu
import datetime
import urllib3
import xmltodict


try:
    now = datetime.datetime.now()
    url = f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={now.day}/0{now.month}/{now.year}"
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    data = xmltodict.parse(response.data)
except IOError as e:
    print(e)


def exchangeRates(rates: object, id):
    return rates['Valute'][findId(rates['Valute'], id)]


def findId(data: list, id):
    for i in range(len(data)):
        if data[i]['@ID'] == id:
            return i


def appendRate():
    usd = exchangeRates(data["ValCurs"], "R01235")
    eur = exchangeRates(data["ValCurs"], "R01239")
    gbr = exchangeRates(data["ValCurs"], "R01035")
    cny = exchangeRates(data["ValCurs"], "R01375")
    exchangeRatesMenu.rates.append(usd)
    exchangeRatesMenu.rates.append(eur)
    exchangeRatesMenu.rates.append(gbr)
    exchangeRatesMenu.rates.append(cny)


