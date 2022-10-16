import fidx
import math
from statistics import mean
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
        leader_start = True
    list_of_lead_change.append(leader_start)
    favor = sub_list[0] if sub_list[0]!=0 else sub_list[1]
    favor = 'first' if favor>0 else 'second'
    list_of_lead_change.append(favor)
    return list_of_lead_change


def who_sow(set):
    if set[0]!= None:
        if type(set[0])==list:
            sign = 'first' if mean(set[0]) > 0 else 'second'
        else:
            sign = 'first' if set[0] > 0 else 'second'
    else:
        sign = None
    return sign


def get_detail_for_lch(data, rez):
    if len(rez)==3:
        if rez[0] == [1, 0]:
            start = data
            non_start = [None]
        else:
            start = data[: rez[0][1]-1]
            non_start = data[rez[0][1]:]
    else:
        list_lch = []
        for i in range(len(rez[:-3])):
            index_l_ch = rez[i][1]
            index_l_ch_i_plus_one = rez[i+1][1]
            period = data[index_l_ch:index_l_ch_i_plus_one-1]
            list_lch.append(period)
        per_start = data[:rez[0][1]-1]
        list_lch.insert(0, per_start)
        per_end = data[rez[-3][1]:]
        list_lch.append(per_end)
        start = []
        non_start = []
        for i in list_lch:
            if (list_lch.index(i)+1) % 2 ==0:
                non_start.append(i)
            else:
                start.append(i)
    start_who = who_sow(start)
    second_who = who_sow(non_start)
    start.append(start_who)
    non_start.append(second_who)
    return start, non_start

def get_info_for_floaterrupt_lch(data, start):
    if start!= [None, None]:
        # prfloat(f' eto start wit non None: {start}')
        if type(start[0])==list:
            start_calc = start[:-1]
            # prfloat(f'eto len start = {len(start)} eto start : {start}')
            lens = [len(x) for x in start_calc] if len(start)>2 else [1 for x in start_calc]
            max_len_favor = max(lens)
            sum_len_favor = sum(lens)
            otn_len_favor_set = float(sum_len_favor /len(data))
        else:
            lens = len(start[:-1])
            max_len_favor = lens
            sum_len_favor = lens
            otn_len_favor_set = float(sum_len_favor /len(data))
    else:
        # prfloat(f' eto start with None : {start}')
        lens = 0
        max_len_favor = 0
        sum_len_favor = 0
        otn_len_favor_set = 0

    return {"lens": lens, "max_len_favor": max_len_favor, "sum_len_favor": sum_len_favor, "otn_len_favor_set": otn_len_favor_set}

def del_zero_in_set(set):
    set = set[1:] if set[0]==0 else set
    if 'second' or 'first' in set[-1]:
        set= set[:-1]
    return set


""" Функции для отрезков непрерывного забития"""

def get_non_stop_goal_first_team(data): # на вход сет - расчет для 1 команды
    smal = []
    big = []
    for i in range(len(data)-1):
        rez = data[i+1] - data[i]
        if  rez ==1 :
            # prfloat(f' eto rez : {rez}, eto data[i+1]: {data[i+1]}, eto data[i] : {data[i]}')
            smal.append(data[i+1])
        elif rez ==2 :
            # prfloat(f' eto rez gde 2: {rez}, eto data[i+1]: {data[i+1]}, eto data[i] : {data[i]}')
            smal.append(data[i+1])
        else:
            # prfloat(f' eto rez WROMG : {rez}')
            if len(smal)>1:
                # prfloat(f' eto smal : {smal}')
                sm = smal.copy()
                big.append(sm)
                smal.clear()
    if len(smal)>1:
        big.append(smal)
    if len(big)>0:
        # big = [[0, 1], [1, 1], [1, 1], [1, 2, 3], [2, 2], [2, 2], [-4, -3, -2, -1, 0,1,2], [0, 1, 2], [2, 3]]
        big_with_lch = [x for x in big if set([-1,0,1]).issubset(x)]
        lens_no_l_ch = max([len(x) for x in big]) if len(big)>0 else 0
        lens_with_l_ch = max([len(x) for x in big_with_lch]) if len(big_with_lch)>0 else 0
        sum_lens_no_l_ch = sum([len(x) for x in big]) if len(big)>0 else 0
        sum_with_l_ch = sum([len(x) for x in big_with_lch]) if len(big_with_lch)>0 else 0


        max_no_l_ch = max([max(x) for x in big]) if len(big)>0 else 0
        max_with_l_ch = max([max(x) for x in big_with_lch]) if len(big_with_lch)>0 else 0
    else:
        lens_no_l_ch = 0
        lens_with_l_ch = 0
        max_no_l_ch = 0
        max_with_l_ch = 0
        sum_lens_no_l_ch = 0
        sum_with_l_ch = 0
    len_data = len(data)
    max_len_no_l_ch_to_len_set = lens_no_l_ch/len_data
    max_len__with_l_ch_to_len_set = lens_with_l_ch / len_data
    sum_lens_no_l_ch_to_set = sum_lens_no_l_ch/len_data
    sum_lens_with_l_ch_to_set = sum_with_l_ch/len_data
    return {'first_t_max_scor_no_lch': max_no_l_ch, 'first_t_max_scor_with_lch': max_with_l_ch,\
            'first_t_max_len_non_stop_goal_no_lch': lens_no_l_ch, 'first_t_max_len_non_st_goal_with_l_ch':lens_with_l_ch,\
            'first_t_lens_no_l_ch_to_len_set': max_len_no_l_ch_to_len_set, 'first_t_lens_with_l_ch_to_len_set': max_len__with_l_ch_to_len_set,\
            'first_t_sum_lens_no_l_ch_to_set': sum_lens_no_l_ch_to_set, 'first_t_sum_lens_with_l_ch_to_set': sum_lens_with_l_ch_to_set}

def get_non_stop_goal_sec_team(data): # на вход сет - расчет для 1 команды
    smal = []
    big = []
    for i in range(len(data)-1):
        rez = data[i+1] - data[i]
        if  rez == -1 :
            # prfloat(f' eto rez : {rez}, eto data[i+1]: {data[i+1]}, eto data[i] : {data[i]}')
            smal.append(data[i+1])
        elif rez == -2 :
            # prfloat(f' eto rez gde 2: {rez}, eto data[i+1]: {data[i+1]}, eto data[i] : {data[i]}')
            smal.append(data[i+1])
        else:
            # prfloat(f' eto rez WROMG : {rez}')
            if len(smal)>1:
                # prfloat(f' eto smal : {smal}')
                sm = smal.copy()
                big.append(sm)
                smal.clear()
    if len(smal)>1:
        big.append(smal)
    if len(big)>0:
        # big = [[0, 1], [1, 1], [1, 1], [1, 2, 3], [2, 2], [2, 2], [-4, -3, -2, -1, 0,1,2], [0, 1, 2], [2, 3]]
        big_with_lch = [x for x in big if set([1, 0,-1]).issubset(x)]
        lens_no_l_ch = max([len(x) for x in big]) if len(big)>0 else 0
        lens_with_l_ch = max([len(x) for x in big_with_lch]) if len(big_with_lch)>0 else 0
        sum_lens_no_l_ch = sum([len(x) for x in big]) if len(big)>0 else 0
        sum_with_l_ch = sum([len(x) for x in big_with_lch]) if len(big_with_lch)>0 else 0


        max_no_l_ch = min([min(x) for x in big]) if len(big)>0 else 0
        max_with_l_ch = min([min(x) for x in big_with_lch]) if len(big_with_lch)>0 else 0
    else:
        lens_no_l_ch = 0
        lens_with_l_ch = 0
        max_no_l_ch = 0
        max_with_l_ch = 0
        sum_lens_no_l_ch = 0
        sum_with_l_ch = 0
    len_data = len(data)
    max_len_no_l_ch_to_len_set = lens_no_l_ch/len_data
    max_len__with_l_ch_to_len_set = lens_with_l_ch / len_data
    sum_lens_no_l_ch_to_set = sum_lens_no_l_ch/len_data
    sum_lens_with_l_ch_to_set = sum_with_l_ch/len_data
    return {'sec_t_max_scor_no_lch': max_no_l_ch, 'sec_t_max_scor_with_lch': max_with_l_ch,\
            'sec_t_max_len_non_stop_goal_no_lch': lens_no_l_ch, 'sec_t_max_len_non_st_goal_with_l_ch':lens_with_l_ch,\
            'sec_t_lens_no_l_ch_to_len_set': max_len_no_l_ch_to_len_set, 'sec_t_lens_with_l_ch_to_len_set': max_len__with_l_ch_to_len_set,\
            'sec_t_sum_lens_no_l_ch_to_set': sum_lens_no_l_ch_to_set, 'sec_t_sum_lens_with_l_ch_to_set': sum_lens_with_l_ch_to_set}

""" Небльшише досчеты : мода, медиана, std, +4"""

""" Получение массива из +4 для 1 команды"""
def pl_two_1_team(set): # на вход 1 строка  - 1 игра
    len_set = len(set)
    count = 0
    for i in set:
        if i >= 4:
            count+=1
    len_to_set = count/len_set
    # return {'quantity_pl_4_1_team': count, 'len_pl_4_to_set_1_team': len_to_set}
    return {'len_pl_4_to_set_1_team': len_to_set}

""" Получение массива из +4 для 1 команды"""
def pl_two_2_team(set): # на вход 1 строка  - 1 игра
    len_set = len(set)
    count = 0
    for i in set:
        if i <= -4:
            count+=1
    len_to_set = count/len_set
    # return {'quantity_pl_4_1_team': count, 'len_pl_4_to_set_1_team': len_to_set}
    return {'len_pl_4_to_set_1_team': len_to_set}