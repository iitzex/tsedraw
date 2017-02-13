# -*- coding: utf-8 -*-
from datetime import timedelta, datetime
from indicator import get_kd
from crawl import auto_crawl
from util import get_list
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform
if platform.system() == 'Darwin':
    font = fm.FontProperties(fname='/System/Library/Fonts/STHeiti Medium.ttc')
else:
    font = fm.FontProperties(fname='/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc')


def drawing(num, df, daily, weekly, monthly, sid, title=None):
    row = 5
    fig, axes = plt.subplots(nrows=row, ncols=1, gridspec_kw={'height_ratios': [2, 1, 1, 1, 1]}, figsize=(16, 12))
    fig.subplots_adjust(hspace=.001, wspace=0.5)

    begin = df.index[-1].to_datetime() - timedelta(num)
    begin = datetime(begin.year, begin.month, 1) - timedelta(1)

    df = df.loc[df.index >= begin]
    axes[0].plot(df.index, df.close, 'b', alpha=0.7)
    axes[0].set_title('{} {}'.format(sid, title), fontproperties=font)
    axes[0].get_yaxis().tick_right()
    axes[0].yaxis.grid(True)

    daily = daily.loc[daily.index >= begin]
    highK = daily[daily.k >= 80]
    lowK = daily[daily.k <= 20]
    axes[1].plot(daily.index, daily.k, 'r', daily.index, daily.d, 'c', alpha=0.3)
    axes[1].plot(highK.index, highK.k, 'ro', mec='r')
    axes[1].plot(lowK.index, lowK.k, 'go', mec='g')
    axes[1].set_title('daily KD', loc='right', fontproperties=font)

    weekly = weekly.loc[weekly.index >= begin]
    highK = weekly[weekly.wk >= 80]
    lowK = weekly[weekly.wk <= 20]
    axes[2].plot(weekly.index, weekly.wk, 'r', weekly.index, weekly.wd, 'c', alpha=0.3)
    axes[2].plot(highK.index, highK.wk, 'ro', mec='r')
    axes[2].plot(lowK.index, lowK.wk, 'go', mec='g')
    axes[2].set_title('weekly KD', loc='right', fontproperties=font)

    monthly = monthly.loc[monthly.index >= begin]
    highK = monthly[monthly.mk >= 80]
    lowK = monthly[monthly.mk <= 20]
    axes[3].plot(monthly.index, monthly.mk, 'r', monthly.index, monthly.md, 'c', alpha=0.3)
    axes[3].plot(highK.index, highK.mk, 'ro', mec='r')
    axes[3].plot(lowK.index, lowK.mk, 'go', mec='g')
    axes[3].set_title('monthly KD', loc='right', fontproperties=font)

    import numpy as np
    mu, sigma = 100, 15
    x = mu + sigma * np.random.randn(10000)

    bar_width = 0.1
    axes[4].bar(df.index, df.number/(df.number.mean()/30), bar_width, color='r', edgecolor='none')
    axes[4].set_title('Volumn', loc='right', fontproperties=font)

    for i in range(1, row):
        axes[i].set_ylim(0, 100)
        axes[i].get_yaxis().set_visible(False)
        axes[i].get_xaxis().set_ticklabels([])
        axes[i].set_axis_bgcolor('white')

    fig.subplots_adjust(bottom=0.1, hspace=0.3)
    # fig.suptitle(sid + ' ' + cname, fontsize=14, fontweight='bold', fontproperties=font)
    fig.set_facecolor('white')
    plt.savefig('kd/' + sid + title + '.png')

    if 'DEBUG' in globals():
        plt.show()


if __name__ == '__main__':
    auto_crawl()
    ret = get_list()

    print('Generating Pic..')
    num = 365
    for sid, title in ret:
        print('{}, {}'.format(sid, title))

        try:
            df, daily, weekly, monthly = get_kd(sid, num)
            drawing(num, df, daily, weekly, monthly, sid, title)

        except IndexError as e:
            print('{}, {}, {}'.format(sid, title, e))

