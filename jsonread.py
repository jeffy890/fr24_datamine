import json
import numpy as np
import datetime
import csv
import sys

# 引数としてpathを受け取る
try:
    data_path = sys.argv [1]
except IndexError:
    print("error: enter json data path as argument")
    print("example: python jsonread.py aircraft.json")
    sys.exit()

# jsonの読み込みと変数への代入
read_data = open(data_path, 'r')
read_json = json.load(read_data)

# dict型の3つ目にaircraftとしてデータが入っているので
# 取り出して変数へ代入(1つ目は時間)
aircraft = read_json["aircraft"]
# print(type(aircraft))

# numpyで扱えるように変換
aircraft_np = np.array(aircraft)

# dict型1つ目のnowにはunix時間で時間データが入っている
# datetimeライブラリにより変換できる．
dt = datetime.datetime.fromtimestamp(read_json["now"])
dt_hms = str(dt.hour) + ":" + str(dt.minute) + ":" + str(dt.second)
dt_md = str(dt.year) + "." + str(dt.month) + "." + str(dt.day)
print("captured time: " + dt_hms)

# shapeがわかると補足した航空機の数が大まかにわかる
#print("tracked aircraft: " + str(aircraft_np.size))

dt_data =[read_json["now"], dt_md, dt_hms]
ac_hex = []
ac_hex.append(dt_data)

file_info = ["hex", "lat", "lon", "altitude"]
ac_hex.insert(1, file_info)

ac_data = np.empty(3)
ac_data_tmp = np.empty(3)

# aircraft_npには航空機のdict型データがlist型になって入っている
# for文を回すために，listのサイズを取り出している
for n in range(aircraft_np.size):
    
    # try, exceptでデータがない時のエラーを回避する
    try:
        ac_data_tmp[0] = aircraft_np[n]["lat"]
    except:
        ac_data_tmp[0] = 91

    try:
        ac_data_tmp[1] = aircraft_np[n]["lon"]
    except:
        ac_data_tmp[1] = 181
    
    try:
        if(aircraft_np[n]["altitude"] == "ground"):
            ac_data_tmp[2] = 0
        elif(aircraft_np[n]["altitude"]<0):
            ac_data_tmp[2] = -1 # 取得しているが高度が負の時
        else:
            ac_data_tmp[2] = aircraft_np[n]["altitude"]
    except:
        ac_data_tmp[2] = -2 # 取得できていない時

    ac_hex_tmp = []

    #print(aircraft_np[n]["hex"])
    ac_hex_tmp.append(aircraft_np[n]["hex"])
    ac_hex_tmp.extend(ac_data_tmp.tolist())
    ac_hex.append(ac_hex_tmp)
    
    #print(ac_data_tmp)
    #ac_data = np.vstack((ac_data, ac_data_tmp))

print(ac_hex)

# ファイルへの保存
path = './ac_data.csv'

with open(path, mode='w') as f:
    writer = csv.writer(f)
    writer.writerows(ac_hex)