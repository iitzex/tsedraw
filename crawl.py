# -*- coding: utf-8 -*-
import csv
import time
import logging
import requests
import argparse
from lxml import html
from datetime import datetime, timedelta
from os import mkdir
from os.path import isdir


class Crawler():
    def __init__(self, prefix="data"):
        """ Make directory if not exist when initialize """
        if not isdir(prefix):
            mkdir(prefix)
        self.prefix = prefix

    def _clean_row(self, row):
        """ Clean comma and spaces """
        for index, content in enumerate(row):
            row[index] = content.replace(',', '')
        return row

    def _record(self, stock_id, row):
        """ Save row to csv file """
        f = open('{}/{}.csv'.format(self.prefix, stock_id), 'a')
        import os
        s = os.stat('{}/{}.csv'.format(self.prefix, stock_id))
        if s.st_size == 0:
            f.write('date,amount,volume,open,high,low,close,diff,number\n')
        cw = csv.writer(f, lineterminator='\n')
        cw.writerow(row)
        f.close()

    def _get_tse_data(self, date_str):
        payload = {
            'download': '',
            'qdate': date_str,
            # 'selectType': 'ALL'
            'selectType': 'ALLBUT0999'
        }
        url = 'http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX.php'

        # Get html page and parse as tree
        page = requests.post(url, data=payload)

        if not page.ok:
            logging.error("Can not get TSE data at {}".format(date_str))
            return

        # Parse page
        tree = html.fromstring(page.text)

        for tr in tree.xpath('//table[2]/tbody/tr'):
            tds = tr.xpath('td/text()')
            # self.get_stocklist(tds)

            sign = tr.xpath('td/font/text()')
            sign = '-' if len(sign) == 1 and sign[0] == u'－' else ''

            # print(self.year.__str__() + self.month.__str__())
            date_str = '{0}-{1:02d}-{2:02d}'.format(self.year, self.month, self.day)
            row = self._clean_row([
                date_str,  # 日期
                tds[2],  # 成交股數
                tds[4],  # 成交金額
                tds[5],  # 開盤價
                tds[6],  # 最高價
                tds[7],  # 最低價
                tds[8],  # 收盤價
                sign + tds[9],  # 漲跌價差
                tds[3],  # 成交筆數
            ])

            self._record(tds[0].strip(), row)

    # def get_stocklist(self, tds):
    #     fp = open('stocklist.csv', 'a')
    #     fp.write('{}, {}\n'.format(tds[0].strip(), tds[1].strip()))
    #     print('{}, {}'.format(tds[0].strip(), tds[1].strip()))
    #     fp.close()

    def _get_otc_data(self, date_str):
        ttime = str(int(time.time()*100))
        url = 'http://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_result.php?l=zh-tw&d={}&_={}'.format(date_str, ttime)
        page = requests.get(url)

        if not page.ok:
            logging.error("Can not get OTC data at {}".format(date_str))
            return

        result = page.json()

        if result['reportDate'] != date_str:
            logging.error("Get error date OTC data at {}".format(date_str))
            return

        for table in [result['mmData'], result['aaData']]:
            for tr in table:
                date_str = '{0}-{1:02d}-{2:02d}'.format(self.year, self.month, self.day)
                row = self._clean_row([
                    date_str,
                    tr[8],  # 成交股數
                    tr[9],  # 成交金額
                    tr[4],  # 開盤價
                    tr[5],  # 最高價
                    tr[6],  # 最低價
                    tr[2],  # 收盤價
                    tr[3],  # 漲跌價差
                    tr[10]  # 成交筆數
                ])
                self._record(tr[0], row)

    def get_data(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

        date_str = '{0}/{1:02d}/{2:02d}'.format(year - 1911, month, day)
        print('Crawling {}'.format(date_str))
        self._get_tse_data(date_str)
        self._get_otc_data(date_str)


def main():
    parser = argparse.ArgumentParser(description='Crawl data at assigned day')
    parser.add_argument('day', type=int, nargs='*', help='assigned day (format: YYYY MM DD), default is today')
    parser.add_argument('-b', '--back', action='store_true', help='crawl back from assigned day until 2004/2/11')
    parser.add_argument('-c', '--check', action='store_true', help='crawl the assigned day')

    args = parser.parse_args()
    print(args)

    crawler = Crawler()
    end = datetime.today()

    try:
        if args.back:
            begin = datetime(args.day[0], args.day[1], args.day[2])
        elif args.check:
            begin = datetime(args.day[0], args.day[1], args.day[2])
            end = begin
        else:
            begin = datetime.today()
    except IndexError:
        parser.error('Date should be assigned with (YYYY MM DD) or none')
        return

    print('BEGIN: ' + begin.__str__())
    print('END  : ' + end.__str__())

    if args.back or args.check:        # otc first day is 2007/04/20 # tse first day is 2004/02/11
        max_error = 5
        error = 0

        while error < max_error and end >= begin:
            try:
                crawler.get_data(begin.year, begin.month, begin.day)
                error = 0
            except OSError:
                date_str = begin.strftime('%Y/%m/%d')
                # logging.error('Crawl raise error {}'.format(date_str))
                logging.error('Crawl raise error {} {} {}'.format(begin.year, begin.month, begin.day))
                error += 1
                continue
            finally:
                begin += timedelta(1)
    else:
        crawler.get_data(end.year, end.month, end.day)


def auto_crawl():
    with open('data/0050.csv', 'r') as f:
        last_line = f.readlines()[-1]
        last_day = last_line.split(',')[0]
        begin = datetime.strptime(last_day, '%Y-%m-%d')
        begin += timedelta(1)
    end = datetime.today()

    crawler = Crawler()

    max_error = 5
    error = 0

    print('BEGIN: ' + begin.__str__())
    print('END  : ' + end.__str__())

    while error < max_error and end >= begin:
        try:
            crawler.get_data(begin.year, begin.month, begin.day)
            error = 0
        except OSError:
            date_str = begin.strftime('%Y/%m/%d')
            # logging.error('Crawl raise error {}'.format(date_str))
            logging.error('Crawl raise error {} {} {}'.format(begin.year, begin.month, begin.day))
            error += 1
            continue
        finally:
            begin += timedelta(1)

if __name__ == '__main__':
    # main()
    auto_crawl()

