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
import numpy as np
import tqdm
import datetime
import statistics
from func_0_pred_obr_aft_pars import *
from func_for_kf_aft_pars import *
from func_3_for_deep_lch import *
from sklearn.linear_model import LogisticRegression
# model = LinearRegression()
model =  LogisticRegression(C=10, tol=0.01,  max_iter=10000)

import pickle
import pandas as pd

# filename = 'finalized_model_all.sav'
filename = 'finalized_model_all_fb.sav'
loaded_model = pickle.load(open(filename, 'rb'))


def make_itog_df(data_it):
    try:
        # print('ЧАСТЬ 1')
        # with open("for_analize_PRIORITET.json", "r", encoding='utf-8') as read_file:
        #     data = json.load(read_file)
        # print(len(data))
        # data_it = []
        # for i in data:
        #     try:
        #         if i["game"] not in data_it:
        #             data_it.append(i["game"])
        #     except Exception as e:
        #         continue


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
                '3_set_kf_1', '3_set_kf_2', 'source', 'sex' , 'urls'
              ]]
        df.to_csv("pdObj.csv")
        list_of_column_names =  ['date', 'event_number ', 'teams','set1','set2', 'set3', 'kf1_1', 'kf2_1', 'kf1_2', 'kf2_2', 'kf1_3','kf2_3',
                                 'source', 'sex', 'urls']
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
            assert float(set[-1])!= 0, f'{set}Не корректно отработала функция get_pred_obrab_data в части проверки пропусков'
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
                # print(f' eto set_1, set_2, set_3: {set_1, set_2, set_3}')
                # i['game'] = str(set_1,set_2,set_3)
                i['game'] = int(set_1+ set_2+ set_3)

            return data
        data = notmalize_set(itg)
        data_itogo = get_correct_data(data, True)

        data = get_pred_obrab_data(data_itogo)
        print(f'eto длина списка до удаления сетов где не выявлен победитель : {len(data)}')
        data = dell_sets_with_no_win(data)
        print(f'eto длина списка после удаления сетов где не выявлен победитель : {len(data)}')

        data = get_who_win_3_set_for_data(data)

        df = pd.DataFrame.from_dict(data, orient='columns')
        df = df[['teams', 'source', 'sex', 'set1', 'set2', 'set3', 'game',
                'kf1_3', 'kf2_3', '1_set_scr_1', '1_set_scr_2', '1_set_len_set',
                '1_set_FLAG_LEN_SCR', '2_set_scr_1', '2_set_scr_2', '2_set_len_set', '2_set_FLAG_LEN_SCR', 'urls', 'event_number ']]

        js = df.to_json(orient = 'records')
        data  = json.loads(js)

        with open('AFT_PARS_data_pred_obr.json', 'w') as f:
            f.write(json.dumps(data))
        print('ALL DATA write to file')

        print('ЧАСТЬ 2')



        with open("AFT_PARS_data_pred_obr.json") as f:
            data = json.load(f)

        itog = []
        for i in data:
            i = pred_obr_base_aft_pars(i)
            itog.append(i)


        with open('AFT_PARS_data_2_obr_base.json', 'w') as f:
            f.write(json.dumps(itog))


        df = pd.DataFrame.from_dict(itog)

        df.to_csv('withkfaft_pars.csv')

        base_columns = ['teams', 'source', 'sex', 'set1', 'set2', 'set3', 'game', 'kf1_3',
               'kf2_3', '1_set_scr_1', '1_set_scr_2', '1_set_len_set',
               '1_set_FLAG_LEN_SCR', '2_set_scr_1', '2_set_scr_2', '2_set_len_set',
               '2_set_FLAG_LEN_SCR', 'len_set_1 ', 'len_set_2', 'win_1_set',
               'win_2_set', 'win_3_set', 'dif_1_set', 'dif_2_set', 'adv_1_1_set',
               'adv_2_1_set', 'adv_1_2_set', 'adv_2_2_set', 'max_1_set', 'min_1_set',
               'max_2_set', 'min_2_set', 'score_befor_3', 'favor', 'quant_teas_1_set',
               'otn_teas_set_1_set', 'quant_teas_2_set', 'otn_teas_set_2_set',
               'quant_pl_2_1_set_1_team', 'otn_pl_2_set_1_set_1_team',
               'quant_pl_2_2_set_1_team', 'otn_pl_2_set_2_set_1_team',
               'quant_pl_2_1_set_2_team', 'otn_pl_2_set_1_set_2_team',
               'quant_pl_2_2_set_2_team', 'otn_pl_2_set_2_set_2_team', 'mean_33_1_set',
               'mean_66_1_set', 'mean_99_1_set', 'mean_33_2_set', 'mean_66_2_set',
               'mean_99_2_set', 'l_ch_1_set', 'l_ch_to_len_1_set', 'l_ch_2_set',
               'l_ch_to_len_2_set']

        non_base  = ['teams', 'source', 'sex', 'set1', 'set2', 'set3', 'game', 'kf1_3',
               'kf2_3', '1_set_scr_1', '1_set_scr_2', '1_set_len_set',
               '1_set_FLAG_LEN_SCR', '2_set_scr_1', '2_set_scr_2', '2_set_len_set',
               '2_set_FLAG_LEN_SCR', 'len_set_1 ', 'len_set_2', 'win_1_set',
               'win_2_set', 'win_3_set', 'dif_1_set', 'dif_2_set', 'adv_1_1_set',
               'adv_2_1_set', 'adv_1_2_set', 'adv_2_2_set', 'max_1_set', 'min_1_set',
               'max_2_set', 'min_2_set', 'score_befor_3', 'favor', 'quant_teas_1_set',
               'otn_teas_set_1_set', 'quant_teas_2_set', 'otn_teas_set_2_set',
               'quant_pl_2_1_set_1_team', 'otn_pl_2_set_1_set_1_team',
               'quant_pl_2_2_set_1_team', 'otn_pl_2_set_2_set_1_team',
               'quant_pl_2_1_set_2_team', 'otn_pl_2_set_1_set_2_team',
               'quant_pl_2_2_set_2_team', 'otn_pl_2_set_2_set_2_team', 'mean_33_1_set',
               'mean_66_1_set', 'mean_99_1_set', 'mean_33_2_set', 'mean_66_2_set',
               'mean_99_2_set', 'l_ch_1_set', 'l_ch_to_len_1_set', 'l_ch_2_set',
               'l_ch_to_len_2_set']

        print('завершена ЧАСТЬ 2')

        print('это ЧАСТЬ 3')



        with open("AFT_PARS_data_2_obr_base.json") as f:
            data= json.load(f)

        data = data[:]


        # """ Прогоняю на весь список """
        itog =  []
        data_itog= []
        for i in data:
            try:

                itog = []
                set1 = i['set1']
                set1 = del_zero_in_set(set1)
                set2 = i['set2']
                set2 = del_zero_in_set(set2)
                data = del_zero_in_set(data)
                sets = [set1, set2]
                for set in sets:
                    num_set = sets.index(set)+1
                    rez = get_list_of_lead_changes(set)
                    # prfloat(f' eto rez : {rez}')
                    rez_itog = get_detail_for_lch(set, rez)
                    # prfloat(f'eto rez_itog: {rez_itog}')
                    rezst = get_info_for_floaterrupt_lch(set, rez_itog[0])
                    reznon_st = get_info_for_floaterrupt_lch(set, rez_itog[1])
                    # prfloat(f' eto rez_start : {rezst}')
                    # prfloat(f' eto rez non start : {reznon_st}')
                    itog.append([num_set, rezst, reznon_st])
                i['lch'] = itog
                data_itog.append(i)
                # print(f' eto i after_add lch_data" {i}')
            except Exception as e:
                print(f'эксепшн в 208 строке {e.args}, {e.__context__}')

        data_real_itg = []
        for i in data_itog:
            try:
                # print(f' eto i : {i}')
                # i['1_team_lens_1_set'] = i['lch'][0][1]["lens"]
                i['1_team_max_len_favor_1_set'] =  i['lch'][0][1]["max_len_favor"]
                i['1_team_sum_len_favor_1_set'] =  i['lch'][0][1]["sum_len_favor"]
                i['1_team_otn_len_favor_1_set'] = i['lch'][0][1]["otn_len_favor_set"]
                # print( i['1_team_otn_len_favor_1_set'])

                # i['2_team_lens_1_set'] = i['lch'][0][2]["lens"]
                i['2_team_max_len_favor_1_set'] =  i['lch'][0][2]["max_len_favor"]
                i['2_team_sum_len_favor_1_set'] =  i['lch'][0][2]["sum_len_favor"]
                i['2_team_otn_len_favor_1_set'] = i['lch'][0][2]["otn_len_favor_set"]
                # print(i['2_team_otn_len_favor_1_set'])

                # i['1_team_lens_2_set'] = i['lch'][1][1]["lens"]
                i['1_team_max_len_favor_2_set'] = i['lch'][1][1]["max_len_favor"]
                i['1_team_sum_len_favor_2_set'] = i['lch'][1][1]["sum_len_favor"]
                i['1_team_otn_len_favor_2_set'] = i['lch'][1][1]["otn_len_favor_set"]
                # print(i['1_team_otn_len_favor_2_set'])

                # i['2_team_lens_2_set'] = i['lch'][1][2]["lens"]
                i['2_team_max_len_favor_2_set'] = i['lch'][1][2]["max_len_favor"]
                i['2_team_sum_len_favor_2_set'] = i['lch'][1][2]["sum_len_favor"]
                i['2_team_otn_len_favor_2_set'] = i['lch'][1][2]["otn_len_favor_set"]
                # print(i['2_team_otn_len_favor_2_set'])
                del i['lch']
                data_real_itg.append(i)
            except Exception as e:
                print(f'эксепшн в 265 строке {e.args}, {e.__context__}')


        with open('AFT_PARS_data_3_process_len_lch.json', 'w') as f:
            f.write(json.dumps(data_real_itg))
        print('окончена часть 3')

        print('это часть 4')


        with open("AFT_PARS_data_3_process_len_lch.json") as f:
            data= json.load(f)
        err = []
        for i in data:
            try:
                # prfloat(f' eto i " {i}')
                set_1= i['set1']
                set_2 = i['set2']
                # prfloat(f' eto data : {data}')
                # prfloat(f' eto data: {data}')
                set_1= del_zero_in_set(set_1)
                set_2= del_zero_in_set(set_2)
                # prfloat(f'eto data after : {data}')
                #
                start_set_1 = get_non_stop_goal_first_team(set_1)
                non_start_set_1 = get_non_stop_goal_sec_team(set_1)
                start_set_2 =  get_non_stop_goal_first_team(set_2)
                non_start_set_2 = get_non_stop_goal_sec_team(set_2)
                """ 1 сет для 1 команды"""
                i['first_t_max_scor_no_lch_1_set'] = start_set_1['first_t_max_scor_no_lch']
                i['first_t_max_scor_with_lch_1_set'] = start_set_1['first_t_max_scor_with_lch']
                i['first_t_max_len_non_stop_goal_no_lch_1_set'] = start_set_1['first_t_max_len_non_stop_goal_no_lch']
                i['first_t_max_len_non_st_goal_with_l_ch_1_set'] = start_set_1['first_t_max_len_non_st_goal_with_l_ch']
                i['first_t_lens_no_l_ch_to_len_set_1_set'] = start_set_1['first_t_lens_no_l_ch_to_len_set']
                i['first_t_lens_with_l_ch_to_len_set_1_set'] = start_set_1['first_t_lens_with_l_ch_to_len_set']
                i['first_t_sum_lens_no_l_ch_to_set_1_set'] = start_set_1['first_t_sum_lens_no_l_ch_to_set']
                i['first_t_sum_lens_with_l_ch_to_set_1_set'] = start_set_1['first_t_sum_lens_with_l_ch_to_set']
                """ 1 сет для 2 команды"""
                i['sec_t_max_scor_no_lch_1_set'] = non_start_set_1['sec_t_max_scor_no_lch']
                i['sec_t_max_scor_with_lch_1_set'] = non_start_set_1['sec_t_max_scor_with_lch']
                i['sec_t_max_len_non_stop_goal_no_lch_1_set'] = non_start_set_1['sec_t_max_len_non_stop_goal_no_lch']
                i['sec_t_max_len_non_st_goal_with_l_ch_1_set'] = non_start_set_1['sec_t_max_len_non_st_goal_with_l_ch']
                i['sec_t_lens_no_l_ch_to_len_set_1_set'] = non_start_set_1['sec_t_lens_no_l_ch_to_len_set']
                i['sec_t_lens_with_l_ch_to_len_set_1_set'] = non_start_set_1['sec_t_lens_with_l_ch_to_len_set']
                i['sec_t_sum_lens_no_l_ch_to_set_1_set'] = non_start_set_1['sec_t_sum_lens_no_l_ch_to_set']
                i['sec_t_sum_lens_with_l_ch_to_set_1_set'] = non_start_set_1['sec_t_sum_lens_with_l_ch_to_set']

                """ 2 сет для 1 команды"""
                i['first_t_max_scor_no_lch_2_set'] = start_set_2['first_t_max_scor_no_lch']
                i['first_t_max_scor_with_lch_2_set'] = start_set_2['first_t_max_scor_with_lch']
                i['first_t_max_len_non_stop_goal_no_lch_2_set'] = start_set_2['first_t_max_len_non_stop_goal_no_lch']
                i['first_t_max_len_non_st_goal_with_l_ch_2_set'] = start_set_2['first_t_max_len_non_st_goal_with_l_ch']
                i['first_t_lens_no_l_ch_to_len_set_2_set'] = start_set_2['first_t_lens_no_l_ch_to_len_set']
                i['first_t_lens_with_l_ch_to_len_set_2_set'] = start_set_2['first_t_lens_with_l_ch_to_len_set']
                i['first_t_sum_lens_no_l_ch_to_set_2_set'] = start_set_2['first_t_sum_lens_no_l_ch_to_set']
                i['first_t_sum_lens_with_l_ch_to_set_2_set'] = start_set_2['first_t_sum_lens_with_l_ch_to_set']
                """ 2 сет для 2 команды"""
                i['sec_t_max_scor_no_lch_2_set'] = non_start_set_2['sec_t_max_scor_no_lch']
                i['sec_t_max_scor_with_lch_2_set'] = non_start_set_2['sec_t_max_scor_with_lch']
                i['sec_t_max_len_non_stop_goal_no_lch_2_set'] = non_start_set_2['sec_t_max_len_non_stop_goal_no_lch']
                i['sec_t_max_len_non_st_goal_with_l_ch_2_set'] = non_start_set_2['sec_t_max_len_non_st_goal_with_l_ch']
                i['sec_t_lens_no_l_ch_to_len_set_2_set'] = non_start_set_2['sec_t_lens_no_l_ch_to_len_set']
                i['sec_t_lens_with_l_ch_to_len_set_2_set'] = non_start_set_2['sec_t_lens_with_l_ch_to_len_set']
                i['sec_t_sum_lens_no_l_ch_to_set_2_set'] = non_start_set_2['sec_t_sum_lens_no_l_ch_to_set']
                i['sec_t_sum_lens_with_l_ch_to_set_2_set'] = non_start_set_2['sec_t_sum_lens_with_l_ch_to_set']

                """ считаю +4 для каждой команды"""
                i['pl_4toset_first_team_1_set'] = pl_two_1_team(set_1)['len_pl_4_to_set_1_team']
                i['pl_4toset_sec_team_1_set'] = pl_two_2_team(set_1)['len_pl_4_to_set_1_team']

                i['pl_4toset_first_team_2_set'] = pl_two_1_team(set_2)['len_pl_4_to_set_1_team']
                i['pl_4toset_sec_team_2_set'] = pl_two_2_team(set_2)['len_pl_4_to_set_1_team']

                i['mode_1_set'] = statistics.mode(set_1)
                i['mode_2_set'] = statistics.mode(set_2)

                i['medi_1_set'] = statistics.median(set_1)
                i['modi_2_set'] = statistics.median(set_2)

                i['std_1_set'] = statistics.stdev(set_1)
                i['std_2_set'] = statistics.stdev(set_2)

            except Exception as e:
                # prfloat('this except {i}')
                err.append(i)


        print(f' eto len oshibki : {len(err)}')



        with open('AFT_PARS_data_4_process_len_non_stop.json', 'w') as f:
            f.write(json.dumps(data))

        df = pd.DataFrame.from_dict(data)
        columns = data[0].keys()


        df.to_csv('lchkf_AFT_PARS.csv')
        print('окончена часть 4')
        return True
    except Exception as e:
        print(e.args)
        return False


while True:
    try:
        flag = True
        print(f'начат новый круг : {datetime.datetime.now()}')
        time.sleep(3)
        print('NEW_LAP')
        """1. STEP 1: """
        print('START STEP 1')
        try:
            with open(r"C:\Users\Пользователь\PycharmProjects\pytFonbet\for_analize_PRIORITET.json", "r", encoding='utf-8') as read_file:
                data = json.load(read_file)

            # with open("for_analize_PRIORITET.json", "r", encoding='utf-8') as read_file:
            #     data = json.load(read_file)
        except Exception as e:
            print(e.args)
            flag = False
        finally:
            if flag:
                data_it = []
                for igra in data:
                    try:
                        if igra["game"] not in data_it:
                            data_it.append(igra["game"])
                            # print(f'eto igra: {igra}')
                            # print(f' time : {datetime.datetime.now()}, here new game : {igra["game"]}')
                    except Exception as e:
                        continue

                make_df = make_itog_df(data_it)
                if make_df:
                    print(f'eto res from make_df: {make_df}')
                    df = pd.read_csv('lchkf_AFT_PARS.csv', low_memory=False)
                    print(df.isnull().values.any(),  df.isnull().any().any())
                    print(f' eto len df : {len(df)}')
                    #Добавляю новые параметры, но предварительно стало хуже
                    ## Добавляю лбщую разницу в счете после 2 сэтов
                    df['dif_scr_aft_2_sets'] = df[['dif_1_set','dif_2_set']].sum(axis=1)
                    ## Добавляю общий счет после 2 сетов
                    df['scr_aft_2_sets'] = df[['1_set_scr_1','2_set_scr_1']].sum(axis=1) - df[['1_set_scr_2','2_set_scr_2']].sum(axis=1)
                    ## Добавляю общую длину после 2 сетов
                    df['scr_aft_2_sets'] = df[['1_set_scr_1','2_set_scr_1']].sum(axis=1) - df[['1_set_scr_2','2_set_scr_2']].sum(axis=1)
                    df['len_game_aft_2_sets'] = df['len_set_1 '] + df['len_set_2']
                    df_plusr = df.copy()
                    X = df.drop(['event_number ', 'urls'], axis = 1)

                    """ставлю перечень параметров из большой модели для всех игр там больше аккураси """
                    # X = df[
                    #
                    #     ['len_set_1 ',
                    #      'len_set_2',
                    #      '2_team_sum_len_favor_2_set',
                    #      'first_t_sum_lens_no_l_ch_to_set_2_set',
                    #      '2_team_otn_len_favor_2_set',
                    #      'first_t_sum_lens_with_l_ch_to_set_2_set',
                    #      'max_2_set',
                    #      'modi_2_set',
                    #      'sec_t_max_scor_with_lch_2_set',
                    #      'first_t_sum_lens_no_l_ch_to_set_1_set',
                    #      '1_team_max_len_favor_2_set',
                    #      'first_t_max_scor_with_lch_2_set',
                    #      'sec_t_lens_no_l_ch_to_len_set_2_set',
                    #      'sec_t_sum_lens_no_l_ch_to_set_2_set',
                    #      'pl_4toset_first_team_1_set',
                    #      'otn_pl_2_set_2_set_1_team',
                    #      'quant_pl_2_1_set_1_team',
                    #      'sec_t_lens_no_l_ch_to_len_set_1_set',
                    #      'adv_2_1_set',
                    #      'otn_pl_2_set_1_set_2_team',
                    #      'mean_99_1_set',
                    #      'otn_pl_2_set_2_set_2_team',
                    #      '1_team_max_len_favor_1_set',
                    #      'dif_2_set',
                    #      'sec_t_lens_with_l_ch_to_len_set_1_set',
                    #      'pl_4toset_first_team_2_set',
                    #      'favor',
                    #      'sec_t_lens_with_l_ch_to_len_set_2_set',
                    #      'sec_t_sum_lens_no_l_ch_to_set_1_set',
                    #      'quant_teas_2_set',
                    #      'quant_teas_1_set',
                    #      'l_ch_1_set',
                    #      'otn_teas_set_1_set',
                    #      '1_team_otn_len_favor_1_set',
                    #      '2_team_max_len_favor_1_set',
                    #      '2_team_otn_len_favor_1_set',
                    #      'sec_t_max_len_non_stop_goal_no_lch_2_set',
                    #      'sec_t_max_len_non_stop_goal_no_lch_1_set',
                    #      '1_team_otn_len_favor_2_set',
                    #      'score_befor_3',
                    #      'first_t_max_scor_no_lch_1_set',
                    #      'sec_t_max_len_non_st_goal_with_l_ch_2_set'
                    #      ]
                    # ]



                    X = df[
                        ['1_set_scr_1',
                         '1_set_scr_2',
                         '1_set_len_set',
                         '2_set_scr_1',
                         '2_set_scr_2',
                         '2_set_len_set',
                         'len_set_1 ',
                         'len_set_2',
                         'win_1_set',
                         'win_2_set',
                         'dif_1_set',
                         'dif_2_set',
                         'adv_1_1_set',
                         'adv_2_1_set',
                         'adv_1_2_set',
                         'adv_2_2_set',
                         'max_1_set',
                         'min_1_set',
                         'max_2_set',
                         'min_2_set',
                         'score_befor_3',
                         'favor',
                         'quant_teas_1_set',
                         'otn_teas_set_1_set',
                         'quant_teas_2_set',
                         'otn_teas_set_2_set',
                         'quant_pl_2_1_set_1_team',
                         'otn_pl_2_set_1_set_1_team',
                         'quant_pl_2_2_set_1_team',
                         'otn_pl_2_set_2_set_1_team',
                         'quant_pl_2_1_set_2_team',
                         'otn_pl_2_set_1_set_2_team',
                         'quant_pl_2_2_set_2_team',
                         'otn_pl_2_set_2_set_2_team',
                         'mean_33_1_set',
                         'mean_66_1_set',
                         'mean_99_1_set',
                         'mean_33_2_set',
                         'mean_66_2_set',
                         'mean_99_2_set',
                         'l_ch_1_set',
                         'l_ch_to_len_1_set',
                         'l_ch_2_set',
                         'l_ch_to_len_2_set',
                         '1_team_max_len_favor_1_set',
                         '1_team_sum_len_favor_1_set',
                         '1_team_otn_len_favor_1_set',
                         '2_team_max_len_favor_1_set',
                         '2_team_sum_len_favor_1_set',
                         '2_team_otn_len_favor_1_set',
                         '1_team_max_len_favor_2_set',
                         '1_team_sum_len_favor_2_set',
                         '1_team_otn_len_favor_2_set',
                         '2_team_max_len_favor_2_set',
                         '2_team_sum_len_favor_2_set',
                         '2_team_otn_len_favor_2_set',
                         'first_t_max_scor_no_lch_1_set',
                         'first_t_max_scor_with_lch_1_set',
                         'first_t_max_len_non_stop_goal_no_lch_1_set',
                         'first_t_max_len_non_st_goal_with_l_ch_1_set',
                         'first_t_lens_no_l_ch_to_len_set_1_set',
                         'first_t_lens_with_l_ch_to_len_set_1_set',
                         'first_t_sum_lens_no_l_ch_to_set_1_set',
                         'first_t_sum_lens_with_l_ch_to_set_1_set',
                         'sec_t_max_scor_no_lch_1_set',
                         'sec_t_max_scor_with_lch_1_set',
                         'sec_t_max_len_non_stop_goal_no_lch_1_set',
                         'sec_t_max_len_non_st_goal_with_l_ch_1_set',
                         'sec_t_lens_no_l_ch_to_len_set_1_set',
                         'sec_t_lens_with_l_ch_to_len_set_1_set',
                         'sec_t_sum_lens_no_l_ch_to_set_1_set',
                         'sec_t_sum_lens_with_l_ch_to_set_1_set',
                         'first_t_max_scor_no_lch_2_set',
                         'first_t_max_scor_with_lch_2_set',
                         'first_t_max_len_non_stop_goal_no_lch_2_set',
                         'first_t_max_len_non_st_goal_with_l_ch_2_set',
                         'first_t_lens_no_l_ch_to_len_set_2_set',
                         'first_t_lens_with_l_ch_to_len_set_2_set',
                         'first_t_sum_lens_no_l_ch_to_set_2_set',
                         'first_t_sum_lens_with_l_ch_to_set_2_set',
                         'sec_t_max_scor_no_lch_2_set',
                         'sec_t_max_scor_with_lch_2_set',
                         'sec_t_max_len_non_stop_goal_no_lch_2_set',
                         'sec_t_max_len_non_st_goal_with_l_ch_2_set',
                         'sec_t_lens_no_l_ch_to_len_set_2_set',
                         'sec_t_lens_with_l_ch_to_len_set_2_set',
                         'sec_t_sum_lens_no_l_ch_to_set_2_set',
                         'sec_t_sum_lens_with_l_ch_to_set_2_set',
                         'pl_4toset_first_team_1_set',
                         'pl_4toset_sec_team_1_set',
                         'pl_4toset_first_team_2_set',
                         'pl_4toset_sec_team_2_set',
                         'mode_1_set',
                         'mode_2_set',
                         'medi_1_set',
                         'modi_2_set',
                         'std_1_set',
                         'std_2_set',
                         'dif_scr_aft_2_sets',
                         'scr_aft_2_sets',
                         'len_game_aft_2_sets']
                    ]

                    X  = X.astype(float)
                    y_pred = loaded_model.predict_proba(X)

                    # print(y_pred)
                    """новый вариант"""
                    df_plusr['prob_1'] = y_pred[:,0]
                    df_plusr['prob_2'] = y_pred[:, 1]
                    result = df_plusr[['teams',  'prob_1', 'prob_2', 'event_number ','urls', 'kf1_3', 'kf2_3']]
                    conditions = [
                    (result['prob_1'] >= result['prob_2']),
                    (result['prob_1'] < result['prob_2'])]
                    # create a list of the values we want to assign for each condition
                    values = [1, 2]
                    # create a new column and use np.select to assign values to it using our lists as arguments
                    result['who_bet'] = np.select(conditions, values)

                    """проверка как определяется победитель"""
                    conditions = [
                        (result['prob_1'] >= 0.5),
                        (result['prob_1'] < 0.5)]
                    # create a list of the values we want to assign for each condition
                    values = [1, 2]
                    # create a new column and use np.select to assign values to it using our lists as arguments
                    result['who_bet_by_prob'] = np.select(conditions, values)

                    conditions = [
                        (result['prob_1'] >= 0.5),
                        (result['prob_1'] < 0.5)]
                    # create a list of the values we want to assign for each condition
                    values = [result['prob_1'], result['prob_2']]
                    # create a new column and use np.select to assign values to it using our lists as arguments
                    result['winner_prob'] = np.select(conditions, values)

                    result = result.loc[result['winner_prob'] >= 0.62]



                    # print(f' eto result: %s' % result.columns)
                    result = result[['teams', 'event_number ',  'who_bet', 'urls', 'winner_prob', 'who_bet_by_prob', 'prob_1', 'prob_2' , 'kf1_3', 'kf2_3']]

                    result = result.to_dict('records')
                    path = r"C:\Users\Пользователь\PycharmProjects\pytFonbet\result_from_voley.json"
                    with open(path, 'w') as f:
                        f.write(json.dumps(result))
                    print(f'TIMe : { datetime.datetime.now()}, ЭТО ДЛИНА result : {len(result)} ' )
            else:
                print(f'NO DATA, TIMe : { datetime.datetime.now()}')

    except Exception as e:
        print(f'eto len data : {len(data)} ,  { datetime.datetime.now()} :  {e.args}')