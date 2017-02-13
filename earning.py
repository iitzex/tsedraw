# -*- coding: utf-8 -*-
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from util import get_list
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform
if platform.system() == 'Darwin':
    font = fm.FontProperties(fname='/System/Library/Fonts/STHeiti Medium.ttc')
else:
    font = fm.FontProperties(fname='/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc')


def gain(sid=None):
    ADDR='http://stock.wearn.com/income.asp?kind=' + str(sid)
    r = requests.get(ADDR)
    content = r.content.decode('Big5-HKSCS', errors='backslashreplace')
    soup = BeautifulSoup(content, "lxml")
    table = soup.find('table')

    date = []
    eps = []
    gross_margin = []
    profit_margin = []
    for i, tr in enumerate(table.find_all('tr', {'class': ['stockalllistbg1', 'stockalllistbg2']})):
        if i > 20:
            break
        td = tr.find_all('td', {'align': ['center', 'right']})
        m = re.match(r"(.*)年0(.*)季", td[0].get_text())
        year = int(m.group(1))
        season = int(m.group(2)) * 3

        date.append(datetime(year + 1911, season, 1))
        _eps = td[6].get_text().strip()
        if _eps == '':
            _eps = 0.0
        eps.append(float(_eps))
        gross_margin.append(float(td[2].get_text().replace(',', '').strip()[:-1]))
        profit_margin.append(float(td[3].get_text().replace(',', '').strip()[:-1]))

    d = {'eps': eps, 'gross_margin': gross_margin, 'profit_margin': profit_margin}
    df = pd.DataFrame(d, index=date)

    return df


def profit(sid):
    ADDR = 'http://easyfun.concords.com.tw/z/zc/zch/zch_' + str(sid) + '.djhtm'
    # print(ADDR)
    r = requests.get(ADDR)
    content = r.content.decode('Big5-HKSCS', errors='backslashreplace')
    soup = BeautifulSoup(content, "lxml")
    table = soup.find('table', id='oMainTable')
    # print(table)

    date = []
    revenue = []

    menu = table.find('tr', id="oScrollMenu")

    for i, tr in enumerate(menu.next_siblings):
        if tr == '\n':
            continue
        td = tr.find_all('td')

        year, month = td[0].get_text().split('/')
        date.append(datetime(int(year) + 1911, int(month), 1))

        value = td[1].get_text()
        if td[1].get_text() == '':
            value = '0'

        revenue.append(int(value.strip().replace(',', ''))/1000)

    d = {'revenue': revenue}
    df = pd.DataFrame(d, index=date)

    return df


def dividend(sid):
    ADDR = 'http://stock.wearn.com/dividend.asp?kind=' + str(sid)
    # print(ADDR)
    r = requests.get(ADDR)
    content = r.content.decode('Big5-HKSCS', errors='backslashreplace')
    soup = BeautifulSoup(content, "lxml")
    tr = soup.find('tr', {'class':"stockalllistbg2"})
    td = tr.find_all('td')
    # print(td[5].get_text().strip())
    return td[5].get_text().strip()


def drawing(df, df_revenue, df_gain, sid, title=None):
    row = 3
    fig, axes = plt.subplots(nrows=row, ncols=1, figsize=(16, 10))
    axes[0].bar(df_revenue.index, df_revenue.revenue, width=10, color='#FFC107', edgecolor='#FFA000', alpha=0.5)
    axes[0].yaxis.tick_right()
    ax = axes[0].twinx()
    ax.plot(df.index, df.close, 'r', alpha=0.7, linewidth=2)
    ax.set_title('Revenue', loc='right')
    axes[0].set_title('{} {}'.format(sid, title), fontproperties=font)

    axes[1].plot(df_gain.index, df_gain.gross_margin, color='#00695c', alpha=0.7, linewidth=2, zorder=2)
    axes[1].plot(df_gain.index, df_gain.profit_margin, color='#1565c0', alpha=0.7, linewidth=2, zorder=2)
    axes[1].set_title('Gross/Profit Margin', loc='right')
    axes[1].yaxis.tick_right()
    ax = axes[1].twinx()
    ax.plot(df.index, df.close, 'r', alpha=0.2, linewidth=2, zorder=1)

    axes[2].bar(df_gain.index, df_gain.eps, width=10, color='#FFC107', edgecolor='#FFA000', alpha=0.5)
    axes[2].yaxis.tick_right()
    ax = axes[2].twinx()
    ax.plot(df.index, df.close, 'r', alpha=0.7, linewidth=2)
    ax.set_title('EPS', loc='right')

    fig.set_facecolor('white')
    plt.savefig('profit/' + sid + title + '.png')


if __name__ == '__main__':
    # ret = get_list('tse')
    # for sid, title in ret:
    #     print('{}, {}'.format(sid, title))
    #
    #     try:
    #         df = pd.read_csv('data/' + str(sid) + '.csv', index_col=0)
    #         df.index = pd.to_datetime(df.index)
    #         df = df.iloc[-255 * 5:]
    #         df = df.apply(pd.to_numeric, errors='coerce')
    #
    #         df_revenue = profit(sid)
    #         df_gain = gain(sid)
    #         drawing(df, df_revenue, df_gain, sid, title)
    #
    #     except:
    #         print('Exception {}, {}'.format(sid, title))
    #         ADDR = 'http://easyfun.concords.com.tw/z/zc/zch/zch_' + str(sid) + '.djhtm'
    #         print(ADDR)
    #         continue

    dividend()



