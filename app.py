import os
from _datetime import datetime
import csv
from collections import OrderedDict


class History:
    def __init__(self, dbpath):
        self.dbpath = dbpath
        self.hist = OrderedDict()
        self.lastid = 0
        if os.path.exists(dbpath):
            with open(dbpath, 'r') as db:
                data = csv.reader(db, delimiter=',')
                for idx, elem in enumerate(data):
                    self.hist[idx+1] = (elem[0], elem[1])
                    self.lastid = idx+1
        else:
            with open(dbpath, 'w') as file: pass

    def add(self, filepath):
        filename = os.path.basename(filepath)
        self.lastid += 1
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.hist[self.lastid] = (time, filename)
        with open(self.dbpath, 'a') as file:
            file.write(','.join(self.hist[self.lastid]) + '\r\n')

    def tolist(self):
        total = []
        for key, value in self.hist.items():
            total.append([key, value[0], value[1]])
        return total

if __name__ == "__main__":
    hist = History('db/db2.csv', '../upload')
    hist.add('file3.ext')
    print(hist.tolist())