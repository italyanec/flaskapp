import os
import csv

from _datetime import datetime
from collections import OrderedDict


class History:
    def __init__(self, dbpath):
        self.dbpath = dbpath
        # self.hist = OrderedDict()
        self.history = []

        # self.lastid = 0
        if os.path.exists(dbpath):
            with open(dbpath, 'r') as db:
                self.history = [tuple(e) for e in csv.reader(db, delimiter=',')]
                # data = csv.reader(db, delimiter=',')
                # for idx, elem in enumerate(data):
                #     if elem:
                #         self.hist[idx+1] = (elem[0], elem[1])
                #         self.lastid = idx+1
        else:
            with open(dbpath, 'w'):     # создать каталог если его нет
                pass

    def add(self, filepath):
        filename = os.path.basename(filepath)
        # self.lastid += 1
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        value = (str(len(self.history)), time, filename)
        self.history.append(value)

        with open(self.dbpath, 'a') as file:
            file.write(','.join(value) + '\n')

        # self.hist[self.lastid] = (time, filename)
        # with open(self.dbpath, 'a') as file:
        #     file.write(','.join(self.hist[self.lastid]) + '\n')

    def __getitem__(self, key):
        return self.history[key]
        # if key <= self.lastid:
        #     return self.hist[key][1], self.hist[key][0]
        # else:
        #     raise KeyError

    def tolist(self):
        # total = []
        # for key, value in self.hist.items():
        #     total.append([key, value[0], value[1]])
        # return total[::-1]
        return self.history[::-1]


if __name__ == "__main__":
    hist = History('db/db2.csv')
    hist.add('file3.ext')
    print(hist[1])
    print(hist.tolist())
