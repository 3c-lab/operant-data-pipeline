import pandas as pd
import os
from tqdm import tqdm
from datetime import datetime

input_path = 'INPUT_PATH'
output_path = 'OUTPUT_PATH'
files = ['ALL NOTE FILES (excelsheets)']

def note_transform(filepath):
    df = pd.read_excel(filepath)
    
    # drop extra column
    initial_cols = list(map(str.lower, df.columns))
    if 'index' in initial_cols:
        idx = initial_cols.index('index')
        df.drop(df.columns[idx], axis=1, inplace=True)

    # drop duplicate data
    df.drop_duplicates(inplace=True)

    # rearrange column format
    df.rename(columns=str.lower,inplace=True)
    df.columns = df.columns.str.replace(' ','_')
    df.trial_id = df.trial_id.str.upper()
    
    df.rfid = df.rfid.astype(str)

    return df

for f in files:
    print(f)
    filepath = os.path.join(input_path, f)
    df = note_transform(filepath)
    df.to_csv(os.path.join(output_path, f.split('.')[0] + '.csv'))