import numpy as np
import pandas as pd
import re
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')
import os
from tqdm import tqdm
import math

df_rfid = pd.read_csv('trials_rfid_merge.csv')
df_rfid.rename(columns={"rat": "Subject", "cohort":"Cohort", "drug group":"Drug"}, inplace=True)
df_rfid['Drug'] = df_rfid['Drug'].str.lower()
df_rfid


if __name__ == "__main__":
    input_path = '__filepath for input transformed data__'
    output_path = '__filepath for output transformed data__'
    files = [i for i in sorted(os.listdir(input_path)) if i != '.DS_Store']

    for i in tqdm(range(len(files))):
        df = pd.read_csv(os.path.join(input_path, files[i]), index_col=0)
        # join the transformed df with rfid info & rearrange the column names
        res = pd.merge(df, df_rfid,  how='left', on = ['Subject','Cohort','Drug'])
        old_columns = res.columns.tolist()
        new_columns = [old_columns[-1]] + old_columns[:-1]
        res = res[new_columns]
        res.rename(columns=str.lower,inplace=True)
        res.columns = res.columns.str.replace(' ','_')
        res.to_csv(os.path.join(output_path, files[i]))