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
from func_for_kf import *
from func_0_pred_obr_aft_pars import *
from func_3_for_deep_lch import *
import statistics

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

for i in data:
    print(f' eto i itog : {i}')
print(f' eto len oshibki : {len(err)}')
for i in err:
    print(f' eto i: {i}')


with open('AFT_PARS_data_4_process_len_non_stop.json', 'w') as f:
    f.write(json.dumps(data))

df = pd.DataFrame.from_dict(data)
columns = data[0].keys()
print(columns)

df.to_csv('lchkf_AFT_PARS.csv')
print('end')

base_columns = ['teams', 'source', 'sex', 'set1', 'set2', 'set3', 'game', 'kf1_3', 'kf2_3', '1_set_scr_1', '1_set_scr_2', '1_set_len_set', '1_set_FLAG_LEN_SCR', '2_set_scr_1', '2_set_scr_2', '2_set_len_set', '2_set_FLAG_LEN_SCR', 'len_set_1 ', 'len_set_2', 'win_1_set', 'win_2_set', 'win_3_set', 'dif_1_set', 'dif_2_set', 'adv_1_1_set', 'adv_2_1_set', 'adv_1_2_set', 'adv_2_2_set', 'max_1_set', 'min_1_set', 'max_2_set', 'min_2_set', 'score_befor_3', 'favor', 'quant_teas_1_set', 'otn_teas_set_1_set', 'quant_teas_2_set', 'otn_teas_set_2_set', 'quant_pl_2_1_set_1_team', 'otn_pl_2_set_1_set_1_team', 'quant_pl_2_2_set_1_team', 'otn_pl_2_set_2_set_1_team', 'quant_pl_2_1_set_2_team', 'otn_pl_2_set_1_set_2_team', 'quant_pl_2_2_set_2_team', 'otn_pl_2_set_2_set_2_team', 'mean_33_1_set', 'mean_66_1_set', 'mean_99_1_set', 'mean_33_2_set', 'mean_66_2_set', 'mean_99_2_set', 'l_ch_1_set', 'l_ch_to_len_1_set', 'l_ch_2_set', 'l_ch_to_len_2_set', '1_team_max_len_favor_1_set', '1_team_sum_len_favor_1_set', '1_team_otn_len_favor_1_set', '2_team_max_len_favor_1_set', '2_team_sum_len_favor_1_set', '2_team_otn_len_favor_1_set', '1_team_max_len_favor_2_set', '1_team_sum_len_favor_2_set', '1_team_otn_len_favor_2_set', '2_team_max_len_favor_2_set', '2_team_sum_len_favor_2_set', '2_team_otn_len_favor_2_set', 'first_t_max_scor_no_lch_1_set', 'first_t_max_scor_with_lch_1_set', 'first_t_max_len_non_stop_goal_no_lch_1_set', 'first_t_max_len_non_st_goal_with_l_ch_1_set', 'first_t_lens_no_l_ch_to_len_set_1_set', 'first_t_lens_with_l_ch_to_len_set_1_set', 'first_t_sum_lens_no_l_ch_to_set_1_set', 'first_t_sum_lens_with_l_ch_to_set_1_set', 'sec_t_max_scor_no_lch_1_set', 'sec_t_max_scor_with_lch_1_set', 'sec_t_max_len_non_stop_goal_no_lch_1_set', 'sec_t_max_len_non_st_goal_with_l_ch_1_set', 'sec_t_lens_no_l_ch_to_len_set_1_set', 'sec_t_lens_with_l_ch_to_len_set_1_set', 'sec_t_sum_lens_no_l_ch_to_set_1_set', 'sec_t_sum_lens_with_l_ch_to_set_1_set', 'first_t_max_scor_no_lch_2_set', 'first_t_max_scor_with_lch_2_set', 'first_t_max_len_non_stop_goal_no_lch_2_set', 'first_t_max_len_non_st_goal_with_l_ch_2_set', 'first_t_lens_no_l_ch_to_len_set_2_set', 'first_t_lens_with_l_ch_to_len_set_2_set', 'first_t_sum_lens_no_l_ch_to_set_2_set', 'first_t_sum_lens_with_l_ch_to_set_2_set', 'sec_t_max_scor_no_lch_2_set', 'sec_t_max_scor_with_lch_2_set', 'sec_t_max_len_non_stop_goal_no_lch_2_set', 'sec_t_max_len_non_st_goal_with_l_ch_2_set', 'sec_t_lens_no_l_ch_to_len_set_2_set', 'sec_t_lens_with_l_ch_to_len_set_2_set', 'sec_t_sum_lens_no_l_ch_to_set_2_set', 'sec_t_sum_lens_with_l_ch_to_set_2_set', 'pl_4toset_first_team_1_set', 'pl_4toset_sec_team_1_set', 'pl_4toset_first_team_2_set', 'pl_4toset_sec_team_2_set', 'mode_1_set', 'mode_2_set', 'medi_1_set', 'modi_2_set', 'std_1_set', 'std_2_set']



non_base_columns = ['teams', 'source', 'sex', 'set1', 'set2', 'set3', 'game', 'kf1_3', 'kf2_3', '1_set_scr_1', '1_set_scr_2',
                    '1_set_len_set', '1_set_FLAG_LEN_SCR', '2_set_scr_1', '2_set_scr_2', '2_set_len_set',
                    '2_set_FLAG_LEN_SCR', 'len_set_1 ', 'len_set_2', 'win_1_set', 'win_2_set', 'win_3_set',
                    'dif_1_set', 'dif_2_set', 'adv_1_1_set', 'adv_2_1_set', 'adv_1_2_set', 'adv_2_2_set', 'max_1_set',
                    'min_1_set', 'max_2_set', 'min_2_set', 'score_befor_3', 'favor', 'quant_teas_1_set', 'otn_teas_set_1_set',
                    'quant_teas_2_set', 'otn_teas_set_2_set', 'quant_pl_2_1_set_1_team', 'otn_pl_2_set_1_set_1_team',
                    'quant_pl_2_2_set_1_team', 'otn_pl_2_set_2_set_1_team', 'quant_pl_2_1_set_2_team', 'otn_pl_2_set_1_set_2_team',
                    'quant_pl_2_2_set_2_team', 'otn_pl_2_set_2_set_2_team', 'mean_33_1_set', 'mean_66_1_set',
                    'mean_99_1_set', 'mean_33_2_set', 'mean_66_2_set', 'mean_99_2_set', 'l_ch_1_set', 'l_ch_to_len_1_set',
                    'l_ch_2_set', 'l_ch_to_len_2_set', '1_team_max_len_favor_1_set', '1_team_sum_len_favor_1_set',
                    '1_team_otn_len_favor_1_set', '2_team_max_len_favor_1_set', '2_team_sum_len_favor_1_set',
                    '2_team_otn_len_favor_1_set', '1_team_max_len_favor_2_set', '1_team_sum_len_favor_2_set',
                    '1_team_otn_len_favor_2_set', '2_team_max_len_favor_2_set', '2_team_sum_len_favor_2_set',
                    '2_team_otn_len_favor_2_set', 'first_t_max_scor_no_lch_1_set', 'first_t_max_scor_with_lch_1_set',
                    'first_t_max_len_non_stop_goal_no_lch_1_set', 'first_t_max_len_non_st_goal_with_l_ch_1_set',
                    'first_t_lens_no_l_ch_to_len_set_1_set', 'first_t_lens_with_l_ch_to_len_set_1_set',
                    'first_t_sum_lens_no_l_ch_to_set_1_set', 'first_t_sum_lens_with_l_ch_to_set_1_set',
                    'sec_t_max_scor_no_lch_1_set', 'sec_t_max_scor_with_lch_1_set', 'sec_t_max_len_non_stop_goal_no_lch_1_set',
                    'sec_t_max_len_non_st_goal_with_l_ch_1_set', 'sec_t_lens_no_l_ch_to_len_set_1_set',
                    'sec_t_lens_with_l_ch_to_len_set_1_set', 'sec_t_sum_lens_no_l_ch_to_set_1_set',
                    'sec_t_sum_lens_with_l_ch_to_set_1_set', 'first_t_max_scor_no_lch_2_set', 'first_t_max_scor_with_lch_2_set',
                    'first_t_max_len_non_stop_goal_no_lch_2_set', 'first_t_max_len_non_st_goal_with_l_ch_2_set',
                    'first_t_lens_no_l_ch_to_len_set_2_set', 'first_t_lens_with_l_ch_to_len_set_2_set',
                    'first_t_sum_lens_no_l_ch_to_set_2_set', 'first_t_sum_lens_with_l_ch_to_set_2_set',
                    'sec_t_max_scor_no_lch_2_set', 'sec_t_max_scor_with_lch_2_set', 'sec_t_max_len_non_stop_goal_no_lch_2_set',
                    'sec_t_max_len_non_st_goal_with_l_ch_2_set', 'sec_t_lens_no_l_ch_to_len_set_2_set',
                    'sec_t_lens_with_l_ch_to_len_set_2_set', 'sec_t_sum_lens_no_l_ch_to_set_2_set',
                    'sec_t_sum_lens_with_l_ch_to_set_2_set', 'pl_4toset_first_team_1_set', 'pl_4toset_sec_team_1_set',
                    'pl_4toset_first_team_2_set', 'pl_4toset_sec_team_2_set', 'mode_1_set', 'mode_2_set', 'medi_1_set',
                    'modi_2_set', 'std_1_set', 'std_2_set']

print(base_columns==non_base_columns)