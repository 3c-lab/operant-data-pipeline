import pandas as pd
import os
from tqdm import tqdm
from datetime import datetime

# load the rfid dataset
df_rfid = pd.read_csv('trial_data/trials_rfid_merge.csv')
df_rfid.rename(columns={"rat": "Subject", "cohort":"Cohort", "drug group":"Drug"}, inplace=True)
df_rfid['Drug'] = df_rfid['Drug'].str.lower()

# Merging & Cleaning for Tail Immersion data
input_path = 'Tail_Immersion'
output_path = 'Cleaned_Tail_Immersion'
files = [i for i in sorted(os.listdir(input_path)) if (i != '.DS_Store')]

for i in tqdm(range(len(files))):
    df_ti = pd.read_excel(os.path.join('Tail_Immersion', files[i]), index_col=0)
    # lowercase for merging
    df_ti['Drug'] = df_ti['Drug'].str.lower()
    res = pd.merge(df_ti, df_rfid,  how='left', on = ['Subject','Cohort','Drug'])
    # rearrange columns
    old_columns = res.columns.tolist()
    new_columns = [old_columns[-1]] + old_columns[:-1]
    res = res[new_columns]
    # rename columns
    res.rename(columns=str.lower,inplace=True)
    res.columns = res.columns.str.replace(' ','_')
    # (need to change later) for null rfid
    res['rfid'] = res['rfid'].fillna(-999)
    res.to_csv(os.path.join(output_path, files[i].split('.')[0] + '.csv'))


################################################################################################
# Merging & Cleaning for Von Frey data

def parse_date(date_string):
    first_date = date_string.split('-')[0]
    date = datetime.strptime(first_date, "%m/%d/%y").date()
    return date

input_path = 'Von_Frey'
output_path = 'Cleaned_Von_Frey'
files = [i for i in sorted(os.listdir(input_path)) if (i != '.DS_Store')]

for i in tqdm(range(len(files))):
    df_vf = pd.read_excel(os.path.join(input_path, files[i]))
    df_vf['Drug'] = df_vf['Drug'].str.lower()
    res = pd.merge(df_vf, df_rfid,  how='left', on = ['Subject','Cohort','Drug'])
    old_columns = res.columns.tolist()
    new_columns = [old_columns[-1]] + old_columns[:-1]
    res = res[new_columns]
    res.rename(columns=str.lower,inplace=True)
    res.columns = res.columns.str.replace(' ','_')
    
    for col in res.columns:
        if ('date' in col) and res[col].dtype != '<M8[ns]':
            res[col] = res[col].apply(lambda x: parse_date(x))
    
    res['rfid'] = res['rfid'].fillna(-999)
    res.to_csv(os.path.join(output_path, files[i].split('.')[0] + '.csv'))
    