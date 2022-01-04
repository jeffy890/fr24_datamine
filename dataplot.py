import matplotlib.pyplot as plt
import numpy as np
import sys
import csv

# 引数としてpathを受け取る
try:
    data_path = sys.argv [1]
except IndexError:
    print("error: enter json data path as argument")
    print("example: python dataplot.py ac_data.csv")
    sys.exit()

# ファイルの読み込み
with open(data_path) as f:
    reader = csv.reader(f)
    load_data = [row for row in reader]

print(load_data[4])

x = load_data[4][2]
y = load_data[4][1]

plt.scatter(x, y)
plt.grid(True)
plt.show()