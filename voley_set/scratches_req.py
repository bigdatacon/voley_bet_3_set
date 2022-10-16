# -*- coding: utf-8 -*-
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor
import threading
from threading import Thread
import time
import json
# from func import *
import concurrent.futures
import urllib.request
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import json
from func_volley import *
from itertools import groupby
import requests
import pprint
from copy import deepcopy

import re

def add_to_analize_prior(analize_2, game):
    adding = None
    try:
        flag = False

        for i in analize_2:
            if analize_2[0]!={}:
                if i.get('game').get('ids') == game['ids']:
                    flag= True
                    break
            continue
        if not flag and flag != True:
            if len(game.get('3_set_data')) == 1:
                if game.get('3_set_data')[0].get('scores') == ['0', '0']:
                    print(f'len_this_game= 1 {game.get("3_set_data")}')
                    print(f'here 0:0 : {game.get("3_set_data")[0].get("scores")}, eto 3 set : {game.get("3_set_data")}')
                    adding = game
            for i in analize_2:
                if analize_2[0]!={}:
                    # print(f'eto len 3 seta v analize_2: {len(i.get("game").get("3_set_data"))}')
                    if len(i.get("game").get("3_set_data")) != 1:
                        print(f'ALARMA WRONG DATA FOR ANALIZE: !!  eto GAME: {i}, eto spisok {analize_2}')
                continue
        else:
            adding = None
    except Exception as e:
        print(f'problem in func add_to_analize_prior : ETOS SPIS {analize_2}, ETO GAME : {game}')
    return adding


def add_link_to_LINKS(IDS, LINKS):
    for i in IDS:
        link = i.get('urls')
        if link not in LINKS:
            LINKS.append(link)
    return LINKS

"""Оборачиваю в функцию 2 функции ниже - перевод счета в нормальный вид"""
def get_sub_list(scor_info):
    scor_list = []
    kf_list = []
    scor_one_list = []
    scor_two_list = []
    sub_list = []
    kf_list= []
    kf_1= None
    kf_2 = None
    try:
        for i in scor_info:
            scor_list.append(i.get('scores'))
            kf_list.append(i.get('koeff'))

        for i in scor_list:
            scor_one_list.append(float(i[0]))
            scor_two_list.append(float(i[1]))
        assert len(scor_list)==len(kf_list), "РАЗНЫЕ ДЛИНЫ СПИСКА ОЧКОВ И КОФФИЦИЕНТОВ"
        if float(scor_list[0][0]) == 0 and float(scor_list[0][1]) == 0:
            kf_1 = kf_list[0][0]
            kf_2 = kf_list[0][1]
        else:
            kf_1 = None
            kf_2 = None
        sub_iter = map(sub, scor_one_list, scor_two_list)
        sub_list = fidx(list(sub_iter))
        # print(f' eto sub_list : {sub_list}')
    except Exception as e:
        print(e.args)
    return sub_list, kf_list, kf_1, kf_2

def get_normal_vid_scores(set_l):
    set_data  = ['1_set_data', '2_set_data', '3_set_data', '4_set_data', '5_set_data']
    scor_list = []
    kf_list = []
    scor_one_list = []
    scor_two_list = []
    try:
        for i in range(len(set_data)):
            el = set_data.pop()
            # print(f' eto el : {el}')
            scor_info = set_l.get(el)
            if scor_info:
                prefix = el[:5]
                # print(f' eto PREFIX : {prefix}')
                # print(f' eto scor_info : {scor_info}')
                # print(get_sub_list(scor_info))
                sub_list, kf_list, kf_1, kf_2 = get_sub_list(scor_info)
                # print(f' ETO IZ FUNC : {sub_list, kf_list, kf_1, kf_2}')
                set_l[f'{prefix}{"_"}{"sub_list"}'] = sub_list
                set_l[f'{prefix}{"_"}{"kf_list"}'] = kf_list
                set_l[f'{prefix}{"_"}{"kf_1"}'] = kf_1
                set_l[f'{prefix}{"_"}{"kf_2"}'] = kf_2
    except Exception as e:
        print(e.args)
    return set_l

"""еще более новая версия от Антона от 25.11.2021 - чтобы кэфы нормально отражались"""
def get_basic_info_in_beginning_v_2(result_json):
    def one_get_sports_id(result_json):
        sport_ids = []
        for sport_id in result_json["sports"]:
            if sport_id.get("name").split(".")[0] == "Волейбол" and sport_id.get("kind") == "segment":
                sport_ids.append(sport_id.get("id"))
        return sport_ids
    """предыдущая версия до того как ссылка сломалась"""
    def get_matсhs_id(result_json, sport_ids):
        matchs_ids = []
        for event in result_json["events"]:
            if event.get("sportId") in sport_ids and \
                    event.get("parentId") and event.get("place") == "live":
                try:
                    matchs_ids.index(event.get('parentId'))
                except:
                    matchs_ids.append(event.get('parentId'))
        return matchs_ids

    def grouper(item):
        return item.get('parentId', -1)

    def result(result_json, matchs_ids):
        ID = []
        values = [(it.get("id", -1), it.get("parentId", -1), it.get('sportId', -1))
                  for it in result_json["events"] if it.get('name').split(" ")[-1] == "сет"]

        grouped_values = groupby(sorted(values, key=lambda it: it[1]), key=lambda it: it[1])

        for key, gvalues in grouped_values:
            if key in matchs_ids:
                v = list(gvalues)
                id, parentId, sportID = list(min(v, key=lambda it: it[0]))
                ID.append({'sport_ids': sportID,
                           'ids': parentId,
                           'urls': f'https://www.fonbet.ru/live/volleyball/{sportID}/{parentId}',
                           'set_ids': id})
        return ID

    sport_ids = one_get_sports_id(result_json)
    matchs_ids = get_matсhs_id(result_json, sport_ids)
    return result(result_json, matchs_ids)



""" Новая версия"""
def get_basic_info_in_beginning(result_json):
    sport_ids = []
    urls = []
    ids = []
    set_ids = []
    """1"""
    def one_get_sports_id(result_json):
        sport_ids = []
        urls = []
        ids = []
        set_ids = []
        for sport_id in result_json["sports"]:
            if sport_id.get("name").split(".")[0] == "Волейбол" and sport_id.get("kind") == "segment":
                sport_ids.append(sport_id.get("id"))
        return sport_ids
    """2"""
    IDS = []
    IDS_SET = []
    def two_get_set_ids_urs(result_json, sport_ids):
        for event in result_json["events"]:
            if event.get("sportId") in sport_ids and event.get("level") == 1:
                ids_dict = {'sport_ids': event.get("sportId"), 'ids': event.get("id"),
                            'urls': f'https://www.fonbet.ru/live/volleyball/{event.get("sportId")}/{event.get("id")}'}
                ids.append(event.get("id"))
                IDS.append(ids_dict)
                urls.append(f'https://www.fonbet.ru/live/volleyball/{event.get("sportId")}/{event.get("id")}')
            elif event.get("sportId") in sport_ids and event.get("level") == 2:
                # print(event.get("id"), event.get("name"))
                ids_set_dict = [event.get("sportId"), event.get("id")]
                IDS_SET.append(ids_set_dict)
                set_ids.append(event.get("id"))
        return set_ids, IDS_SET, urls, ids, IDS
    """3 какие то фильтры """
    def chek_chek(data_all, elem):
        flag = True
        for i in data_all:
            if i[0] == elem:
                flag = False
        return flag
    def process_id_set(list_to_filter):
        data_all = []
        itog = []
        for i in range(len(list_to_filter)):
            data = []
            elem = list_to_filter.pop(0)
            # print(f' eto len list : {len(list_to_filter)}, eto list : {list_to_filter}')
            for el in list_to_filter:
                if el[0] == elem[0]:
                    data.append(el[1])
            chek = chek_chek(data_all, elem[0])
            if chek:
                data.append(elem[1])
                data_all.append([elem[0], data])
        for i in data_all:
            dicti = {'sport_ids': i[0], 'set_ids': i[1]}
            itog.append(dicti)
        return itog
    """4 юнион дикс"""
    def union_dicts_in_begining(IDS, id_list):
        for i in IDS:
            for j in id_list:
                if i.get('sport_ids') == j.get('sport_ids'):
                    i['set_ids'] = j.get('set_ids')
        return IDS
    """ 5 получение итогового словаря"""
    def get_itog_list_for_begining(itog_pred_last):
        for i in itog_pred_last:
            try:
                # print(f'eto i : {i}')
                set_id = min(i.get('set_ids'))
                i['set_ids'] = set_id
            except Exception as e:
                # print('NO set_ids in var itog_pred_last ')
                i['set_ids'] = [0]
                # print(f' eto i v iskl : {i}')
        return itog_pred_last

    sport_ids = one_get_sports_id(result_json)
    set_ids, IDS_SET, urls, ids, IDS = two_get_set_ids_urs(result_json, sport_ids)
    list_to_filter = IDS_SET
    id_list = process_id_set(list_to_filter)
    itog_pred_last = union_dicts_in_begining(IDS, id_list)
    ID = get_itog_list_for_begining(itog_pred_last)
    return ID




def dump_to_file_add(itog, filename):
    lock.acquire()
    try:
        with open(filename,'a+', encoding="utf-8") as f:
            # s = json.dumps(data,ensure_ascii=False,indent=4)
            for chunk in json.JSONEncoder(ensure_ascii=False, indent=4).iterencode(itog):
                f.write(chunk)
    finally:
        lock.release()
def dump_to_file_w(itog, filename):
    lock.acquire()
    try:
        with open(filename,'w', encoding="utf-8") as f:
            # s = json.dumps(data,ensure_ascii=False,indent=4)
            for chunk in json.JSONEncoder(ensure_ascii=False, indent=4).iterencode(itog):
                f.write(chunk)
    finally:
        lock.release()

def add_set_id(ID, result_json):
    for i in ID:
        SPORT_ID = i[0]
        for event in result_json["events"]:
            if event.get("sportId") == SPORT_ID  and event.get("level") == 2:
                i.append(event.get("id"))
    return ID


def get_all_ids(ID):
    IDS_LIST = []
    for i in ID:

        key_lst = ['sport_ids', 'ids', 'urls', 'set_ids']
        value_list = [i[0], i[1], i[2], i[3]]
        my_dict = dict(zip(key_lst, value_list))
        IDS_LIST.append(my_dict)
    return IDS_LIST


"""II Блок функций для обработки get_zaprosov"""

def get_number_teams_set(result_json, sport_ids):
    event_number = None
    team1 = None
    team2 = None
    teams_str = None
    try:
        for event in result_json["events"]:
            # if event.get("sportId") == sport_ids and event.get("level") == 1:
            if event.get("id") == sport_ids and event.get("level") == 1:
                event_number = event.get('num')
                team1 = event.get('team1')
                team2 = event.get('team2')
                teams_str = str(f'{team1} - {team2}')
            # elif event.get("sportId") == sport_ids and event.get("level") == 2:
            #     set_num = event.get('name')
    except Exception as e:
        print(e.args)

    return teams_str, event_number

def get_set_number_by_len_score(len_score):
    set_num = None
    try:
        if len_score == 1:
            set_num = '1-й сет'
        if len_score == 2:
            set_num = '2-й сет'
        if len_score == 3:
            set_num = '3-й сет'
        if len_score == 4:
            set_num = '4-й сет'
        if len_score == 5:
            set_num = '5-й сет'
    except Exception as e:
        print(e.args)
        print("f исключение в функции gget_set_number_by_len_score")
    return set_num

#'25ИТОГ'

def get_score(data):
    pattern_itg = re.compile('ИТОГ')
    pattern = re.compile('\(\d+\*-\d+\)|\(\d+-\d+\*\)|\(\d+-\d+\*\)|\(\*\d+-\d+\)|\d+\W+\d+\)|\d+\W\d+\*\)')
    scr_one = -9999
    scr_two = 0
    END_GAME = False
    set = 0
    set_num = 0
    addd = 1
    try:
        if data != 'Матч не начался':
            SCORE = data.split()
            if SCORE[0] == '(':
                addd = 0
            else:
                addd = 1

            # print(f' eto SCORE_SPLIT {SCORE}, eto len score : {len(SCORE)}, eto score : {SCORE}, eto len(c[:-1]): {len(SCORE[:-1])}')
            for i in reversed(SCORE):
                if not re.findall(pattern_itg, i):
                    if re.match(pattern, i):
                        # print('MATCH PATTERN')
                        set_num = int(SCORE.index(i)) + addd
                        # set_num = int(SCORE.index(i)+1) + int(addd)
                        set = get_set_number_by_len_score(set_num)
                        scr_one = re.sub('[(*)]+', '', i).split('-')[0]
                        scr_two = re.sub('[(*)]+', '', i).split('-')[1]
                        break
                        # print(set_num, scr_one, scr_two)
                else:
                    scr_one = 456789
                    scr_two = 123479
            if set_num == 3 and int(scr_one) == 0 and int(scr_two) == 0:
                END_GAME= True
            else:
                END_GAME= False
        else:
            scr_one = 0
            scr_two = 0

    except Exception as e:
        print('ОШИЮКА В ФУНКЦИИ get_score')
    return [scr_one, scr_two], END_GAME, data, set

"""новая после того как сломалась ссылка"""
def get_koefficients(result_json, set_ids):
    team_1_kf = -1000
    team_2_kf = -1000
    try:
        for k in result_json["customFactors"]:
            if k.get("e") == set_ids:
                for factor in k.get("factors"):
                    if factor.get("f") == 921:
                        team_1_kf= factor.get("v")
                    if factor.get("f") == 923:
                        team_2_kf= factor.get("v")
    except Exception as e:
        print(e.args)
        print(f' ИЗ ЭТИХ ДАННЫХ НЕ ПОЛУЧИЛОСЬ ВЫТАЩИТЬ КОЭФФИЦИЕНТЫ : {set_ids}, k.get("e") : {k.get("e")}, k.get("f") : {k.get("f")}')
        dump_to_file_add([set_ids, k.get("e"), k.get("f")], "ERR_KF.json")
    return [team_1_kf, team_2_kf]


def process_score_list_and_set_l(set_l, scor_info):
    flag= True
    flag_new_set= True
    flag_new_KF= True
    for i in set_l:
        if i == scor_info:
            # print(f'HERE IS : {i}')
            flag = False
            break
    if flag==True:
        for i in set_l:
            if i['set']!= scor_info['set']:
                # print(f'NEW SET')
                set_l.append(scor_info)
                flag_new_set = False
                break
        for i in set_l:
            one = i["scor"]
            twoe = scor_info["scor"]
            if one == twoe:
                # print('True')

                if (i['kf_1'] != scor_info['kf_1']) or (i['kf_2'] != scor_info['kf_2']):
                    set_l.remove(i)
                    set_l.append(scor_info)
                    flag_new_KF = False
                    break
        if (flag_new_set and flag_new_KF):
            set_l.append(scor_info)
    return set_l



def chek_for_adding(i, score_info):
    # print(f' eto i  V начале CHEKING " {i}')
    # print(f' eto score_info : {score_info}')
    try:
        score_info = score_info[0]
        # print(f' eto i CHEKING : {i}')
        # print(f' eto score info - там где счет : {score_info}')
        flag = True
        if len(i) == 0:
            i.append(score_info)
            flag = False
        for el in i:
            # print(f' eto el["koeff"]  : {el["koeff"] }')
            # print(f' eto score info scores " {score_info["scores"]}')
            # print(f'  eto score info KF " {score_info["koeff"]}')
            if type(el) is dict:
                if el['scores'] == score_info['scores'] and el['koeff'] == score_info['koeff']:
                    flag = False
                    break
        if flag:
            for el in i:
                if type(el) is dict:
                    # print(f' eto el["koeff"] : {el["koeff"]}, {el["koeff"][0]}, {score_info["koeff"]}, {score_info["koeff"][0]}, {el["koeff"]==score_info["koeff"]}, {score_info["koeff"]==[-1000, -1000]}'\
                    # f'{el["koeff"]==[-1000, -1000]}')
                    if el['scores'] == score_info['scores'] and el["koeff"]==[-1000, -1000]:
                        # print(
                        #     f' eto el["koeff"] когда равен - 1000 : {el["koeff"]}, eto score_info["koeff"] : {score_info["koeff"]}  ')
                        i.remove(el)
                        i.append(score_info)
                        flag = False
                        break
                    elif el['scores'] == score_info['scores'] and el['koeff'] != [-1000, -1000] :
                        # print(
                        #     f' eto el["koeff"] когда не равен -1000 но скоры равны  : {el["koeff"]}, eto score_info["koeff"] : {score_info["koeff"]} '\
                        # f'eto el["scores"] когда не равен -1000 {el["scores"]}, eto koeff scores : {score_info["scores"] } ')
                        flag = False
                        break
                    else:
                        # print(f'внимание тут новый score-его нужно добавлять : {score_info}')
                        flag = True

        if flag:
            i.append(score_info)
    except Exception as e:
        print(e.args)
        print("f исключение в функции chek_for_adding")
        i = False
    # print(f' eto i  V KONCE CHEKING " {i}')
    return i


""" Добавление данных в итоговый список """
def add_to_games(data_list, game):
    copy_list = data_list.copy()
    # print(f' ETO GAME: {game}')
    try:
        flag = False
        for i in data_list:
            if i['ids'] == game['ids']:
                flag= True
                break
        if flag:
            for i in data_list:
                # print(f' eto i v nachale {i}')
                # print(f' eto i " {i}')
                if i['ids'] == game['ids']:
                    if game['set'] == '1-й сет':
                        rez = chek_for_adding(i['1_set_data'], game['1_set_data'])
                        if rez:
                            # i['1_set_data'].append(rez)
                            i['1_set_data'] = rez
                    elif game['set'] == '2-й сет':
                        rez = chek_for_adding(i['2_set_data'], game['2_set_data'])
                        if rez:
                            # i['2_set_data'].append(rez)
                            i['2_set_data'] = rez
                    elif game['set'] == '3-й сет':
                        # print(f' eto game[3_set_data] : {game["3_set_data"]}')
                        rez = chek_for_adding(i['3_set_data'], game['3_set_data'])
                        # print(f' eto rez 3 SET : {rez}')
                        if rez:
                            # print(f' eto i[3_set_data] DEFORE : {i["3_set_data"]}')
                            i['3_set_data'] = rez
                            # i['3_set_data'].append(rez)
                            # print(f' eto i[3_set_data] AFTER : {i["3_set_data"]}')
                    elif game['set'] == '4-й сет':
                        rez = chek_for_adding(i['4_set_data'], game['4_set_data'])
                        if rez:
                            # i['4_set_data'].append(rez)
                            i['4_set_data'] = rez
                    elif game['set'] == '5-й сет':
                        rez = chek_for_adding(i['5_set_data'], game['5_set_data'])
                        if rez:
                            # i['5_set_data'].append(rez)
                            i['5_set_data'] = rez
                    elif game['set'] == 'ошибки на подаче':
                        continue
                # print(f' eto i v KONCE {i}')
        else:
            data_list.append(game)

    except Exception as e:
        data_list = copy_list
        print(e.args)
    return data_list


""" Основная функция по обработке игры"""
def get_all_info_for_game(i, result_json):
    set_num = None
    try:
        END_GAME = False
        urls = []
        scores = []
        sport_ids = i.get("sport_ids")
        ids = i.get("ids")
        set_ids= i.get("set_ids")
        urls = i.get("urls")
        # set_num = None
        i['1_set_data'] = []
        i['2_set_data'] = []
        i['3_set_data'] = []
        i['4_set_data'] = []
        i['5_set_data'] = []
        i['date'] = str(datetime.datetime.now())
        # teams_str,  event_number = get_number_teams_set(result_json, sport_ids)
        teams_str, event_number = get_number_teams_set(result_json, ids)
        # print(f' eto teams_str, set_num, event_number " {teams_str ,set_num, event_number}')
        i['event_number '] = event_number
        i['teams'] = teams_str
        # print(f' eto SET : {set_num}')
        koeff = get_koefficients(result_json, set_ids)
        # print(f' eto koeffs : {koeff}')
        for el in result_json['eventMiscs']:
            if el.get("id") == ids:
                # print(f' ETO EL COMMENT : {el["comment"]}')
                scores, END_GAME, data, set_num = get_score(el["comment"])
                # print(f' eto rez from get score : {scores}, {set_num}, ETO EL COMMENT : {el["comment"]} ')
        score_info = {'scores': scores, 'koeff': koeff}
        # print(f' eto set_num FROM SCRORES : {set_num}')
        i['set'] = set_num
        i['END_GAME'] = END_GAME

        if set_num == '1-й сет':
            i['1_set_data'] = [score_info]
        elif set_num == '2-й сет':
            i['2_set_data'] = [score_info]
        elif set_num == '3-й сет':
            i['3_set_data'] = [score_info]
        elif set_num == '4-й сет':
            i['4_set_data'] = [score_info]
        elif set_num == '5-й сет':
            i['5_set_data'] = [score_info]
    except Exception as e:
        print(e.args)
        print("f исключение в функции get_all_info_for_game")
    return i





def get_score_bot(data):
    pattern_itg = re.compile('ИТОГ')
    pattern = re.compile('\(\d+\*-\d+\)|\(\d+-\d+\*\)|\(\d+-\d+\*\)|\(\*\d+-\d+\)|\d+\W+\d+\)|\d+\W\d+\*\)')
    scr_one = -9999
    scr_two = 0
    END_GAME = False
    set = 0
    set_num = 0
    addd = 1
    try:
        if data != 'Матч не начался':
            SCORE = data.split()
            if SCORE[0] == '(':
                addd = 0
            else:
                addd = 1

            # print(f' eto SCORE_SPLIT {SCORE}, eto len score : {len(SCORE)}, eto score : {SCORE}, eto len(c[:-1]): {len(SCORE[:-1])}')
            for i in reversed(SCORE):
                if not re.findall(pattern_itg, i):
                    if re.match(pattern, i):
                        # print('MATCH PATTERN')
                        set_num = int(SCORE.index(i)) + addd
                        # set_num = int(SCORE.index(i)+1) + int(addd)
                        set = get_set_number_by_len_score(set_num)
                        scr_one = re.sub('[(*)]+', '', i).split('-')[0]
                        scr_two = re.sub('[(*)]+', '', i).split('-')[1]
                        break
                        # print(set_num, scr_one, scr_two)
                else:
                    scr_one = 456789
                    scr_two = 123479
            if set_num == 3 and int(scr_one) == 0 and int(scr_two) == 0:
                END_GAME= True
            else:
                END_GAME= False
        else:
            scr_one = 0
            scr_two = 0
    except Exception as e:
        print('ОШИЮКА В ФУНКЦИИ get_score')
    return [scr_one, scr_two]






















"""_______________________________________________________________________________________________________________"""

