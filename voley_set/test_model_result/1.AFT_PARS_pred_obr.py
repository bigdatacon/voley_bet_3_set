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

df['3_set_sub_list'] = None
df['source'] = 'fonbet.ru'
df['sex'] = None
df['kf1_1'] = '99,0'
df['kf2_1'] = '99,0'
df['kf1_2'] = '99,0'
df['kf2_2'] = '99,0'

df = df[[ 'date', 'event_number ',
       'teams',  '1_set_sub_list', '2_set_sub_list', '3_set_sub_list', 'kf1_1', 'kf2_1', 'kf1_2', 'kf2_2',
        '3_set_kf_1', '3_set_kf_2', 'source', 'sex'
      ]]
df.to_csv("pdObj.csv")
list_of_column_names =  ['date', 'event_number', 'teams','set1','set2', 'set3', 'kf1_1', 'kf2_1', 'kf1_2', 'kf2_2', 'kf1_3','kf2_3',
                         'source', 'sex']
df = pd.read_csv("pdObj.csv")
df = df.drop('Unnamed: 0', axis =1)
df.columns = list_of_column_names


js = df.to_json(orient = 'records')
data  = json.loads(js)
itg = []
for i in data:
    if (i.get('set1')!= None and  i.get('set2') != None):
        # prfloat(f' eto i : {i}')
        itg.append(i)


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


def who_win_set(set): #на вход двидение по сету
    assert float(set[-1])!= 0, 'Не корректно отработала функция get_pred_obrab_data в части проверки пропусков'
    if float(set[-1])>0:
        rez = 1
    else:
        rez = 2
    return rez

def get_who_win_3_set_for_data(data): #на вход весь массив игр, функция применяется только для игр с парсинга
    for i in data:
        set_1 = str(who_win_set(i.get('set1')))
        set_2 = str(who_win_set(i.get('set2')))
        set_3 = str(9)
        print(f' eto set_1, set_2, set_3: {set_1, set_2, set_3}')
        # i['game'] = str(set_1,set_2,set_3)
        i['game'] = int(set_1+ set_2+ set_3)

    return data



data = notmalize_set(itg)

data_itogo = get_correct_data(data, True)

data = get_pred_obrab_data(data_itogo)
data = get_who_win_3_set_for_data(data)

df = pd.DataFrame.from_dict(data, orient='columns')
df = df[['teams', 'source', 'sex', 'set1', 'set2', 'set3', 'game',
        'kf1_3', 'kf2_3', '1_set_scr_1', '1_set_scr_2', '1_set_len_set',
        '1_set_FLAG_LEN_SCR', '2_set_scr_1', '2_set_scr_2', '2_set_len_set', '2_set_FLAG_LEN_SCR']]

js = df.to_json(orient = 'records')
data  = json.loads(js)

for i in data:
    print(f' eto i : {i.keys()}')
    print(f' eto i : {i}')
print(f' eto len data : {len(data)}, eto len data_itogo : {len(data_itogo)}')


with open('AFT_PARS_data_pred_obr.json', 'w') as f:
    f.write(json.dumps(data))
print('ALL DATA write to file')
print(data[0])
print(data[0].keys())


base = ['teams', 'source', 'sex', 'set1', 'set2', 'set3', 'game',
        'kf1_3', 'kf2_3', '1_set_scr_1', '1_set_scr_2', '1_set_len_set',
        '1_set_FLAG_LEN_SCR', '2_set_scr_1', '2_set_scr_2', '2_set_len_set', '2_set_FLAG_LEN_SCR']


non_base =['teams', 'source', 'sex', 'set1', 'set2', 'set3', 'game', 'kf1_3', 'kf2_3', '1_set_scr_1',
           '1_set_scr_2', '1_set_len_set', '1_set_FLAG_LEN_SCR', '2_set_scr_1', '2_set_scr_2',
           '2_set_len_set', '2_set_FLAG_LEN_SCR']



print(base==non_base)
