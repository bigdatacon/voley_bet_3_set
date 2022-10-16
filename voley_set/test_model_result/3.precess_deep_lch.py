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
from func_0_pred_obr import *
from func_3_for_deep_lch import *

with open("data_2_obr_base.json") as f:
    data= json.load(f)

data = data[:]
itog =  []
new_data = []
for i in data:
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
        rez_itog = get_detail_for_lch(set, rez)
        rezst = get_info_for_floaterrupt_lch(set, rez_itog[0])
        reznon_st = get_info_for_floaterrupt_lch(set, rez_itog[1])
        itog.append([num_set, rezst, reznon_st])
    i['lch'] = itog
    new_data.append(i)

for i in new_data:
    # i['1_team_lens_1_set'] = i['lch'][0][1]["lens"]
    i['1_team_max_len_favor_1_set'] =  i['lch'][0][1]["max_len_favor"]
    i['1_team_sum_len_favor_1_set'] =  i['lch'][0][1]["sum_len_favor"]
    i['1_team_otn_len_favor_1_set'] = i['lch'][0][1]["otn_len_favor_set"]
    # prfloat( i['1_team_otn_len_favor_1_set'])

    # i['2_team_lens_1_set'] = i['lch'][0][2]["lens"]
    i['2_team_max_len_favor_1_set'] =  i['lch'][0][2]["max_len_favor"]
    i['2_team_sum_len_favor_1_set'] =  i['lch'][0][2]["sum_len_favor"]
    i['2_team_otn_len_favor_1_set'] = i['lch'][0][2]["otn_len_favor_set"]
    # prfloat(i['2_team_otn_len_favor_1_set'])

    # i['1_team_lens_2_set'] = i['lch'][1][1]["lens"]
    i['1_team_max_len_favor_2_set'] = i['lch'][1][1]["max_len_favor"]
    i['1_team_sum_len_favor_2_set'] = i['lch'][1][1]["sum_len_favor"]
    i['1_team_otn_len_favor_2_set'] = i['lch'][1][1]["otn_len_favor_set"]
    # prfloat(i['1_team_otn_len_favor_2_set'])

    # i['2_team_lens_2_set'] = i['lch'][1][2]["lens"]
    i['2_team_max_len_favor_2_set'] = i['lch'][1][2]["max_len_favor"]
    i['2_team_sum_len_favor_2_set'] = i['lch'][1][2]["sum_len_favor"]
    i['2_team_otn_len_favor_2_set'] = i['lch'][1][2]["otn_len_favor_set"]
    # prfloat(i['2_team_otn_len_favor_2_set'])
    del i['lch']

# for i in new_data:
#     print(f' eto i itog : {i}')

with open('data_3_process_len_lch.json', 'w') as f:
    f.write(json.dumps(new_data))


print(f'end, eto len data : {len(new_data)}')
print(new_data[0])
print(new_data[0].keys())


base_columns = ['teams', 'source', 'sex', 'set1', 'set2', 'set3', 'game', 'kf1_3', 'kf2_3', '1_set_scr_1', '1_set_scr_2',
                '1_set_len_set', '1_set_FLAG_LEN_SCR', '2_set_scr_1', '2_set_scr_2', '2_set_len_set', '2_set_FLAG_LEN_SCR',
                'len_set_1 ', 'len_set_2', 'win_1_set', 'win_2_set', 'win_3_set', 'dif_1_set', 'dif_2_set', 'adv_1_1_set',
                'adv_2_1_set', 'adv_1_2_set', 'adv_2_2_set', 'max_1_set', 'min_1_set', 'max_2_set', 'min_2_set', 'score_befor_3',
                'favor', 'quant_teas_1_set', 'otn_teas_set_1_set', 'quant_teas_2_set', 'otn_teas_set_2_set', 'quant_pl_2_1_set_1_team',
                'otn_pl_2_set_1_set_1_team', 'quant_pl_2_2_set_1_team', 'otn_pl_2_set_2_set_1_team', 'quant_pl_2_1_set_2_team',
                'otn_pl_2_set_1_set_2_team', 'quant_pl_2_2_set_2_team', 'otn_pl_2_set_2_set_2_team', 'mean_33_1_set', 'mean_66_1_set',
                'mean_99_1_set', 'mean_33_2_set', 'mean_66_2_set', 'mean_99_2_set', 'l_ch_1_set', 'l_ch_to_len_1_set',
                'l_ch_2_set', 'l_ch_to_len_2_set', '1_team_max_len_favor_1_set', '1_team_sum_len_favor_1_set',
                '1_team_otn_len_favor_1_set', '2_team_max_len_favor_1_set', '2_team_sum_len_favor_1_set',
                '2_team_otn_len_favor_1_set', '1_team_max_len_favor_2_set', '1_team_sum_len_favor_2_set',
                '1_team_otn_len_favor_2_set', '2_team_max_len_favor_2_set', '2_team_sum_len_favor_2_set', '2_team_otn_len_favor_2_set']