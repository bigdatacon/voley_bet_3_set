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
from func_for_kf_aft_pars import *
from func_0_pred_obr_aft_pars import *

with open("AFT_PARS_data_pred_obr.json") as f:
    data = json.load(f)

itog = []
for i in data:
    i = pred_obr_base_aft_pars(i)
    itog.append(i)

print(f' eto len itog : {len(itog)}, eto len data : {len(data)}')
with open('AFT_PARS_data_2_obr_base.json', 'w') as f:
    f.write(json.dumps(itog))


for i in itog:
    print(f' eto itog : {i}')

df = pd.DataFrame.from_dict(itog)
print(df.columns)
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

for i in base_columns:
    if i not in non_base:
        print(f' etogo net: {i}')

print(base_columns==non_base)