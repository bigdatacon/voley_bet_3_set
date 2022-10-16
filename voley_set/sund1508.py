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
import requests
import browser_cookie3
import pprint
from datetime import datetime
import schedule
import time
from copy import deepcopy

#то что ниже закомениторовано работает!!! Не удаляй
from scratches_req import get_number_teams_set, get_koefficients, get_score, chek_for_adding, add_set_id, \
    get_all_ids, dump_to_file_add, get_all_info_for_game, add_to_games, dump_to_file_w, get_basic_info_in_beginning, \
    get_sub_list, get_normal_vid_scores, add_link_to_LINKS, add_to_analize_prior, get_basic_info_in_beginning_v_2

# from scratches_rea_no_change_kf import get_number_teams_set, get_koefficients, get_score, chek_for_adding, add_set_id, \
#     get_all_ids, dump_to_file_add, get_all_info_for_game, add_to_games, dump_to_file_w, get_basic_info_in_beginning, \
#     get_sub_list, get_normal_vid_scores, add_link_to_LINKS, add_to_analize_prior
"""_______________________________________________________________________________________________________________"""
headers = {"sec-fetch-dest": "document",
"sec-fetch-mode": "navigate",
"sec-fetch-site": "none",
"sec-fetch-user": "?1",
"upgrade-insecure-requests": "1",
"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"}
# events[?id==`29437252`]

# eto ID LAST eto ID : [{'sport_ids': 54356, 'ids': 31336860, 'urls': 'https://www.fonbet.ru/live/volleyball/54356/31336860', 'set_ids': 31348379}, {'sport_ids': 14344, 'ids': 31271868, 'urls': 'https://www.fonbet.ru/live/volleyball/14344/31271868', 'set_ids': 31271869}, {'sport_ids': 54356, 'ids': 31336861, 'urls': 'https://www.fonbet.ru/live/volleyball/54356/31336861', 'set_ids': 31348379}, {'sport_ids': 46933, 'ids': 31337311, 'urls': 'https://www.fonbet.ru/live/volleyball/46933/31337311', 'set_ids': 31348390}, {'sport_ids': 26979, 'ids': 31336843, 'urls': 'https://www.fonbet.ru/live/volleyball/26979/31336843', 'set_ids': 31348407}, {'sport_ids': 42493, 'ids': 31336211, 'urls': 'https://www.fonbet.ru/live/volleyball/42493/31336211', 'set_ids': 31348401}]
# eto ID NEW eto ID : [{'sport_ids': 14344, 'ids': 31271868, 'urls': 'https://www.fonbet.ru/live/volleyball/14344/31271868', 'set_ids': 31271869}, {'sport_ids': 42493, 'ids': 31336211, 'urls': 'https://www.fonbet.ru/live/volleyball/42493/31336211', 'set_ids': 31348401}, {'sport_ids': 26979, 'ids': 31336843, 'urls': 'https://www.fonbet.ru/live/volleyball/26979/31336843', 'set_ids': 31348407}, {'sport_ids': 54356, 'ids': 31336860, 'urls': 'https://www.fonbet.ru/live/volleyball/54356/31336860', 'set_ids': 31348477}, {'sport_ids': 54356, 'ids': 31336861, 'urls': 'https://www.fonbet.ru/live/volleyball/54356/31336861', 'set_ids': 31348379}, {'sport_ids': 46933, 'ids': 31337311, 'urls': 'https://www.fonbet.ru/live/volleyball/46933/31337311', 'set_ids': 31348390}, {'sport_ids': 46932, 'ids': 31337312, 'urls': 'https://www.fonbet.ru/live/volleyball/46932/31337312', 'set_ids': 31349216}]
def main():
    lap = 0
    GAMES = []
    zapisi_schetchic = 0
    n_sec = 6.4
    time_pass = 0
    LINKS = []
    test_links_for_GAMES = []
    ERR = []
    analize_2 = []
    ids_for_analize = []
    # result_json = []
    while True:
        try:
            GAMES_COPY = []
            """прежний не работает"""
            # result_json = requests.get(
            #     "https://line510.bkfon-resources.com/live/updatesFromVersion/6043867316/ru/?5d98b5an3rcksbwdycr&sysId=1", headers=headers).json()
            # dump_to_file_w(result_json, 'result_json.json')

            """ДО 09.04.22 Новое с линией работает,  но это еще нужно проверить нужно что там лайв корректно отрабатывает"""
            # result_json = requests.get(
            #     "https://line110.bkfon-resources.com/events/list?lang=ru&scopeMarket=1600&version=6819238395",
            #     headers=headers).json()
            """Это от 09.04.22"""
            # result_json = requests.get(
            #     "https://line01w.bk6bba-resources.com/events/list?lang=ru&version=7807280591&scopeMarket=1600",
            #     headers=headers).json()



            result_json = requests.get(
                "https://line04w.bk6bba-resources.com/events/list?lang=ru&version=8684406733&scopeMarket=1600",
                headers=headers).json()


            dump_to_file_w(result_json, 'result_json.json')


            ID = get_basic_info_in_beginning_v_2(result_json)
            # print(f'eto ID : {ID}')
            lap +=1
            for i in ID:
                i = get_all_info_for_game(i, result_json)
                GAMES = add_to_games(GAMES, i)
            LINKS = add_link_to_LINKS(ID, LINKS)
            for i in GAMES:
                i = get_normal_vid_scores(i)
                # print(f' ETO GAME : {i}')
            GAMES_COPY = deepcopy(GAMES)
            for i in analize_2:
                idd = i.get('game').get('ids')
                if idd not in ids_for_analize:
                    # print(f' THIS ID NEW : {idd}')
                    ids_for_analize.append(idd)
            for i in GAMES_COPY:
                if i.get('ids') not in ids_for_analize:
                    adding = add_to_analize_prior(analize_2, i)
                    if adding!= None:
                        real_add = dict(deepcopy(adding))
                        # print(f'eto adding : {real_add}')
                        # print(f' eto 3 set v adding : {real_add.get("3_set_data")}')
                        # print(f' eto 3 set v adding : {real_add.get("3_set_data")}')
                        # assert len(real_add.get('3_set_data')) == 1, 'НЕ ПРАВИЛЬНО ПОЛУЧЕНАЯ ИГРА ДЛЯ ДОБАВЛЕНИЯ'
                        assert len(real_add.get('3_set_data')) == 1, 'НЕ ПРАВИЛЬНО ПОЛУЧЕНАЯ ИГРА ДЛЯ ДОБАВЛЕНИЯ'
                        to_rec = {'game' : real_add}
                        # print(f' eto to rec : {to_rec}')
                        analize_2.append(deepcopy(to_rec))
                        to_rec.clear()
            dump_to_file_w(GAMES, 'GAMES.json')
            # print(f'eto GAMES:{GAMES}')
            dump_to_file_w(deepcopy(analize_2), 'for_analize_PRIORITET.json')
            time_pass += n_sec
            test_links_for_GAMES = add_link_to_LINKS(GAMES, test_links_for_GAMES)
            print(f'  eto LAP : {lap}, eto time_pass : {time_pass} ----- len LINKS : {len(LINKS)}, len GAMES : {len(GAMES)}, eto len test_links_for_GAMES: {len(test_links_for_GAMES)}, eto len analize_2 : {len(analize_2)} ')
            time.sleep(n_sec)
            # assert len(LINKS) == len(GAMES)==len(test_links_for_GAMES), "WRONG PARS LINKS"
        except Exception as e:
            print(e.args)
            ERR.append(result_json)
            dump_to_file_w(ERR, 'ERR.json')
            print("f исключение в функции MAIN ")


if __name__=='__main__':
    main()




