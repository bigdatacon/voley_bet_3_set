import pandas as pd
import sklearn
from sklearn.ensemble import GradientBoostingClassifier
import json
import csv
import random
import pandas as pd
from itertools import *
import json
import time
import tqdm

""" КОД НИЖЕ НЕ УДАЛЯТЬ - ОН НУЖЕН ДЛЯ ФАЙЛА КРИВОШАПКИ, для парсера использовать то что с 200 строки"""
""" 0.Предобработка - сет из строки в список"""
def get_normal_schet_in_set(i): # на вход сет (движение по счету
    i = i.split()[0].split(",")
    return i
"""1. Предобработка - удаляю первый элемент unknown"""
def notmalize_set(data): # удаляю поля nonname + счет в лист из строки перевожу
    for i in data:
        try:
            del i['Unnamed: 0']
        except Exception as e:
            continue
        finally:
            i['set1'] = get_normal_schet_in_set(i['set1'])
            i['set2'] = get_normal_schet_in_set(i['set2'])
            i['set3'] = get_normal_schet_in_set(i['set3'])
    return data

"""1. Предобработка - удаляю первый элемент unknown"""
def notmalize_set_after_pars(data): # удаляю поля nonname + счет в лист из строки перевожу
    for i in data:
        try:
            del i['Unnamed: 0']
        except Exception as e:
            continue
    return data


"""2. Функция проверки что в сете корректно заполнены пропуска - не более 2  подряд одинаковых значений, если не так то удаляются данные"""
def get_info_about_incorr_propusk(i): # на вход движение счета по одному из сетов
    l = []
    count = 0
    for g in range(len(i)-1):
        if i[g+1]== i[g]:
            count+=1
        else:
            if count!=0:
                # prfloat(f' eto count : {count}')
                l.append(count)
                count = 0
    flag = True if len(i)<25 else False
    return any([x > 0 for x in l]) or flag

"""2.5 реализую функцию 2 на весь датасет"""
def get_correct_data_after_pars(data): # на вход массив
    data = notmalize_set(data)
    data_itog = []
    for i in data:
        s1 = i["set1"]
        s2 =  i["set2"]
        rez_1 = get_info_about_incorr_propusk(s1)
        rez_2 = get_info_about_incorr_propusk(s2)
        if not (rez_1 or rez_2):
            data_itog.append(i)
    return data_itog

"""2.5 реализую функцию 2 но для данных после парсинга - добавил флаг Tru для данных с парсинга"""
def get_correct_data(data, flag=False): # на вход массив
    if flag==False:
        data = notmalize_set(data)
    else:
        data = notmalize_set_after_pars(data)
    data_itog = []
    for i in data:
        s1 = i["set1"]
        s2 =  i["set2"]
        rez_1 = get_info_about_incorr_propusk(s1)
        rez_2 = get_info_about_incorr_propusk(s2)
        if not (rez_1 or rez_2):
            data_itog.append(i)
    return data_itog



""" 3. Функция перевода движения по сету в итоговый счет"""

def get_simple_score(data): # на вход движение по сету

    one = 0
    twoe = 0
    for i in range(len(data)-1):
        if float(data[i+1]) - float(data[i]) > 0:
            # prfloat(f' eto i+1: {data[i+1]}, eto i {data[i]}')
            one+= 1
        else:
            # prfloat(f' eto i+1: {data[i + 1]}, eto i {data[i]}')
            twoe+=1
    len_set = len(data)
    if data[0]==0:
        if abs(len_set-one-twoe) !=0:
            flag = False
        else:
            flag = True
    else:
        if abs(len_set-one-twoe) !=1:
            flag = False
        else:
            flag = True
    return {'scr_1': one, 'scr_2': twoe, 'len_set': len_set, 'FLAG_LEN_SCR' : flag}

"""4. Итоговая пред обработка """
def get_pred_obrab_data(data):
    it= []
    for i in data:
        i['1_set_scr_1'] = get_simple_score(i["set1"])['scr_1']
        i['1_set_scr_2'] = get_simple_score(i["set1"])['scr_2']
        i['1_set_len_set'] = get_simple_score(i["set1"])["len_set"]
        i['1_set_FLAG_LEN_SCR'] = get_simple_score(i["set1"])["FLAG_LEN_SCR"]

        i['2_set_scr_1'] = get_simple_score(i["set2"])['scr_1']
        i['2_set_scr_2'] = get_simple_score(i["set2"])['scr_2']
        i['2_set_len_set'] = get_simple_score(i["set2"])["len_set"]
        i['2_set_FLAG_LEN_SCR'] = get_simple_score(i["set2"])["FLAG_LEN_SCR"]


        if i['1_set_FLAG_LEN_SCR']== True and i['2_set_FLAG_LEN_SCR']==True:
            it.append(i)
    return it

"""4.1 Дополнительная функция удаляю из списка игры у которых в сете не выявлен победитель"""
def dell_sets_with_no_win(data):
    itg = []
    for i in data:
        if float(i.get('set1')[-1]) == 0 or float(i.get('set2')[-1])==0:
            print(f'here wrong game : {i}')
        else:
            itg.append(i)
    return itg


""" !!!!!!!!!!!!!!!!!!!!!!!!блок функций после парсера """
"""
def get_normal_schet_in_set(i): # на вход сет (движение по счету(i): #на вход игра со всеми сетами
    new_set = []
    set = i.split(',')
    for i in set:

        i = i.replace('[', '')
        i = i.replace(']', '')
        new_set.append(i)
    return new_set

""""""
1. Предобработка - удаляю первый элемент unknown
def notmalize_set(data): # удаляю поля nonname + счет в лист из строки перевожу
    for i in data:
        try:
            del i['Unnamed: 0']
        except Exception as e:
            continue
        finally:
            i['set1'] = get_normal_schet_in_set(i['set1'])
            i['set2'] = get_normal_schet_in_set(i['set2'])
            # i['set3'] = get_normal_schet_in_set(i['set3'])
    return data
""""""
2. Функция проверки что в сете корректно заполнены пропуска - не более 2  подряд одинаковых значений, если не так то удаляются данные
def get_info_about_incorr_propusk(i): # на вход движение счета по одному из сетов
    l = []
    count = 0
    for g in range(len(i)-1):
        if i[g+1]== i[g]:
            count+=1
        else:
            if count!=0:
                # prfloat(f' eto count : {count}')
                l.append(count)
                count = 0
    flag = True if len(i)<25 else False
    return any([x > 0 for x in l]) or flag
""""""
2.5 реализую функцию 2 на весь датасет
def get_correct_data(data): # на вход массив
    data = notmalize_set(data)
    data_itog = []
    for i in data:
        s1 = i["set1"]
        s2 =  i["set2"]
        rez_1 = get_info_about_incorr_propusk(s1)
        rez_2 = get_info_about_incorr_propusk(s2)
        if not (rez_1 or rez_2):
            data_itog.append(i)
    return data_itog

""" """
3. Функция перевода движения по сету в итоговый счет
def get_simple_score(new_set): # на вход отнормализованный сетам
    one = 0
    twoe = 0
    flag = True
    nulevoy = float(new_set[0])
    minus_for_len_set = 0
    if abs(nulevoy) == 1:
        if nulevoy > 0:
            one += abs(nulevoy)
        else:
            twoe += abs(nulevoy)
    else:
        minus_for_len_set = 1
    for i in range(len(new_set) - 1):
        if abs(float(new_set[i+1])) - abs(float(new_set[i])) > 0:
            one+= 1
        else:
            twoe+=1
    len_set = len(new_set) - minus_for_len_set
    if new_set[0] == 0:
        if abs(len_set - one - twoe) != 1:
            flag = False
        else:
            flag = True
    else:
        if abs(len_set - one - twoe) != 0:
            flag = False
        else:
            flag = True
    # prfloat(f'eto chto ostalos : { one,  twoe,  len_set,  flag}')
    return {'scr_1': one, 'scr_2': twoe, 'len_set': len_set, 'FLAG_LEN_SCR': flag}

""""""
4. Итоговая пред обработка 
def get_pred_obrab_data(data):
    it= []
    for i in data:
        i['1_set_scr_1'] = get_simple_score(i["set1"])['scr_1']
        i['1_set_scr_2'] = get_simple_score(i["set1"])['scr_2']
        i['1_set_len_set'] = get_simple_score(i["set1"])["len_set"]
        i['1_set_FLAG_LEN_SCR'] = get_simple_score(i["set1"])["FLAG_LEN_SCR"]

        i['2_set_scr_1'] = get_simple_score(i["set2"])['scr_1']
        i['2_set_scr_2'] = get_simple_score(i["set2"])['scr_2']
        i['2_set_len_set'] = get_simple_score(i["set2"])["len_set"]
        i['2_set_FLAG_LEN_SCR'] = get_simple_score(i["set2"])["FLAG_LEN_SCR"]


        if i['1_set_FLAG_LEN_SCR']== True and i['2_set_FLAG_LEN_SCR']==True :
            it.append(i)
    return it

""""""
5. Удаляю игры в  которых счет не дошел до 24
def del_games_less_then_24_scores(data):
    it= []
    for i in data:
        f_set_scr_1 = i['1_set_scr_1']
        f_set_scr_2 = i['1_set_scr_2']
        s_set_scr_1 = i['2_set_scr_1']
        s_set_scr_2 = i['2_set_scr_2']
        set_one = [f_set_scr_1, f_set_scr_2]
        set_two = [s_set_scr_1, s_set_scr_2]
        if any(x >=24 for x in set_one) and any(x >=24 for x in set_two) and abs(float(f_set_scr_1) - float(f_set_scr_2))>=1 and \
                abs(float(s_set_scr_1) - float(s_set_scr_2))>=1:
            # print(f' eto i set : {f_set_scr_1, f_set_scr_2} eto 2 set : {[s_set_scr_1, s_set_scr_2]}')
            it.append(i)
    return it
"""