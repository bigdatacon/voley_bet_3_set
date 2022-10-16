import fidx
import math
from statistics import mean
def return_max_advantage_in_set_new(set):
    mi = float(min(set))
    ma = float(max(set))
    if mi< 0:
        second_max = abs(mi)
        first_min = mi
    else:
        first_min = mi
        second_max = -(mi)
    if ma>0:
        first_max = ma
        second_min = -(ma)
    else:
        first_max = ma
        second_min = abs(ma)
    return {'first_max': first_max, 'first_min': first_min, 'second_max': second_max, 'second_min': second_min}

""" Получение массива из 0:0 ии отношения в длине игры - корректно"""
def short_corr_ver_get_list_of_teas(set, len_set):# на вход 1 строка  - 1 сета
    count = 0
    for i in set:
        if i == 0:
            count+=1
    len_to_set = count/len_set
    return {'quantity_teas': count, 'len_teas_to_set': len_to_set}

""" Получение массива из +2 для 1 команды"""
def pl_two_1_team(set, len_set): # на вход 1 строка  - 1 игра
    count = 0
    for i in set:
        if i >= 2:
            count+=1
    len_to_set = count/len_set
    return {'quantity_pl_2_1_team': count, 'len_pl_2_to_set_1_team': len_to_set}

""" Получение массива из +2 для 1 команды"""
def pl_two_2_team(set, len_set): # на вход 1 строка  - 1 игра
    count = 0
    for i in set:
        if i <= -2:
            count+=1
    len_to_set = count/len_set
    return {'quantity_pl_2_1_team': count, 'len_pl_2_to_set_1_team': len_to_set}

""" среднее преимущество на трети партии, второй трети и 3 трети в очках и в количестве розыгрышей"""
def short_mean_advantage_per_set(set): # на вход 1 строка  - 1 игра
    sub_list = fidx(set)
    newList_33 = sub_list[0.00:0.33]
    newList_66 = sub_list[0.331:0.66]
    newList_99 = sub_list[0.661:0.9999]
    mean_33 = mean(newList_33)
    mean_66 = mean(newList_66)
    mean_99 = mean(newList_99)
    return {'mean_33': mean_33, 'mean_66': mean_66, 'mean_99': mean_99}


def get_list_of_lead_changes(sub_list): # на вход разницы по 1 сету, на выходе массив сет: [flag, index el где был лид ченд] если флаг четный то лидер сменился от первоначального
    list_of_lead_change = []
    flag = 1
    ties_list = []
    for i in range(len(sub_list)):
        if (sub_list[i]==1 and sub_list[i-1]==0 and sub_list[i-2]==-1) or (sub_list[i]==-1 and sub_list[i-1]==0 and sub_list[i-2]==1):
            flag+=1
            list_of_lead_change.append([flag, i])
    if len(list_of_lead_change) > 1:
        if list_of_lead_change[-1][0] % 2 == 0:
            leader_start = False
        else:
            leader_start = True
    elif len(list_of_lead_change) == 1:
        leader_start = False
    else:
        leader_start = True
    if len(list_of_lead_change)==0:
        list_of_lead_change = [[1, 0]]
    list_of_lead_change.append(leader_start)
    # ties_list.append([set, list_of_lead_change])
    ties_list.append(list_of_lead_change)
    return ties_list[0]

def get_lead_changes(sub_list, len_set): # на вход разницы по 1 сету, на выходе массив сет: [flag, index el где был лид ченд] если флаг четный то лидер сменился от первоначального
    count = 0
    for i in range(len(sub_list)):
        if (sub_list[i]==1 and sub_list[i-1]==0 and sub_list[i-2]==-1) or (sub_list[i]==-1 and sub_list[i-1]==0 and sub_list[i-2]==1):
            count+=1
    len_to_set = count / len_set
    return {'quantity_l_ch': count, 'l_ch_to_len_set': len_to_set}

def pred_obr_base(i): # на вход строка из json
    data = i
    set_1 = [float(x) for x in data['set1']]
    set_2 = [float(x) for x in data['set2']]
    # 'kf1_1': '1,78', 'kf2_1': '1,92', 'kf1_2': '1,85', 'kf2_2': '1,85', 'kf1_3': '1,65', 'kf2_3'

    # data['kf1_1'] = float(data['kf1_1'].replace(',', '.'))
    # data['kf2_1'] = float(data['kf2_1'].replace(',', '.'))
    # data['kf1_2'] = float(data['kf1_2'].replace(',', '.'))
    # data['kf2_2'] = float(data['kf2_2'].replace(',', '.'))
    data['kf1_3'] = float(data['kf1_3'].replace(',', '.'))
    data['kf2_3'] = float(data['kf2_3'].replace(',', '.'))

    len_set_1 = data['1_set_len_set']
    len_set_2 = data['2_set_len_set']

    data['set1'] = set_1
    data['set2'] = set_2
    data['len_set_1 '] = len_set_1
    data['len_set_2'] = len_set_2

    """ добавляю простые параметры"""
    win_1_set = float(str(abs(data['game']))[0])
    win_2_set = float(str(abs(data['game']))[1])
    win_3_set = float(str(abs(data['game']))[2])
    dif_1_set = data['1_set_scr_1'] - data['1_set_scr_2']
    dif_2_set = data['2_set_scr_1'] - data['2_set_scr_2']
    adv_1_1_set = dif_1_set
    adv_2_1_set = - dif_1_set
    adv_1_2_set = dif_2_set
    adv_2_2_set = - dif_2_set

    data['win_1_set'] = win_1_set
    data['win_2_set'] = win_2_set
    data['win_3_set'] = win_3_set
    data['dif_1_set'] = dif_1_set
    data['dif_2_set'] = dif_2_set


    data['adv_1_1_set'] = adv_1_1_set
    data['adv_2_1_set'] = adv_2_1_set
    data['adv_1_2_set'] = adv_1_2_set
    data['adv_2_2_set'] = adv_2_2_set


    """ добавляю min/max"""
    max_1_set = max(set_1)
    min_1_set = min(set_1)
    max_2_set = max(set_2)
    min_2_set = min(set_2)

    data['max_1_set'] = max_1_set
    data['min_1_set'] = min_1_set
    data['max_2_set'] = max_2_set
    data['min_2_set'] = min_2_set

    """ Добавляю счет до 3"""
    score_befor_3 = 2 if (win_1_set == win_2_set) else 1
    data['score_befor_3'] = score_befor_3
    """ Добавляю какая команда ведет"""
    favor = win_2_set if (win_1_set == win_2_set) else 1000
    data['favor'] = favor

    """ Добавляю количество ничей и ничей к игре"""
    quant_teas_1_set = short_corr_ver_get_list_of_teas(set_1, len_set_1)["quantity_teas"]
    otn_teas_set_1_set = short_corr_ver_get_list_of_teas(set_1, len_set_1)["len_teas_to_set"]
    quant_teas_2_set = short_corr_ver_get_list_of_teas(set_2, len_set_2)["quantity_teas"]
    otn_teas_set_2_set = short_corr_ver_get_list_of_teas(set_2, len_set_2)["len_teas_to_set"]

    data['quant_teas_1_set'] = quant_teas_1_set
    data['otn_teas_set_1_set'] = otn_teas_set_1_set
    data['quant_teas_2_set'] = quant_teas_2_set
    data['otn_teas_set_2_set'] = otn_teas_set_2_set


    """ Добавляю количество +2 и ничей к игре для 1 команды"""
    quant_pl_2_1_set_1_team = pl_two_1_team(set_1, len_set_1)["quantity_pl_2_1_team"]
    otn_pl_2_set_1_set_1_team = pl_two_1_team(set_1, len_set_1)["len_pl_2_to_set_1_team"]
    quant_pl_2_2_set_1_team = pl_two_1_team(set_2, len_set_2)["quantity_pl_2_1_team"]
    otn_pl_2_set_2_set_1_team = pl_two_1_team(set_2, len_set_2)["len_pl_2_to_set_1_team"]

    data['quant_pl_2_1_set_1_team'] = quant_pl_2_1_set_1_team
    data['otn_pl_2_set_1_set_1_team'] = otn_pl_2_set_1_set_1_team
    data['quant_pl_2_2_set_1_team'] = quant_pl_2_2_set_1_team
    data['otn_pl_2_set_2_set_1_team'] = otn_pl_2_set_2_set_1_team
    """ Добавляю количество +2 и ничей к игре для 2 команды"""
    quant_pl_2_1_set_2_team = pl_two_2_team(set_1, len_set_1)["quantity_pl_2_1_team"]
    otn_pl_2_set_1_set_2_team = pl_two_2_team(set_1, len_set_1)["len_pl_2_to_set_1_team"]
    quant_pl_2_2_set_2_team = pl_two_2_team(set_2, len_set_2)["quantity_pl_2_1_team"]
    otn_pl_2_set_2_set_2_team = pl_two_2_team(set_2, len_set_2)["len_pl_2_to_set_1_team"]

    data['quant_pl_2_1_set_2_team'] = quant_pl_2_1_set_2_team
    data['otn_pl_2_set_1_set_2_team'] = otn_pl_2_set_1_set_2_team
    data['quant_pl_2_2_set_2_team'] = quant_pl_2_2_set_2_team
    data['otn_pl_2_set_2_set_2_team'] = otn_pl_2_set_2_set_2_team
    """ Добавляю средний счет на 33/66/99"""
    mean_33_1_set = short_mean_advantage_per_set(set_1)["mean_33"]
    mean_66_1_set = short_mean_advantage_per_set(set_1)["mean_66"]
    mean_99_1_set = short_mean_advantage_per_set(set_1)["mean_99"]
    data['mean_33_1_set'] = mean_33_1_set
    data['mean_66_1_set'] = mean_66_1_set
    data['mean_99_1_set'] = mean_99_1_set

    mean_33_2_set = short_mean_advantage_per_set(set_2)["mean_33"]
    mean_66_2_set = short_mean_advantage_per_set(set_2)["mean_66"]
    mean_99_2_set = short_mean_advantage_per_set(set_2)["mean_99"]
    data['mean_33_2_set'] = mean_33_2_set
    data['mean_66_2_set'] = mean_66_2_set
    data['mean_99_2_set'] = mean_99_2_set

    """добавляю количество лид ченджей """
    l_ch_1_set = get_lead_changes(set_1, len_set_1)['quantity_l_ch']
    l_ch_to_len_1_set = get_lead_changes(set_1, len_set_1)['l_ch_to_len_set']
    data['l_ch_1_set'] =   l_ch_1_set
    data['l_ch_to_len_1_set'] = l_ch_to_len_1_set

    l_ch_2_set = get_lead_changes(set_2, len_set_2)['quantity_l_ch']
    l_ch_to_len_2_set = get_lead_changes(set_2, len_set_2)['l_ch_to_len_set']
    data['l_ch_2_set'] =   l_ch_2_set
    data['l_ch_to_len_2_set'] = l_ch_to_len_2_set
    return data



def pred_obr_base_aft_pars(i): # на вход строка из json - функция отличается от базовой только тем что коэффицианты не replace так как float. остальное тоже самое
    data = i
    set_1 = [float(x) for x in data['set1']]
    set_2 = [float(x) for x in data['set2']]
    # 'kf1_1': '1,78', 'kf2_1': '1,92', 'kf1_2': '1,85', 'kf2_2': '1,85', 'kf1_3': '1,65', 'kf2_3'

    # data['kf1_1'] = float(data['kf1_1'].replace(',', '.'))
    # data['kf2_1'] = float(data['kf2_1'].replace(',', '.'))
    # data['kf1_2'] = float(data['kf1_2'].replace(',', '.'))
    # data['kf2_2'] = float(data['kf2_2'].replace(',', '.'))
    # data['kf1_3'] = float(data['kf1_3'].replace(',', '.'))
    # data['kf2_3'] = float(data['kf2_3'].replace(',', '.'))

    len_set_1 = data['1_set_len_set']
    len_set_2 = data['2_set_len_set']

    data['set1'] = set_1
    data['set2'] = set_2
    data['len_set_1 '] = len_set_1
    data['len_set_2'] = len_set_2

    """ добавляю простые параметры"""
    win_1_set = float(str(abs(data['game']))[0])
    win_2_set = float(str(abs(data['game']))[1])
    win_3_set = float(str(abs(data['game']))[2])
    dif_1_set = data['1_set_scr_1'] - data['1_set_scr_2']
    dif_2_set = data['2_set_scr_1'] - data['2_set_scr_2']
    adv_1_1_set = dif_1_set
    adv_2_1_set = - dif_1_set
    adv_1_2_set = dif_2_set
    adv_2_2_set = - dif_2_set

    data['win_1_set'] = win_1_set
    data['win_2_set'] = win_2_set
    data['win_3_set'] = win_3_set
    data['dif_1_set'] = dif_1_set
    data['dif_2_set'] = dif_2_set


    data['adv_1_1_set'] = adv_1_1_set
    data['adv_2_1_set'] = adv_2_1_set
    data['adv_1_2_set'] = adv_1_2_set
    data['adv_2_2_set'] = adv_2_2_set


    """ добавляю min/max"""
    max_1_set = max(set_1)
    min_1_set = min(set_1)
    max_2_set = max(set_2)
    min_2_set = min(set_2)

    data['max_1_set'] = max_1_set
    data['min_1_set'] = min_1_set
    data['max_2_set'] = max_2_set
    data['min_2_set'] = min_2_set

    """ Добавляю счет до 3"""
    score_befor_3 = 2 if (win_1_set == win_2_set) else 1
    data['score_befor_3'] = score_befor_3
    """ Добавляю какая команда ведет"""
    favor = win_2_set if (win_1_set == win_2_set) else 1000
    data['favor'] = favor

    """ Добавляю количество ничей и ничей к игре"""
    quant_teas_1_set = short_corr_ver_get_list_of_teas(set_1, len_set_1)["quantity_teas"]
    otn_teas_set_1_set = short_corr_ver_get_list_of_teas(set_1, len_set_1)["len_teas_to_set"]
    quant_teas_2_set = short_corr_ver_get_list_of_teas(set_2, len_set_2)["quantity_teas"]
    otn_teas_set_2_set = short_corr_ver_get_list_of_teas(set_2, len_set_2)["len_teas_to_set"]

    data['quant_teas_1_set'] = quant_teas_1_set
    data['otn_teas_set_1_set'] = otn_teas_set_1_set
    data['quant_teas_2_set'] = quant_teas_2_set
    data['otn_teas_set_2_set'] = otn_teas_set_2_set


    """ Добавляю количество +2 и ничей к игре для 1 команды"""
    quant_pl_2_1_set_1_team = pl_two_1_team(set_1, len_set_1)["quantity_pl_2_1_team"]
    otn_pl_2_set_1_set_1_team = pl_two_1_team(set_1, len_set_1)["len_pl_2_to_set_1_team"]
    quant_pl_2_2_set_1_team = pl_two_1_team(set_2, len_set_2)["quantity_pl_2_1_team"]
    otn_pl_2_set_2_set_1_team = pl_two_1_team(set_2, len_set_2)["len_pl_2_to_set_1_team"]

    data['quant_pl_2_1_set_1_team'] = quant_pl_2_1_set_1_team
    data['otn_pl_2_set_1_set_1_team'] = otn_pl_2_set_1_set_1_team
    data['quant_pl_2_2_set_1_team'] = quant_pl_2_2_set_1_team
    data['otn_pl_2_set_2_set_1_team'] = otn_pl_2_set_2_set_1_team
    """ Добавляю количество +2 и ничей к игре для 2 команды"""
    quant_pl_2_1_set_2_team = pl_two_2_team(set_1, len_set_1)["quantity_pl_2_1_team"]
    otn_pl_2_set_1_set_2_team = pl_two_2_team(set_1, len_set_1)["len_pl_2_to_set_1_team"]
    quant_pl_2_2_set_2_team = pl_two_2_team(set_2, len_set_2)["quantity_pl_2_1_team"]
    otn_pl_2_set_2_set_2_team = pl_two_2_team(set_2, len_set_2)["len_pl_2_to_set_1_team"]

    data['quant_pl_2_1_set_2_team'] = quant_pl_2_1_set_2_team
    data['otn_pl_2_set_1_set_2_team'] = otn_pl_2_set_1_set_2_team
    data['quant_pl_2_2_set_2_team'] = quant_pl_2_2_set_2_team
    data['otn_pl_2_set_2_set_2_team'] = otn_pl_2_set_2_set_2_team
    """ Добавляю средний счет на 33/66/99"""
    mean_33_1_set = short_mean_advantage_per_set(set_1)["mean_33"]
    mean_66_1_set = short_mean_advantage_per_set(set_1)["mean_66"]
    mean_99_1_set = short_mean_advantage_per_set(set_1)["mean_99"]
    data['mean_33_1_set'] = mean_33_1_set
    data['mean_66_1_set'] = mean_66_1_set
    data['mean_99_1_set'] = mean_99_1_set

    mean_33_2_set = short_mean_advantage_per_set(set_2)["mean_33"]
    mean_66_2_set = short_mean_advantage_per_set(set_2)["mean_66"]
    mean_99_2_set = short_mean_advantage_per_set(set_2)["mean_99"]
    data['mean_33_2_set'] = mean_33_2_set
    data['mean_66_2_set'] = mean_66_2_set
    data['mean_99_2_set'] = mean_99_2_set

    """добавляю количество лид ченджей """
    l_ch_1_set = get_lead_changes(set_1, len_set_1)['quantity_l_ch']
    l_ch_to_len_1_set = get_lead_changes(set_1, len_set_1)['l_ch_to_len_set']
    data['l_ch_1_set'] =   l_ch_1_set
    data['l_ch_to_len_1_set'] = l_ch_to_len_1_set

    l_ch_2_set = get_lead_changes(set_2, len_set_2)['quantity_l_ch']
    l_ch_to_len_2_set = get_lead_changes(set_2, len_set_2)['l_ch_to_len_set']
    data['l_ch_2_set'] =   l_ch_2_set
    data['l_ch_to_len_2_set'] = l_ch_to_len_2_set
    return data