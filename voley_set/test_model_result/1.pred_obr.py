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
from func_0_pred_obr import *

df  = pd.read_csv("output_all_sex.csv", low_memory=False)
# df = df.drop(['Unnamed: 0'], axis=1)
print(df.columns)
df = df.dropna(how='any')
js = df.to_json(orient = 'records')
data  = json.loads(js)

"""1. Обработка датасета через 2 функции get_correct_data и get_pred_obrab_data"""
data = get_correct_data(data)
data = get_pred_obrab_data(data)
with open('data_pred_obr.json', 'w') as f:
    f.write(json.dumps(data))

print(f' all done, eto len : {len(data)}')
print(data[0])
print(data[0].keys())