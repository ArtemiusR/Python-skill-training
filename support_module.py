import requests
import time
import datetime
import pandas as pd
import os
import json


class URLParse:

    def __init__(self, url=None):
        self.url = url

    @staticmethod
    def get_name(splitted, data_dict):
        idx = splitted.index('<div class="instrumentHead">') + 1
        b = splitted[idx]
        c = b.find('\"name\">')
        d = b.find('</h1>')
        name = b[c + 7:d - 1]
        data_dict['name'] = name

    @staticmethod
    def get_pair_id(raw_site, data_dict):
        idx = raw_site.index(r'pair-id="') + 9
        d = raw_site[idx:].index(r'"')
        pair_id = raw_site[idx:idx + d]
        data_dict['pair_id'] = pair_id

    @staticmethod
    def get_price(splitted, data_dict):
        idx = splitted.index('<div class="top bold inlineblock">') + 1
        b = splitted[idx]
        c = b.find('dir="ltr">')
        d = b.find('</span>')
        price = b[c + 10:d]
        data_dict['price'] = price.replace('.', '').replace(',', '.')

    @staticmethod
    def get_currency(splitted, data_dict):
        idx = splitted.index('<div class="bottom lighterGrayFont arial_11">') + 2
        b = splitted[idx]
        c = b.find('Цена в <span class=\'bold\'>')
        d = b[c + 26:].find('</span>')
        currency = b[c + 26:c + 26 + d]
        data_dict['currency'] = currency

    @staticmethod
    def get_ma(splitted, data_dict):
        idx = splitted.index('<div class="newTechStudiesRight instrumentTechTab" id="techStudiesInnerWrap">') + 2
        b = splitted[idx]
        c = b.index('<i id="maBuy">(')
        d = b[c + 15:].index(')</i>')
        ma_buy = int(b[c + 15:c + 15 + d])
        data_dict['1hr maBuy'] = ma_buy
        c = b.index('<i id="maSell">(')
        d = b[c + 16:].index(')</i>')
        ma_sell = int(b[c + 16:c + 16 + d])
        data_dict['1hr maSell'] = ma_sell
        data_dict['1hr MA'] = ma_buy - ma_sell

    @staticmethod
    def get_ti(splitted, data_dict):
        idx = splitted.index('<div class="newTechStudiesRight instrumentTechTab" id="techStudiesInnerWrap">') + 3
        b = splitted[idx]
        c = b.index('<i id="tiBuy">(')
        d = b[c + 15:].index(')</i>')
        ti_buy = int(b[c + 15:c + 15 + d])
        data_dict['1hr tiBuy'] = ti_buy
        c = b.index('<i id="tiSell">(')
        d = b[c + 16:].index(')</i>')
        ti_sell = int(b[c + 16:c + 16 + d])
        data_dict['1hr tiSell'] = ti_sell
        data_dict['1hr TI'] = ti_buy - ti_sell
        data_dict['1hr SUM'] = data_dict['1hr MA'] + data_dict['1hr TI']

    @staticmethod
    def get_ma_dim(raw_site, data_dict, timings, i):
        idx = raw_site.index('<i id="maBuy">(') + 15
        d = raw_site[idx:].index(')</i>')
        ma_buy = int(raw_site[idx:idx + d])
        data_dict[timings[i][0] + ' maBuy'] = ma_buy
        idx = raw_site.index('<i id="maSell">(') + 16
        d = raw_site[idx:].index(')</i>')
        ma_sell = int(raw_site[idx:idx + d])
        data_dict[timings[i][0] + ' maSell'] = ma_sell
        data_dict[timings[i][0] + ' MA'] = ma_buy - ma_sell

    @staticmethod
    def get_ti_dim(raw_site, data_dict, timings, i):
        idx = raw_site.index('<i id="tiBuy">(') + 15
        d = raw_site[idx:].index(')</i>')
        ti_buy = int(raw_site[idx:idx + d])
        data_dict[timings[i][0] + ' tiBuy'] = ti_buy
        idx = raw_site.index('<i id="tiSell">(') + 16
        d = raw_site[idx:].index(')</i>')
        ti_sell = int(raw_site[idx:idx + d])
        data_dict[timings[i][0] + ' tiSell'] = ti_sell
        data_dict[timings[i][0] + ' TI'] = ti_buy - ti_sell
        data_dict[timings[i][0] + ' SUM'] = data_dict[timings[i][0] + ' MA'] + data_dict[timings[i][0] + ' TI']

    def parse(self, s):
        data_dict = {'name': None, 'pair_id': None, 'price': None, 'currency': None,
                     'Overall SUM': None, '1hr SUM': None, '5hr SUM': None, '1d SUM': None, '1w SUM': None,
                     '1m SUM': None,
                     '1hr maBuy': None, '1hr maSell': None, '1hr MA': None, '1hr tiBuy': None, '1hr tiSell': None,
                     '1hr TI': None,
                     '5hr maBuy': None, '5hr maSell': None, '5hr MA': None, '5hr tiBuy': None, '5hr tiSell': None,
                     '5hr TI': None,
                     '1d maBuy': None, '1d maSell': None, '1d MA': None, '1d tiBuy': None, '1d tiSell': None,
                     '1d TI': None,
                     '1w maBuy': None, '1w maSell': None, '1w MA': None, '1w tiBuy': None, '1w tiSell': None,
                     '1w TI': None,
                     '1m maBuy': None, '1m maSell': None, '1m MA': None, '1m tiBuy': None, '1m tiSell': None,
                     '1m TI': None,
                     }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/92.0.4515.131 Safari/537.36'}
        headers2 = {
            'accept': '*/*',
            'authority': 'ru.investing.com',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://ru.investing.com',
            'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/92.0.4515.131 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        timings = {0: ['5hr', '18000'], 1: ['1d', '86400'], 2: ['1w', 'week'], 3: ['1m', 'month']}

        result = s.get(self.url, headers=headers, timeout=10)
        raw_site = result.text
        splitted = tuple(raw_site.splitlines())

        self.get_name(splitted, data_dict)
        self.get_pair_id(raw_site, data_dict)
        self.get_price(splitted, data_dict)
        self.get_currency(splitted, data_dict)
        self.get_ma(splitted, data_dict)
        self.get_ti(splitted, data_dict)

        for i in range(4):
            body = 'pairID=' + data_dict['pair_id'] + '&period=' + timings[i][1] + '&viewType=normal'
            result = s.post('https://ru.investing.com/instruments/Service/GetTechincalData', headers=headers2,
                            data=body, timeout=10)
            raw_site = result.text
            self.get_ma_dim(raw_site, data_dict, timings, i)
            self.get_ti_dim(raw_site, data_dict, timings, i)

        data_dict['Overall SUM'] = data_dict['1hr SUM'] + data_dict['5hr SUM'] + data_dict['1d SUM'] + data_dict[
            '1w SUM'] + data_dict['1m SUM']
        return data_dict


class RefList:

    def __init__(self, name=None):
        self.name = str(name)
        self.ref_list = []
        self.url = ''
        self.extract()

    def getlist(self, url):

        string_data = ''
        self.url = str(url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/92.0.4515.131 Safari/537.36'}
        result = requests.get(url, headers=headers)
        if result.status_code != 200:
            raise ConnectionError
        raw_site = result.content.decode()
        a = raw_site.splitlines()
        for string in a:
            if '><table id=\"cross_rate_markets_stocks_1\"' in string:
                string_data = string

        urls = []
        url_technicals = []
        while '<a href=\"' in string_data:
            b = string_data.find('<a href=\"')
            string_data = string_data[b + 10:]
            c = string_data.find('\"')
            urls.append(string_data[:c])

        for i in range(len(urls)):
            urls[i] = r'https://ru.investing.com/' + urls[i]
            if '?cid' in urls[i]:
                pos = urls[i].index('?cid')
                url_technicals.append(urls[i][:pos] + '-technical' + urls[i][pos:])
            else:
                url_technicals.append(urls[i] + '-technical')

        self.ref_list = url_technicals

    def print_list(self):
        if not self.ref_list:
            print('Список пуст')
        else:
            for url in self.ref_list:
                print(url)

    def __str__(self):
        a = self.name + '\n'
        for i in self.ref_list:
            a = a + i + '\n'
        return a

    def write(self):
        with open(self.name + '_refs.txt', 'w') as f:
            for ref in self.ref_list:
                f.write(ref + '\n')

    def extract(self):
        self.ref_list = []
        try:
            with open(self.name + '_refs.txt', 'r') as f:
                for line in f.read().splitlines():
                    self.ref_list.append(line)
        except FileNotFoundError:
            self.ref_list = []

    def join(self, market):
        with open(market.name + '_refs.txt', 'r') as f:
            url_list = f.read().splitlines()
        with open(self.name + '_refs.txt', 'r') as f:
            url_list2 = f.read().splitlines()
        with open(market.name + '+' + self.name + '_refs.txt', 'w') as f:
            for url in url_list:
                f.write(url + '\n')
            for url in url_list2:
                if url not in url_list:
                    f.write(url + '\n')
        with open(market.name + '+' + self.name + '_refs.txt', 'r') as f:
            url_list3 = f.read().splitlines()
        return url_list3


def get_table(market):
    start = time.time()
    temp_dict = []
    a = URLParse()
    s = requests.Session()
    for ref in market.ref_list:
        a.url = ref
        try:
            temp_dict.append(a.parse(s))
        except ValueError:
            try:
                time.sleep(5)
                temp_dict.append(a.parse(s))
            except ValueError:
                time.sleep(60)
                temp_dict.append(a.parse(s))

    final_dict = dict.fromkeys(list(temp_dict[0]), [])
    for bar in list(temp_dict[0]):
        listt = []
        for foo in range(len(temp_dict)):
            listt.append(temp_dict[foo][bar])
        final_dict[bar] = listt

    table_all = pd.DataFrame(data=final_dict)
    table_all.to_csv('technical_log\\' + datetime.datetime.now().strftime("%Y-%m-%d %H-%M") + '.csv', index=False)
    print('Данные технического анализа по ' + market.name + ' успешно загружены')

    with open('log.txt', 'a') as f:
        f.write(
            str(datetime.datetime.now()) + '    Данные технического анализа по ' + market.name + ' успешно загружены\n')

    end = time.time()
    print(f'Runtime of the program is {end - start}')
    print(datetime.datetime.now())

    return table_all


class Table:

    def __init__(self, table):
        self.table = table
        self.target_buy = {}
        self.target_sell = {}

    def initialize_graphs(self):
        a = self.table
        a = a['name'].to_list()
        b = pd.DataFrame(
            data={'datetime': [], 'price': [], 'Overall SUM': [], '1hr SUM': [], '5hr SUM': [], '1d SUM': [],
                  '1w SUM': [], '1m SUM': [], })
        for foo in a:
            os.mkdir('technical_log\\graphs\\' + foo + '\\')
            b.to_csv('technical_log\\graphs\\' + foo + '\\' + foo + '.csv', index=False)

    def add_to_graphs(self):
        a = self.table
        b = a['name'].to_list()
        for foo in b:
            c = pd.read_csv('technical_log\\graphs\\' + foo + '\\' + foo + '.csv')
            d = a.loc[a.name == foo, ['price', 'Overall SUM', '1hr SUM', '5hr SUM', '1d SUM', '1w SUM', '1m SUM']]
            d['datetime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            e = c.append(d)
            e.to_csv('technical_log\\graphs\\' + foo + '\\' + foo + '.csv', index=False)

    def check_target_buy(self, lim_sum):
        if type(lim_sum) != str:
            lim_sum = str(lim_sum)

        with open('target_buy'+lim_sum+'.json', 'r') as f:
            self.target_buy = json.load(f)
            assert type(self.target_buy) == dict

        a = self.table
        b = self.table.loc[self.table['Overall SUM'] >= int(lim_sum), ['name', 'price', 'currency', 'Overall SUM']]

        with open('target_log'+lim_sum+'.txt', 'a') as f:
            for bar in list(self.target_buy.keys()):
                if bar not in b.name.to_list():
                    dict_for_log = {
                        'datetime': str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                        'move': 'stop_buy' + lim_sum,
                        'name': str(a.loc[a.name == bar].iloc[0, 0]),
                        'delta': str((-float(self.target_buy[bar][1]) + float(a.loc[a.name == bar].iloc[0, 2])) / float(
                            self.target_buy[bar][1]) * 100),
                        'time_delta': str(datetime.datetime.now() - datetime.datetime.strptime(self.target_buy[bar][3],
                                                                                               '%Y-%m-%d %H:%M:%S.%f')),
                        'final_osum': str(a.loc[a.name == bar].iloc[0, 4])
                    }

                    text = str(dict_for_log['datetime'] + '\t' + 'STOP BUY\tFinal OSUM = ' + dict_for_log[
                        'final_osum'] + '\t' +
                               dict_for_log['name'] + '    ' + 'delta = ' + dict_for_log['delta'] + '    ' +
                               'time passed = ' + dict_for_log['time_delta'] + '\n')

                    f.write(text)
                    print(text)
                    del self.target_buy[bar]
                    log_csv = pd.read_csv('targets_log.csv')
                    new_line = pd.DataFrame(data=dict_for_log, index=[0])
                    new_log_csv = log_csv.append(new_line)
                    new_log_csv.to_csv('targets_log.csv', index=False)

            for foo in b.index.to_list():
                if b.loc[foo, 'name'] not in self.target_buy:
                    f.write(str(datetime.datetime.now()) + '\t')
                    f.write('START BUY\tEntry OSUM = ' + str(b.loc[foo, 'Overall SUM']) + '\t' + b.loc[
                        foo, 'name'] + '\t' + str(b.loc[foo, 'price']) + ' ' + b.loc[foo, 'currency'] + '\n')
                    print('START BUY\tEntry OSUM = ' + str(b.loc[foo, 'Overall SUM']) + '\t' + b.loc[
                        foo, 'name'] + '\t' + str(b.loc[foo, 'price']) + ' ' + b.loc[foo, 'currency'] + '\n')
                    self.target_buy[b.loc[foo, 'name']] = [int(b.loc[foo, 'Overall SUM']), b.loc[foo, 'price'],
                                                           b.loc[foo, 'currency'], str(datetime.datetime.now())]

        with open('target_buy'+lim_sum+'.json', 'w') as f:
            json.dump(self.target_buy, f)

    def check_target_sell(self, lim_sum):
        if type(lim_sum) != str:
            lim_sum = str(lim_sum)
        with open('target_sell'+lim_sum+'.json', 'r') as f:
            self.target_sell = json.load(f)
            assert type(self.target_sell) == dict

        a = self.table
        b = self.table.loc[self.table['Overall SUM'] <= ((-1)*int(lim_sum)), ['name', 'price', 'currency', 'Overall SUM']]

        with open('target_log'+lim_sum+'.txt', 'a') as f:
            for bar in list(self.target_sell.keys()):
                if bar not in b.name.to_list():
                    dict_for_log = {
                        'datetime': str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                        'move': 'stop_sell' + lim_sum,
                        'name': str(a.loc[a.name == bar].iloc[0, 0]),
                        'delta': str((-float(self.target_sell[bar][1]) + float(a.loc[a.name == bar].iloc[0, 2])) / float(
                            self.target_sell[bar][1]) * 100),
                        'time_delta': str(datetime.datetime.now() - datetime.datetime.strptime(self.target_sell[bar][3],
                                                                                               '%Y-%m-%d %H:%M:%S.%f')),
                        'final_osum': str(a.loc[a.name == bar].iloc[0, 4])
                    }
                    text = str(dict_for_log['datetime'] + '\t' + 'STOP SELL\tFinal OSUM = ' + dict_for_log[
                        'final_osum'] + '\t' +
                               dict_for_log['name'] + '    ' + 'delta = ' + dict_for_log['delta'] + '    ' +
                               'time passed = ' + dict_for_log['time_delta'] + '\n')
                    f.write(text)
                    print(text)
                    del self.target_sell[bar]
                    log_csv = pd.read_csv('targets_log.csv')
                    new_line = pd.DataFrame(data=dict_for_log, index=[0])
                    new_log_csv = log_csv.append(new_line)
                    new_log_csv.to_csv('targets_log.csv', index=False)

            for foo in b.index.to_list():
                if b.loc[foo, 'name'] not in self.target_sell:
                    f.write(str(datetime.datetime.now()) + '\t')
                    f.write('START SELL\tEntry OSUM = ' + str(b.loc[foo, 'Overall SUM']) + '\t' + b.loc[foo, 'name'] +
                            '\t' + str(b.loc[foo, 'price']) + ' ' + b.loc[foo, 'currency'] + '\n')
                    print('START SELL\tEntry OSUM = ' + str(b.loc[foo, 'Overall SUM']) + '\t' + b.loc[foo, 'name'] +
                          '\t' + str(b.loc[foo, 'price']) + ' ' + b.loc[foo, 'currency'] + '\n')
                    self.target_sell[b.loc[foo, 'name']] = [int(b.loc[foo, 'Overall SUM']), b.loc[foo, 'price'],
                                                            b.loc[foo, 'currency'], str(datetime.datetime.now())]

        with open('target_sell'+lim_sum+'.json', 'w') as f:
            json.dump(self.target_sell, f)

