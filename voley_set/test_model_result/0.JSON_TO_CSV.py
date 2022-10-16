import pandas as pd
# import sklearn
# from sklearn.ensemble import GradientBoostingClassifier
import json
import csv
import random
import pandas as pd
from itertools import *
import json
import time
import tqdm
from func_0_pred_obr_aft_pars import *

with open("for_analize_PRIORITET.json", "r", encoding='utf-8') as read_file:
    data = json.load(read_file)
print(len(data))
data_it = []
for i in data:
    try:
        if i["game"] not in data_it:
            data_it.append(i["game"])
    except Exception as e:
        continue

import pandas as pd
df = pd.DataFrame.from_dict(data_it, orient='columns')
# prfloat(df.columns)
# pdObj = pd.read_json('for_analize_PRIORITET.json')
# prfloat(f' eto pdObj : {pdObj}')
df['3_set_sub_list'] = None

df = df[[ 'date', 'event_number ',
       'teams',  '1_set_sub_list', '2_set_sub_list', '3_set_sub_list',
       '3_set_kf_1', '3_set_kf_2',
      ]]
df.to_csv("pdObj.csv")
list_of_column_names =  ['date', 'event_number', 'teams','set1','set2', 'set3', 'kf1_3','kf2_3']
df = pd.read_csv("pdObj.csv")
df = df.drop('Unnamed: 0', axis =1)
df.columns = list_of_column_names




# df = pd.read_csv('after_pars.csv', delimiter=',')
# # prfloat(df)

js = df.to_json(orient = 'records')
data  = json.loads(js)
itg = []
for i in data:
    if (i.get('set1')!= None and  i.get('set2') != None):
        # prfloat(f' eto i : {i}')
        itg.append(i)

# for i in itg:
#     print(f' eto i : {type(i.get("set1"))}')
#     for j in i.get("set1"):
#         print(f' eto j : {j}, {type(j)}')

""" ВНИМАНИЕ тут видно что в счет в сете попадают всякие скобки из за которых не работает - это нужно убрать"""

def get_normal_schet_in_set(i): # на вход сет (движение по счету(i): #на вход игра со всеми сетами
    new_set = []
    set = i.split(',')
    for i in set:

        i = i.replace('[', '')
        i = i.replace(']', '')
        new_set.append(i)
    return new_set


"""укороченная версия - делаю счет без скобок и так далее"""
def notmalize_set(data): # удаляю поля nonname + счет в лист из строки перевожу
    for i in data:

        i['set1'] = get_normal_schet_in_set(i.get('set1'))
        i['set2'] = get_normal_schet_in_set(i.get('set2'))
        # i['set3'] = get_normal_schet_in_set(i['set3'])
    return data




data = notmalize_set(itg)
# for i in data:
#     print(f' eto i : {type(i.get("set1"))}')
#     for j in i.get("set1"):
#         print(f' eto j : {j}, {type(j)}')



data_itogo = get_correct_data(data, True)



data = get_pred_obrab_data(data_itogo)

for i in data:
    print(f' eto i : {i.keys()}')
print(f' eto len data : {len(data)}, eto len data_itogo : {len(data_itogo)}')

# data_itogo = del_games_less_then_24_scores(data_itogo)
# for i in data_itogo:
#     print(f' eto i posle obrabotki : {i}')
#
# print(len(data_itogo))
# with open('data_pred_obr_aft_pars.json', 'w') as f:
#     f.write(json.dumps(data_itogo))
# print('ALL DATA write to file')