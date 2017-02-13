# -*- coding: utf8 -*-
from bs4 import BeautifulSoup
import re
import requests


def getlist(ADDR):
    """get all stock list"""
    r = requests.get(ADDR)
    content = r.content.decode('Big5-HKSCS', errors='backslashreplace')
    soup = BeautifulSoup(content, "lxml")

    tse = []
    total = soup.find_all('tr')
    for row in total:
        column = row.find_all('td')
        if len(column) < 5:
            continue
        if column[5].text == 'ESVUFR':
            item = column[0].text
            pat = "(\d{4})(.*)"
            all = re.search(pat, item)
            sid = all.group(1)
            name = all.group(2).strip()
            cat = column[4].text
            # print(key, name, cat)

            tse.append((sid, name))

    return tse


def writelist(tse, otc):
    f = open('tse.csv', 'w+')

    print("writing twse")
    for sid, name in tse:
        print(sid, name)
        f.write(sid + ", " + name + "\n")

    f = open('otc.csv', 'w+')

    print("writing otc")
    for sid, name in otc:
        print(sid, name)
        f.write(sid + ", " + name + "\n")


if __name__ == '__main__':
    ADDR = "http://isin.twse.com.tw/isin/C_public.jsp?strMode=2"
    tse = getlist(ADDR)

    ADDR = "http://isin.twse.com.tw/isin/C_public.jsp?strMode=4"
    otc = getlist(ADDR)

    writelist(tse, otc)
