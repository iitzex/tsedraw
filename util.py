# -*- coding: utf-8 -*-
import os
import csv
from os import listdir
from os.path import isfile, join


def add_columns():
    # add columns for data/csv
    mypath = 'data/'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    for filename in onlyfiles:
        with open('data/' + filename, 'r') as original:
            lines = original.readlines()

        new_lines = []
        for line in lines:
            if '--' not in line:
                new_lines.append(line)

        with open('data/' + filename, 'w') as modified:
            modified.writelines(new_lines)


def convert_time():
    allfile = os.listdir('data/')
    for item in allfile:
        with open('data/'+item, 'r') as fp:
            tp = open('old/'+item, 'w')
            for i, line in enumerate(fp.readlines()):
                if i == 0:
                    tp.write(line.__str__())
                    continue
                time = line.split(',')
                s = time[0].split('/')
                s[0] = str(int(s[0]) + 1911)
                t = '-'.join(s)
                time[0] = t
                tp.write(','.join(time))


def Cname(name):
    with open(name + '.csv', newline='') as csvfile:
        r = csv.reader(csvfile)

        buffer = {}
        for row in r:
            # print(row[0] + ' ' + row[1])
            buffer.update({row[0]: row[1]})

        return buffer


def get_list(name):
    f = open(name + '.csv', 'r')
    lists = csv.reader(f)

    for stock in lists:
        sid = stock[0]
        title = stock[1]

        yield sid, title

if __name__ == '__main__':
    c = Cname()
    print(c['0050'])

