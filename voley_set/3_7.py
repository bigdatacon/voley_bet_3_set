
# -*- coding: utf-8 -*-
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor
from selenium.common.exceptions import WebDriverException
import time
import json
# import browser_cookie3
import datetime
# from scratches_req import get_set_number_by_len_score, get_score_bot

def set_pari_one_click():
    flag_one_click = False
    while not flag_one_click:
        print('не нажатa кнопка pari_one_click')
        try:
            pari_one_click = driver.find_element(By.XPATH, '//span[contains(@class, "switch--TWHeG _use_color_settings--1aPeu")]')
            time.sleep(1)
            if pari_one_click.get_attribute("class").split()[-1].split("-")[0] == "_off":
                pari_one_click.click()
            else:
                print("Ставка в один клик установлена")
                flag_one_click = True
        except Exception as e:
            flag_one_click = False
            print('"Эксепшн в функции set_pari_one_click : не нажал на кнопку пари в 1 клик')

def close_spasibo(driver):
    spasibo_spis = driver.find_elements(By.XPATH, './/i[@class="icon--3NKYN"]')
    if len(spasibo_spis) != 0:
        print(f' есть кнопка спасибо : {len(spasibo_spis)}')
        flag_spasibo_click = False
        print('ПЫТАЮС ЗАКРЫТЬ КНОПКУ СПАСИБО')
        while not flag_spasibo_click:
            print('не нажатa кнопка cпасибо')
            try:
                spasibo = driver.find_elements(By.XPATH, './/i[@class="icon--3NKYN"]')[0]
                time.sleep(1)
                spasibo.click()
                print('DID CLICK FOR SPASIBO')
                spasibo_spis = driver.find_elements(By.XPATH, './/i[@class="icon--3NKYN"]')
                time.sleep(0.8)

                print(f' Длина  spasibo : {len(spasibo_spis)}')
                if len(spasibo_spis) == 0:
                    flag_spasibo_click= True
            except Exception as e:
                flag_spasibo_click = False
                print('Эксепшн в функции close_spasibo не нажал на кнопку спасибо')

def connection_to_fb(driver):

    url = 'https://www.fonbet.ru/live/'
    driver.get(url)
    time.sleep(3)
    for i in range(7):
        if driver.current_url != url:
            driver.get(url)
            time.sleep(5)
            print(f' {i}: try to connect to {url}, this current_url : {driver.current_url}')
    print(f' connect to CORRECT URL : {driver.current_url}')

    entering = driver.find_elements_by_xpath(
        '//div[@id = "headerContainer"]//a[@class="header-btn _login-btn"]')
    time.sleep(2)
    while len(entering) == 0:
        print(f'не нашел кнопку ВХОД')
        entering = driver.find_elements_by_xpath(
            '//div[@id = "headerContainer"]//a[@class="header-btn _login-btn"]')
        time.sleep(2)
    print('DO')
    time.sleep(0.6)
    entering[0].click()
    time.sleep(0.6)
    print('приступил к вводу логина')
    input_login = driver.find_elements_by_xpath('(//input[@data-name = "edit"])[1]')
    time.sleep(0.5)
    input_login[0].send_keys('+79266745962')
    time.sleep(0.5)
    input_password = driver.find_elements_by_xpath('(//input[@data-name = "edit"])[2]')
    time.sleep(0.5)
    input_password[0].send_keys('Link1789')
    time.sleep(0.5)
    input_password[0].send_keys(Keys.ENTER)
    time.sleep(0.5)

    close_adv_pre = driver.find_elements_by_xpath('//i[@class="icon--3NKYN"]')

    time.sleep(1.5)
    if len(close_adv_pre) > 0:
        print(f' ЕСТЬ КНОПКА ЗАКРЫТЬ РЕКЛАМУ для всех игр')
        flagg_pre = True
    print('ищу кнопку закрыть рекламу большое рекламное предложение ')
    while flagg_pre:
        print('ЗДЕСЬ КНОПКА С РЕКЛАМОЙ - которую нужно зарыть')
        try:
            close_adv_pre[0].click()
            time.sleep(0.4)
            print('CLOSE ADV BUTTON CLICK')
            flagg_pre = False
        except Exception as e:
            print('ВСПЛЫВАЮЩЕЕ окно закрыть не удалось ')
    else:
        print('NO ADV BUTTON')

    print('ищу кнопку закрыть рекламу')
    close_adv = driver.find_elements_by_xpath('//div[contains(@class, "close-button")]')
    time.sleep(1.5)
    if len(close_adv) > 0:
        print(f' ЕСТЬ КНОПКА ЗАКРЫТЬ РЕКЛАМУ')
        flagg = True
    while flagg:
        print('ЗДЕСЬ КНОПКА С РЕКЛАМОЙ - которую нужно зарыть')
        try:
            close_adv[0].click()
            time.sleep(0.4)
            print('CLOSE ADV BUTTON CLICK')
            flagg = False
        except Exception as e:
            print('ВСПЛЫВАЮЩЕЕ окно закрыть не удалось ')
    else:
        print('NO ADV BUTTON')

    try:
        pari_one_click = driver.find_element(By.XPATH ,'//span[contains(@class, "switch--TWHeG _use_color_settings--1aPeu")]')
        if pari_one_click.get_attribute("class").split()[-1].split("-")[0] == "_off":
            pari_one_click.click()
        else:
            print("Ставка в один клик уже установлена")
    except Exception as er:
        print(er.args)
    print("VHOD _-------------------------------------------")
    return True


def get_index_of_event(annot_1_string, annot_2_string):
    list_events = [annot_1_string, annot_2_string]
    for i in list_events:
        if i == 'Победа в 3м сете':
            print(f'CORRECT SET в фцнкции get_index_of_event: {i}')
            ind_bet = list_events.index(i)
        else:
            print(f'INCORRECT SET в фцнкции get_index_of_event: {i}')
            ind_bet = 1
    return ind_bet

make_bet = []


def make_main_bet(bet, index_team):

    try:
        print(f'НАЧАЛ ДВИЖЕНИЕ В ФУНКЦИИ make_main_bet(bet, index_team)')
        print(f', eto index_team : {index_team}, это тип index_team: {type(index_team)}')
        print(f'пробую поставить')
        bet.click()
        print(f'кликнул по ставке ')
        time.sleep(12)
    except Exception as e:
        print( f"Эксепшн в функции make_main_bet в непосредственном клике по ставке : {e.args}, жду 10 сек")
        time.sleep(10)
        teams = item.find_elements(By.XPATH, './/div[@class="cell-wrap--phQzD"]')
        if  int(index_team) == int(0):
            bet = teams[0]
        else:
            bet = teams[1]
        try:
            print(f'пробую поставить повторно после эксепшн ')
            bet.click()
            print(f'кликнул по ставке повторно после эксепшн ')
            time.sleep(12)
        except Exception as e:
            print(f"Эксепшн в функции make_main_bet  в непосредственном клике по ставке после эксепшн : {e.args},")






make_bet = []
if __name__ == '__main__':
    """Версия для обработки списка """
    driver = webdriver.Chrome()
    url_live = 'https://www.fonbet.ru/live/'
    driver.get(url_live)
    time.sleep(5)
    base_time = datetime.datetime.now()

    id_list = []

    try:
        entering = driver.find_elements_by_xpath(
            '//div[@id = "headerContainer"]//a[@class="header-btn _login-btn"]')
        time.sleep(2.5)
        if len(entering)> 0:
            print(f' КНОПКА ВХОД НЕ НАЖАТА')
            try:
                connection_to_fb(driver)
            except Exception as e:
                print('не получилось законнектиться')
        else:
            driver.get(url_live)
            time.sleep(2)
    except Exception as e:
        print(f'BAD BAD problem in connection : {driver.current_url}')


        # print(f'connect to {driver.current_url}')
        # time.sleep(3)

    while True:
        try:
            time.sleep(5)
            print(f'OBRABOTKA NOVOI PORCII IGR: {datetime.datetime.now()}')
            with open("result_from_voley.json", "r", encoding='utf-8') as read_file:
                read_bet_data = json.load(read_file)
            for i in read_bet_data:
                if i.get('event_number ') not in make_bet:
                    print(f' WOW : THIS NEW ID  {datetime.datetime.now()}: {i.get("teams")}, это i.get("event_number ")  {i.get("event_number ") }, eto '
                          f'make_bet : {make_bet}')
                    id_list.append(i)
            """ Убираю всплывающее окно если есть"""

            print(f'проверяю длину id_list')
            if len(id_list)> 0:
                print(f' eto len id_list до цикла : {len(id_list)}')
                for elem in id_list:
                    print(f' eto len id_list в начале  : {len(id_list)}')
                    make_bet.append(elem.get('event_number '))
                    print(f'eto make_bet после добавления : {make_bet}')
                    try:
                        print(f'получаю данные из json')
                        url = elem.get('urls')
                        bet_team = elem.get('who_bet')
                        probability = elem.get('winner_prob')
                        if probability <0.6:
                            print('NE CORRECT PROBABILITY')
                        print(f' eto url: {url}, eto bet_team: {bet_team}, eto probability: {probability}')

                        driver.switch_to.window(driver.window_handles[0])
                        while len(driver.window_handles) < 2:
                            driver.switch_to.new_window()
                            time.sleep(1)
                        # driver.switch_to.new_window()
                        # time.sleep(1.4)

                        driver.get(url)
                        time.sleep(5)

                        for _ in range(3):
                            print(f' проверяю что на правильной странице')
                            if driver.current_url != url:
                                print('не удалось зайти на страницу игры, делаю повторный вход')
                                driver.get(url)
                                time.sleep(4)
                            else:
                                print(f'страница верная {driver.current_url} == {url}')
                                break
                        else:
                            id_list.remove(elem)
                            driver.close()
                            time.sleep(1)
                            driver.switch_to.window(driver.window_handles[0])
                            print('не удалось зайти на страницу игры')
                            continue


                        time.sleep(4)
                        set_pari_one_click()
                        print(f'ЗАКРЫВАЮ СПАСИБО ЕСЛИ ЕСТЬ на старте')
                        close_spasibo(driver)

                        table_wins = driver.find_element(By.XPATH, '//div[@class="group--1Ws2S"]')
                        print(f'формирую список items')
                        items = table_wins.find_elements(By.XPATH, './/div[@class="market-group-box--iAdNd"]')
                        if len(items)>0:
                            print(f'items не пустой : {len(items)} - начинаю проход по странице')
                            for item in items:
                                if item.text.split("\n")[0] == "Победа в 3‑м сете":
                                    text = item.text.split("\n")[0].replace('\u2011', '')
                                    print(f'ALARMA : здесь есть 3 сет : {text}')
                                    teams = item.find_elements(By.XPATH, './/div[@class="cell-wrap--phQzD"]')
                                    # team_one = WebDriverWait(driver, 20).until(
                                    #     EC.element_to_be_clickable((item.find_elements(By.XPATH, './/div[@class="cell-wrap--phQzD"]'))[0]))
                                    # team_two = WebDriverWait(driver, 20).until(
                                    #     EC.element_to_be_clickable((item.find_elements(By.XPATH, './/div[@class="cell-wrap--phQzD"]'))[1]))

                                    def get_score_kf(item):
                                        score_one = None
                                        score_two = None
                                        try:
                                            score_one = item.find_elements(By.XPATH, './/div[@class="v--GM-zl"]')[
                                                0].text
                                            time.sleep(0.2)
                                            score_two = item.find_elements(By.XPATH, './/div[@class="v--GM-zl"]')[
                                                1].text
                                            time.sleep(0.2)
                                        except Exception as e:
                                            print(f' Эксепшн в функции get_score_kf(item), причина : {e.args}')
                                            score_one = None
                                            score_two = None
                                        return float(score_one), float(score_two)

                                    print(f'получаю кэфы')
                                    score_one, score_two = get_score_kf(item)
                                    print(f' eto score_one, score_two : {score_one}, {score_two}')

                                    if bet_team == 1:
                                        try:
                                            print('пробую ставить на команду 1')
                                            index_team = int(0)
                                            if score_one is not None and score_one> 1:
                                                print(f' KEF > 1.5 : {score_one}, делаю ставку')

                                                make_main_bet(teams[0], index_team)
                                            else:
                                                print(f' KEF < 1.5 : {score_one}, не делаю ставку')
                                            # team_one = WebDriverWait(teams[0], 20).until(EC.visibility_of_element_located(
                                            #     (By.XPATH, './/div[contains(@class, "selectable")]')))

                                            # team_one.click()
                                            print(f'кликнул по ставке на команду 1 : {datetime.datetime.now()}')
                                        except:
                                            print("Эксепшн в ставке на ком 1 : Ставка заблокирована")
                                    else:
                                        try:
                                            print('пробую ставить на команду 2')
                                            # team_two = WebDriverWait(teams[1], 20).until(EC.visibility_of_element_located(
                                            #     (By.XPATH, './/div[contains(@class, "selectable")]')))
                                            # team_two.click()

                                            index_team = int(1)
                                            if score_two is not None and score_two > 1:
                                                print(f' KEF > 1.5 : {score_two}, делаю ставку')
                                                make_main_bet(teams[1], index_team)
                                            else:
                                                print(f' KEF < 1.5 : {score_two}, не делаю ставку')
                                            print(f'кликнул по ставке на команду 2 : {datetime.datetime.now()}')
                                        except:
                                            print("Эксепшн в ставке на ком 2 : Ставка заблокирована")

                                    print(f' удаляю элемент')
                                    id_list.remove(elem)
                                    print(f' закрываю драйвер')
                                    driver.close()
                                    time.sleep(1)
                                    print(f' переключаюсь на предыдущее окно')
                                    driver.switch_to.window(driver.window_handles[0])
                                    print(f' переключился на предыдущее окно')
                                    break
                            else:
                                print(f'ВНИМАНИЕ НЕТ  нет 3 сета - удаляю эелемент')
                                print(f' удаляю элемент')
                                id_list.remove(elem)
                                print(f' закрываю драйвер')
                                driver.close()
                                time.sleep(1)
                                print(f' переключаюсь на предыдущее окно')
                                driver.switch_to.window(driver.window_handles[0])
                                print(f' переключился на предыдущее окно')
                                break
                        else:
                            print(f'items пустой : {len(items)} - удаляю элемент')
                            id_list.remove(elem)



                    except Exception as e:
                        print(f'Эксепшн в обработке url Из json : {datetime.datetime.now()}')
                        print(f'удаляю элемент в самом эксепшн')
                        id_list.remove(elem)
                        print(f'на печать аргументы ошибки в самом эксепшн : {e.args}')
        except Exception as e:
            print(f'Эксепшн:  ошибка в самом начале : {e.args}, {e.__cause__}, {e.__context__} : {datetime.datetime.now()}')


            # teams = item.find_elements(By.XPATH, './/div[@class="cell-wrap--phQzD"]')
            # score_one  = item.find_elements(By.XPATH, './/div[@class="v--GM-zl"]')[0].text
            # score_two = item.find_elements(By.XPATH, './/div[@class="v--GM-zl"]')[1].text
            # print(f' eto score_one, score_two : {float(score_one)}, {float(score_two)}')
            # print(float(score_one)>1.5)