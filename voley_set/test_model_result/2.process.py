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

with open("data_pred_obr.json") as f:
    data = json.load(f)


# data = '1,78'
# prfloat(float(data.replace(',', '.')))

itog = []
for i in data:
    i = pred_obr_base(i)
    itog.append(i)

print(f' eto len itog : {len(itog)}, eto len data : {len(data)}')
with open('data_2_obr_base.json', 'w') as f:
    f.write(json.dumps(itog))

# for i in itog:
#     print(f' eto itog : {i}')

df = pd.DataFrame.from_dict(itog)
print(df.columns)
df.to_csv('withkf.csv')

# data = data[0]
# set_1 = [float(x) for x in data['set1']]
# set_2 = [float(x) for x in data['set2']]
# len_set_1 = data['1_set_len_set']
# len_set_2 = data['2_set_len_set']
# """ добавляю простые параметры"""
# win_1_set =  float(str(abs(data['game']))[0])
# win_2_set = float(str(abs(data['game']))[1])
# win_3_set = float(str(abs(data['game']))[2])
# dif_1_set = data['1_set_scr_1'] - data['1_set_scr_2']
# dif_2_set = data['2_set_scr_1'] - data['2_set_scr_2']
#
# adv_1_1_set = dif_1_set
# adv_2_1_set = - dif_1_set
# adv_1_2_set = dif_2_set
# adv_2_2_set = - dif_2_set
#
# """ добавляю min/max"""
# max_1_set = max(set_1)
# min_1_set = min(set_1)
# max_2_set = max(set_2)
# min_2_set = min(set_2)
#
# """ Добавляю счет до 3"""
# score_befor_3 = 2 if (win_1_set==win_2_set) else 1
#
# """ Добавляю какая команда ведет"""
# favor = win_2_set if (win_1_set==win_2_set) else 1000
#
# """ Добавляю количество ничей и ничей к игре"""
# quant_teas_1_set = short_corr_ver_get_list_of_teas(set_1, len_set_1)["quantity_teas"]
# otn_teas_set_1_set = short_corr_ver_get_list_of_teas(set_1, len_set_1)["len_teas_to_set"]
# quant_teas_2_set = short_corr_ver_get_list_of_teas(set_2, len_set_2)["quantity_teas"]
# otn_teas_set_2_set = short_corr_ver_get_list_of_teas(set_2, len_set_2)["len_teas_to_set"]
# """ Добавляю количество +2 и ничей к игре для 1 команды"""
# quant_pl_2_1_set_1_team = pl_two_1_team(set_1, len_set_1)["quantity_pl_2_1_team"]
# otn_pl_2_set_1_set_1_team = pl_two_1_team(set_1, len_set_1)["len_pl_2_to_set_1_team"]
# quant_pl_2_2_set_1_team = pl_two_1_team(set_2, len_set_2)["quantity_pl_2_1_team"]
# otn_pl_2_set_2_set_1_team = pl_two_1_team(set_2, len_set_2)["len_pl_2_to_set_1_team"]
# """ Добавляю количество +2 и ничей к игре для 2 команды"""
# quant_pl_2_1_set_2_team = pl_two_2_team(set_1, len_set_1)["quantity_pl_2_1_team"]
# otn_pl_2_set_1_set_2_team = pl_two_2_team(set_1, len_set_1)["len_pl_2_to_set_1_team"]
# quant_pl_2_2_set_2_team = pl_two_2_team(set_2, len_set_2)["quantity_pl_2_1_team"]
# otn_pl_2_set_2_set_2_team = pl_two_2_team(set_2, len_set_2)["len_pl_2_to_set_1_team"]
# """ Добавляю средний счет на 33/66/99"""
# mean_33_1_set = short_mean_advantage_per_set(set_1)["mean_33"]
# mean_66_1_set = short_mean_advantage_per_set(set_1)["mean_66"]
# mean_99_1_set = short_mean_advantage_per_set(set_1)["mean_99"]
#
# mean_33_2_set = short_mean_advantage_per_set(set_2)["mean_33"]
# mean_66_2_set = short_mean_advantage_per_set(set_2)["mean_66"]
# mean_99_2_set = short_mean_advantage_per_set(set_2)["mean_99"]
#
# """добавляю количество лид ченджей """
# l_ch_1_set = get_lead_changes(set_1, len_set_1)['quantity_l_ch']
# l_ch_to_len_1_set = get_lead_changes(set_1, len_set_1)['l_ch_to_len_set']
# l_ch_2_set = get_lead_changes(set_2, len_set_2)['quantity_l_ch']
# l_ch_to_len_2_set = get_lead_changes(set_2, len_set_2)['l_ch_to_len_set']
#
# """ПЕЧАТЬ"""
# prfloat(f' eto data : {data}')
# prfloat(f' eto set_1 : {set_1}')
# prfloat(f' eto set_2  : {set_2}')
# prfloat(f' eto len_set_1 : {len_set_1}')
# prfloat(f' eto len_set_2 : {len_set_2}')
# prfloat(f' eto win_1_set : {win_1_set}')
# prfloat(f' eto win_2_set : {win_2_set}')
# prfloat(f' eto win_3_set : {win_3_set}')
# prfloat(f' eto dif_1_set : {dif_1_set}')
# prfloat(f' eto dif_2_set : {dif_2_set}')
# """ распечатываю макс/мин """
# prfloat(f' max_1_set : {max_1_set}')
# prfloat(f' min_1_set : {min_1_set}')
# prfloat(f' eto max_2_set : {max_2_set}')
# prfloat(f' eto min_2_set : {min_2_set}')
#
# """ распечатываю преимущества """
# prfloat(f' adv_1_1_set  : {adv_1_1_set }')
# prfloat(f' adv_2_1_set : {adv_2_1_set}')
# prfloat(f' eto adv_1_2_set  : {adv_1_2_set }')
# prfloat(f' eto adv_2_2_set : {adv_2_2_set}')
#
# """ распечатываю кто ведет и с каким счетом """
# prfloat(f' score_befor_3  : {score_befor_3 }')
# prfloat(f' favor : {favor}')
#
# """распечатываю ничьи и ничьи к игре"""
# prfloat(f' quant_teas_1_set  : {quant_teas_1_set }')
# prfloat(f' otn_teas_set_1_set: {otn_teas_set_1_set}')
# prfloat(f' quant_teas_2_set  : {quant_teas_2_set }')
# prfloat(f' otn_teas_set_2_set: {otn_teas_set_2_set}')
#
# """ Распечатываю +2 для 1 и 2 команды"""
# prfloat(f' quant_pl_2_1_set_1_team : {quant_pl_2_1_set_1_team }')
# prfloat(f' otn_pl_2_set_1_set_1_team : {otn_pl_2_set_1_set_1_team }')
# prfloat(f' quant_pl_2_2_set_1_team  : {quant_pl_2_2_set_1_team}')
# prfloat(f' otn_pl_2_set_2_set_1_team: {otn_pl_2_set_2_set_1_team}')
#
# prfloat(f' quant_pl_2_1_set_2_team : {quant_pl_2_1_set_2_team }')
# prfloat(f' otn_pl_2_set_1_set_2_team : {otn_pl_2_set_1_set_2_team }')
# prfloat(f' quant_pl_2_2_set_2_team  : {quant_pl_2_2_set_2_team}')
# prfloat(f' otn_pl_2_set_2_set_2_team: {otn_pl_2_set_2_set_2_team}')
#
# """ Распечатываю преимущества 33/66/99"""
# prfloat(f' mean_33_1_set : {mean_33_1_set}')
# prfloat(f' mean_66_1_set : {mean_66_1_set }')
# prfloat(f' mean_99_1_set : {mean_99_1_set}')
# prfloat(f' mean_33_2_set : {mean_33_2_set}')
# prfloat(f' mean_66_2_set : {mean_66_2_set }')
# prfloat(f' mean_99_2_set : {mean_99_2_set}')
#
# """ Распечатываю количество лид ченджей"""
# prfloat(f' l_ch_1_set : {l_ch_1_set }')
# prfloat(f' l_ch_to_len_1_set : {l_ch_to_len_1_set}')
# prfloat(f' l_ch_2_set : {l_ch_2_set }')
# prfloat(f' l_ch_to_len_2_set : {l_ch_to_len_2_set}')

