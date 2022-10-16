# -*- coding: utf-8 -*-
from selenium import webdriver
import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import math
import json
from statistics import mean
import datetime
import fidx
from operator import sub
import threading
lock = threading.RLock()




def dump_to_file_add(itog, filename):
    lock.acquire()
    try:
        with open(filename,'a+', encoding="utf-8") as f:
            # s = json.dumps(data,ensure_ascii=False,indent=4)
            for chunk in json.JSONEncoder(ensure_ascii=False, indent=4).iterencode(itog):
                f.write(chunk)
    finally:
        lock.release()

def dump_to_file(itog, filename):
    lock.acquire()
    try:
        with open(filename,'w', encoding="utf-8") as f:
            # s = json.dumps(data,ensure_ascii=False,indent=4)
            for chunk in json.JSONEncoder(ensure_ascii=False, indent=4).iterencode(itog):
                f.write(chunk)
    finally:
        lock.release()

def normalvid(set_l):
    scor_list = []
    kf_list = []
    scor_one_list = []
    scor_two_list = []

    for i in set_l:
        scor_list.append(i['scor'])
        kf_list.append([i['kf_1'], i['kf_2']])
    assert len(scor_list)==len(kf_list), 'PROBLEM WITH LEN SCORE AND KF'
    for i in scor_list:
        scor_one_list.append(float(i[0]))
        scor_two_list.append(float(i[1]))
    assert len(scor_one_list) == len(scor_two_list)
    if float(scor_list[0][0]) == 0 and float(scor_list[0][1]) == 0:
        kf_1 = kf_list[0][0]
        kf_2 = kf_list[0][1]
    else:
        kf_1 = None
        kf_2 = None

    # print(f' eto scor_list : {scor_list}, eto scor_one_list : {scor_one_list}, eto scor_two_list : {scor_two_list}')
    sub_iter = map(sub, scor_one_list, scor_two_list)
    sub_list = fidx(list(sub_iter))
    return sub_list, kf_1, kf_2, kf_list, scor_list

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

def process_itog_list(itog_list, game_info):
    it_l = []
    first_set = []
    second_set = []
    third_set = []
    four_set = []
    five_set = []
    sub_list_1_set=None
    sub_list_2_set=None
    sub_list_3_set=None
    sub_list_4_set=None
    sub_list_5_set=None

    kf1_1 = None
    kf2_1 =None
    kf1_2 = None
    kf2_2 = None
    kf1_3 = None
    kf2_3 = None
    kf1_4 = None
    kf2_4 = None
    kf1_5 = None
    kf2_5 = None

    kf_1set = None
    kf_2set = None
    kf_3set = None
    kf_4set = None
    kf_5set = None

    scor_l_1set = None
    scor_l_2set = None
    scor_l_3set = None
    scor_l_4set = None
    scor_l_5set = None

    for i in itog_list:
        if i['set'] == '1 сет':
            first_set.append(i)
        elif i['set'] == '2 сет':
            second_set.append(i)
        elif i['set'] == '3 сет':
            third_set.append(i)
        elif i['set'] == '4 сет':
            four_set.append(i)
        elif i['set'] == '5 сет':
            five_set.append(i)
    """ Дополнение - привод движения по счету в нормальный вид с помощью функции normalvid(set_l)"""
    if len(first_set)>0:
        sub_list_1_set, kf1_1, kf2_1, kf_1set, scor_l_1set = normalvid(first_set)
    if len(second_set) > 0:
        sub_list_2_set, kf1_2, kf2_2, kf_2set, scor_l_2set = normalvid(second_set)
    if len(third_set)>0:
        sub_list_3_set, kf1_3, kf2_3, kf_3set, scor_l_3set = normalvid(third_set)
    if len(four_set) > 0:
        sub_list_4_set, kf1_4, kf2_4, kf_4set, scor_l_4set = normalvid(four_set)
    if len(five_set) > 0:
        sub_list_5_set, kf1_5, kf2_5, kf_5set, scor_l_5set = normalvid(five_set)

    # game_info = {'id': id, 'teams': teams, 'data': data}
    itog = {'id': game_info['id'], 'teams': game_info['teams'], 'data': game_info['data'],\
            'first_set': sub_list_1_set,\
            'kf1_1': kf1_1, 'kf2_1': kf2_1,
            'second_set': sub_list_2_set, 'kf1_2': kf1_2, 'kf2_2': kf2_2,
            'third_set': sub_list_3_set, 'kf1_3': kf1_3, 'kf2_3': kf2_3,  \
            'four_set': sub_list_4_set, 'kf1_4': kf1_4, 'kf2_4': kf2_4,\
            'five_set': sub_list_5_set, 'kf1_5': kf1_5, 'kf2_5': kf2_5, \
            'kf_1set': kf_1set, 'kf_2set': kf_2set, 'kf_3set': kf_3set, 'kf_4set': kf_4set, \
            'kf_5set': kf_5set, 'scor_l_1set': scor_l_1set, 'scor_l_2set': scor_l_2set, 'scor_l_3set': scor_l_3set,\
            'scor_l_4set': scor_l_4set, 'scor_l_5set': scor_l_5set}
    return itog



def process_link_dublfirst(event_url, id):
    try:
        driver = webdriver.Chrome()
        driver.get(event_url)
        err = 0
        itog_list = []
        set_l = []
        driver.get(event_url)
        if driver.current_url != event_url:
            for i in range(200):
                driver.get(event_url)
                time.sleep(2)
                if driver.current_url == event_url:
                    break
        itog = []
        game_info = None

        while err<6:
            try:
                while driver.find_elements_by_xpath('//div[@class="ev-comment--1GT4Y"]/div'):
                    print(driver.find_elements_by_xpath('//div[@class="ev-comment--1GT4Y"]/div')[0].text)
                    time.sleep(5)
                time.sleep(5)

                # id = driver.find_elements_by_xpath('//div[@class="menu--HzLjc"]//div[@class="tab--30YXI"][last()]')[0].text #work
                id = id
                scor_list = driver.find_elements_by_xpath('//div[@class="ev-score--2aHgg"]') #work
                scor_1 = scor_list[-2].text #work
                scor_2 = scor_list[-1].text #work
                scor = [scor_1, scor_2] #work
                name_list = driver.find_elements_by_xpath('//span[@class="ev-team__name--3zWY8 _live--2gx4G"]') #work
                teams = str(f'{name_list[0].text} - {name_list[1].text}') #work

                """ Закоментированных данные нет так как пока нет игр в лайве - делаю урезанную версию"""
                set = driver.find_elements_by_xpath('//div[@class="ev-score-table__period-container--3xn3A"]/div[last()]/div')[0].text #work
                try:
                    kf_1 = float(driver.find_elements_by_xpath('//div[@class="v---x8Cq"]')[0].text) #work
                    kf_2 = float(driver.find_elements_by_xpath('//div[@class="v---x8Cq"]')[1].text) #work
                except Exception as e:
                    kf_1 = -1000
                    kf_2 = -1000
                data  = str(datetime.datetime.now())


                scor_info = {'set': set, 'scor': scor, 'kf_1': kf_1, 'kf_2': kf_2}
                game_info = {'id': id, 'teams': teams, 'data': data}
                # print(f' eto game_info : {game_info}')
                # print(f' eto score_info : {scor_info}')
                if len(set_l)==0:
                    set_l.append(scor_info)
                set_l = process_score_list_and_set_l(set_l, scor_info)
                # print(f' eto set_l : {set_l}')
                if set_l not in itog_list:
                    # print(True)
                    # print(f' eto set_l : {set_l}, eto itog_list: {itog_list}')
                    itog_list.append(set_l)
                # print(f' eto itog_list : {itog_list[0]}')
                itog =  process_itog_list(itog_list[0], game_info)
                print(f' eto ITOG AFTER ALL : {itog}')

                dump_to_file_add(itog, "ITERIM_FIRST.json")
                err=0
            except Exception as e:
                time.sleep(1.5)
                end_game_one = driver.find_elements_by_xpath(
                    '//div[@class="match-finished__container--2mad_"]/div[@class="match-finished__container--2mad_"]/span[@class="match-finished__head--1fJMk"]')
                end_game_two = driver.find_elements_by_xpath(
                    '//div[@class="match-finished__container--2mad_"]/span[@class="match-finished__head--1fJMk"]')
                time.sleep(1)
                if not any([end_game_one, end_game_two]):
                    err += 1
                    print(f'may be END GAME OR NOW KOEFFICIENTS: СТОЛЬКО ОШИБОК : {err}, {game_info}, {itog}, NUM_ERROR_LAP : {err}')


                    """ добавляю попытки реконнекта """
                    for i in range(3):
                        driver.get(event_url)
                        time.sleep(3)
                        # print(f' eto curr url : {driver.current_url}, eto event_url : {event_url}')
                        if driver.current_url == event_url:
                            break
                else:
                    try:
                        print(f'END GAME: {end_game_one[0].text}, {end_game_two[0].text}')
                    except Exception as e:
                        print('END GAME BUT CANT PRINT TEXT')
                    err=10
                    dump_to_file_add(itog, "ITERIM_FIRST.json")

                    break
        print(f' eto ITOG V SAMOM KONCE: {itog}')
        driver.quit()
        dump_to_file_add(itog, "ITOG_FIRST.json")
    except Exception as e:
        print(f' {e.args} on this URL : {event_url}')

def process_link_dublsecond(event_url, id):
    try:
        driver = webdriver.Chrome()
        driver.get(event_url)
        err = 0
        itog_list = []
        set_l = []
        driver.get(event_url)
        if driver.current_url != event_url:
            for i in range(200):
                driver.get(event_url)
                time.sleep(2)
                if driver.current_url == event_url:
                    break
        itog = []
        game_info = None

        while err<6:
            try:
                while driver.find_elements_by_xpath('//div[@class="ev-comment--1GT4Y"]/div'):
                    print(driver.find_elements_by_xpath('//div[@class="ev-comment--1GT4Y"]/div')[0].text)
                    time.sleep(5)
                time.sleep(5)

                id = id
                scor_list = driver.find_elements_by_xpath('//div[@class="ev-score--2aHgg"]') #work
                scor_1 = scor_list[-2].text #work
                scor_2 = scor_list[-1].text #work
                scor = [scor_1, scor_2] #work
                name_list = driver.find_elements_by_xpath('//span[@class="ev-team__name--3zWY8 _live--2gx4G"]') #work
                teams = str(f'{name_list[0].text} - {name_list[1].text}') #work

                """ Закоментированных данные нет так как пока нет игр в лайве - делаю урезанную версию"""
                set = driver.find_elements_by_xpath('//div[@class="ev-score-table__period-container--3xn3A"]/div[last()]/div')[0].text #work
                try:
                    kf_1 = float(driver.find_elements_by_xpath('//div[@class="v---x8Cq"]')[0].text) #work
                    kf_2 = float(driver.find_elements_by_xpath('//div[@class="v---x8Cq"]')[1].text) #work
                except Exception as e:
                    kf_1 = -1000
                    kf_2 = -1000
                data  = str(datetime.datetime.now())


                scor_info = {'set': set, 'scor': scor, 'kf_1': kf_1, 'kf_2': kf_2}
                game_info = {'id': id, 'teams': teams, 'data': data}
                # print(f' eto game_info : {game_info}')
                # print(f' eto score_info : {scor_info}')
                if len(set_l)==0:
                    set_l.append(scor_info)
                set_l = process_score_list_and_set_l(set_l, scor_info)
                # print(f' eto set_l : {set_l}')
                if set_l not in itog_list:
                    # print(True)
                    # print(f' eto set_l : {set_l}, eto itog_list: {itog_list}')
                    itog_list.append(set_l)
                # print(f' eto itog_list : {itog_list[0]}')
                itog =  process_itog_list(itog_list[0], game_info)
                print(f' eto ITOG AFTER ALL : {itog}')

                dump_to_file_add(itog, "ITERIM_SECOND.json")
                err=0
            except Exception as e:
                time.sleep(1.5)
                end_game_one = driver.find_elements_by_xpath(
                    '//div[@class="match-finished__container--2mad_"]/div[@class="match-finished__container--2mad_"]/span[@class="match-finished__head--1fJMk"]')
                end_game_two = driver.find_elements_by_xpath(
                    '//div[@class="match-finished__container--2mad_"]/span[@class="match-finished__head--1fJMk"]')
                time.sleep(1)
                if not any([end_game_one, end_game_two]):
                    err += 1
                    print(f'may be END GAME OR NOW KOEFFICIENTS: СТОЛЬКО ОШИБОК : {err}, {game_info}, {itog}, NUM_ERROR_LAP : {err}')


                    """ добавляю попытки реконнекта """
                    for i in range(3):
                        driver.get(event_url)
                        time.sleep(3)
                        # print(f' eto curr url : {driver.current_url}, eto event_url : {event_url}')
                        if driver.current_url == event_url:
                            break
                else:
                    try:
                        print(f'END GAME: {end_game_one[0].text}, {end_game_two[0].text}')
                    except Exception as e:
                        print('END GAME BUT CANT PRINT TEXT')
                    err=10
                    dump_to_file_add(itog, "ITERIM_SECOND.json")

                    break
        print(f' eto ITOG V SAMOM KONCE: {itog}')
        driver.quit()
        dump_to_file_add(itog, "ITOG_SECOND.json")
    except Exception as e:
        print(f' {e.args} on this URL : {event_url}')

