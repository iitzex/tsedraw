# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from util import Cname


def D_KD(df):
    low_list = df['low'].rolling(window=9, center=False).min()
    low_list.fillna(value=df['low'].expanding(min_periods=1).min(), inplace=True)
    high_list = df['high'].rolling(window=9, center=False).max()
    high_list.fillna(value=df['high'].expanding(min_periods=1).max(), inplace=True)
    rsv = (df['close'] - low_list) / (high_list - low_list) * 100

    slowk = rsv.ewm(com=2).mean()
    slowd = slowk.ewm(com=2).mean()

    kd = pd.concat([slowk, slowd], axis=1, keys=['k', 'd'])

    # for i, item in enumerate(rsv):
    #     print i, low_list[i], high_list[i], rsv[i], slowk[i], slowd[i]

    return kd


def W_KD(df):
    ohlc_dict = {
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
    }
    df = df.resample('W-Mon', label='left', closed='left').apply(ohlc_dict)
    df = df.dropna()
    # print df

    low_list = df['low'].rolling(window=6, center=False).min()
    low_list.fillna(value=df['low'].expanding(min_periods=1).min(), inplace=True)
    high_list = df['high'].rolling(window=6, center=False).max()
    high_list.fillna(value=df['high'].expanding(min_periods=1).max(), inplace=True)
    rsv = (df['close'] - low_list) / (high_list - low_list) * 100

    slowk = rsv.ewm(com=2).mean()
    slowd = slowk.ewm(com=2).mean()

    # for i, item in enumerate(rsv):
    #     print i, low_list[i], high_list[i], rsv[i], slowk[i], slowd[i]

    d_slowk = slowk.asfreq('D', method='pad')
    d_slowd = slowd.asfreq('D', method='pad')
    # w_kd = pd.concat([slowk, slowd, d_slowk, d_slowd], axis=1, keys=['wk', 'wd', 'dk', 'dd'])
    w_kd = pd.concat([slowk, slowd], axis=1, keys=['wk', 'wd'])

    return w_kd


def M_KD(df):
    ohlc_dict = {
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
    }
    df = df.resample('M', label='left', closed='left').apply(ohlc_dict)
    df = df.dropna()
    # print df

    low_list = df['low'].rolling(window=6, center=False).min()
    low_list.fillna(value=df['low'].expanding(min_periods=1).min(), inplace=True)
    high_list = df['high'].rolling(window=6, center=False).max()
    high_list.fillna(value=df['high'].expanding(min_periods=1).max(), inplace=True)
    rsv = (df['close'] - low_list) / (high_list - low_list) * 100

    slowk = rsv.ewm(com=2).mean()
    slowd = slowk.ewm(com=2).mean()

    # for i, item in enumerate(rsv):
    #     print i, low_list[i], high_list[i], rsv[i], slowk[i], slowd[i]

    m_kd = pd.concat([slowk, slowd], axis=1, keys=['mk', 'md'])

    return m_kd


def month_mean(df):
    ohlc_dict = {
        'open': np.mean,
        'high': np.mean,
        'low': np.mean,
        'close': np.mean,
    }
    df = df.resample('M', label='left', closed='left').apply(ohlc_dict)
    df = df.dropna()
    # print(df)


def get_kd(filename, num):
    pd.options.display.float_format = '{:,.2f}'.format

    df = pd.read_csv('data/' + filename + '.csv', index_col=0)
    df.index = pd.to_datetime(df.index)
    if len(df.index) < num/2:
        raise IndexError('Not enough data!')
        # return False

    # print(df)
    df = df.apply(pd.to_numeric, errors='coerce')

    daily = D_KD(df)
    weekly = W_KD(df)
    monthly = M_KD(df)

    # num = 150
    # result = pd.concat([df, daily, weekly, monthly], axis=1, join_axes=[df.index])[-num:]
    # result.to_csv('pandas.txt', sep=',', mode='w')
    return df, daily, weekly, monthly


if __name__ == '__main__':
    sid = '1102'
    cname = Cname()[sid]

    print(sid, cname)
    num = 365
    try:
        df, daily, weekly, monthly = get_kd(sid, num)
        # drawing(num, df, daily, weekly, monthly, sid, cname)
    except IndexError as e:
        print('{}, {}, {}'.format(sid, cname, e))
