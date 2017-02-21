# -*- coding: utf-8 -*-
from datetime import timedelta, datetime
from indicator import get_kd
import pandas as pd
from earning import profit, gain, dividend
from util import get_list
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform

if platform.system() == 'Darwin':
    font = fm.FontProperties(fname='/System/Library/Fonts/STHeiti Medium.ttc', size=25)
else:
    font = fm.FontProperties(fname='/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc')


def drawing(num, df, daily, weekly, monthly, df_f, df_revenue, df_gain, sid, title=None):
    fig = plt.figure(figsize=(36, 16))

    ax0 = plt.subplot2grid((6, 2), (0, 0), rowspan=2)
    ax1 = plt.subplot2grid((6, 2), (2, 0))
    ax2 = plt.subplot2grid((6, 2), (3, 0))
    ax3 = plt.subplot2grid((6, 2), (4, 0))
    ax4 = plt.subplot2grid((6, 2), (5, 0))

    ay0 = plt.subplot2grid((6, 2), (0, 1), rowspan=2)
    ay1 = plt.subplot2grid((6, 2), (2, 1), rowspan=2)
    ay2 = plt.subplot2grid((6, 2), (4, 1), rowspan=2)

    begin = df.index[-1].to_pydatetime() - timedelta(num)
    begin = datetime(begin.year, begin.month, 1) - timedelta(1)
    print(begin)

    df = df.loc[df.index >= begin]
    ax0.plot(df.index, df.close, 'b', alpha=0.7)
    ax0.set_title('price', loc='right', fontproperties=font)
    ax0.get_yaxis().tick_right()
    ax0.yaxis.grid(True)

    daily = daily.loc[daily.index >= begin]
    highK = daily[daily.k >= 80]
    lowK = daily[daily.k <= 20]
    ax1.plot(daily.index, daily.k, 'r', daily.index, daily.d, 'c', alpha=0.3)
    ax1.plot(highK.index, highK.k, 'ro', mec='r')
    ax1.plot(lowK.index, lowK.k, 'go', mec='g')
    ax1.set_title('日KD', loc='right', fontproperties=font)

    weekly = weekly.loc[weekly.index >= begin]
    highK = weekly[weekly.wk >= 80]
    lowK = weekly[weekly.wk <= 20]
    ax2.plot(weekly.index, weekly.wk, 'r', weekly.index, weekly.wd, 'c', alpha=0.3)
    ax2.plot(highK.index, highK.wk, 'ro', mec='r')
    ax2.plot(lowK.index, lowK.wk, 'go', mec='g')
    ax2.set_title('週KD', loc='right', fontproperties=font)

    monthly = monthly.loc[monthly.index >= begin]
    highK = monthly[monthly.mk >= 80]
    lowK = monthly[monthly.mk <= 20]
    ax3.plot(monthly.index, monthly.mk, 'r', monthly.index, monthly.md, 'c', alpha=0.3)
    ax3.plot(highK.index, highK.mk, 'ro', mec='r')
    ax3.plot(lowK.index, lowK.mk, 'go', mec='g')
    ax3.set_title('月KD', loc='right', fontproperties=font)

    ax4.bar(df.index, df.amount, 0.5, color='r', edgecolor='none')
    ax4.get_yaxis().tick_right()
    ax4.set_title('成交量', loc='right', fontproperties=font)

    for ax in [ax1, ax2, ax3]:
        ax.set_ylim(0, 100)
        ax.get_yaxis().set_visible(False)
        ax.get_xaxis().set_ticklabels([])
        ax.set_facecolor('white')

    ay0.plot(df_f.index, df_f.close, 'r', alpha=0.5, linewidth=2)
    ay0.set_title('月營收', loc='right', fontproperties=font)
    ay0.yaxis.grid(True)
    ax = ay0.twinx()
    ax.bar(df_revenue.index, df_revenue.revenue, width=10, color='#FFC107', edgecolor='#FFA000', alpha=0.5)

    ay1.plot(df_f.index, df_f.close, 'r', alpha=0.2, linewidth=2, zorder=1)
    ay1.get_yaxis().set_visible(False)
    ay1.set_title('毛利率/營益率', loc='right', fontproperties=font)
    ax = ay1.twinx()
    ax.plot(df_gain.index, df_gain.gross_margin, color='g', alpha=0.5, linewidth=2, zorder=2)
    ax.plot(df_gain.index, df_gain.profit_margin, color='b', alpha=0.5, linewidth=2, zorder=2)

    ay2.plot(df_f.index, df_f.close, 'r', alpha=0.5, linewidth=2, zorder=1)
    ay2.get_yaxis().set_visible(False)
    ay2.set_title('EPS', loc='right', fontproperties=font)
    ax = ay2.twinx()
    ax.bar(df_gain.index, df_gain.eps, width=10, color='#00bcd4', edgecolor='#00838f', alpha=0.5, zorder=2)

    fig.subplots_adjust(bottom=0.1, hspace=0.5)
    fig.set_facecolor('white')
    div = float(dividend(sid)) * 100 / df.close[-1]
    fig.suptitle("{} {}, \t殖利率 {:6.2f}%".format(sid, title, div), fontsize=32, fontproperties=font)

    plt.savefig('pic/' + sid + '.png')


def gen_pic(items):
    print('Generating Pic ...')
    for sid, title in items:
        print('{}, {}'.format(sid, title))

        try:
            df_f = pd.read_csv('data/' + str(sid) + '.csv', index_col=0)
            df_f.index = pd.to_datetime(df_f.index)
            df_f = df_f.iloc[-255 * 5:]
            df_f = df_f.apply(pd.to_numeric, errors='coerce')

            if len(df_f.index) > 365:
                num = 365
            else:
                num = len(df_f.index)

            df_revenue = profit(sid)
            df_gain = gain(sid)
            # drawing(df, df_revenue, df_gain, sid, title)

            df, daily, weekly, monthly = get_kd(sid, num)
            drawing(num, df, daily, weekly, monthly, df_f, df_revenue, df_gain, sid, title)

        except Exception as e:
            print('Exception {}, {}'.format(sid, title))
            ADDR = 'http://easyfun.concords.com.tw/z/zc/zch/zch_' + str(sid) + '.djhtm'
            print(ADDR)
            print(e)
            continue


if __name__ == '__main__':
    # auto_crawl()
    tse = get_list('tse')
    gen_pic(tse)

    # otc = get_list('otc')
    # gen_pic(otc)



