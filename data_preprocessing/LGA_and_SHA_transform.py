import numpy as np
import pandas as pd
import re
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')
import os
from tqdm import tqdm

def transform_data(input_path, file, parsers, drug):
    # import data and transpose
    filepath = os.path.join(input_path, file)
    df_raw = pd.read_excel(filepath).T
    df_raw.reset_index(inplace=True)

    # modify the header
    new_header = df_raw.iloc[0]   #grab the first row for the header
    df = df_raw[1:]               #take the data except the header row
    df.columns = new_header 
    df.reset_index(drop=True, inplace=True)
    df.drop(['Filename', 'Experiment', 'Group', 'MSN', 'FR'], axis=1, inplace=True)
    
    # change data types
    cols = df.columns.tolist()
    for col in cols:
        name = col.lower()
        if ('active' in name) or ('reward' in name) or ('timeout' in name) or (name == 'box'):
            df[col] = df[col].astype('int32')
        elif ('date' in name):
            df[col] = df[col].apply(lambda x: datetime.strptime(x, "%Y-%m-%d").date())
        elif ('time' in name):
            df[col] = df[col].apply(lambda x: datetime.strptime(x, "%H:%M:%S").time())
        else:
            pass
        
    # group the timestamps
    colnames = df.columns.tolist()
    active_col_begin = colnames.index('Active 1')
    inactive_col_begin = colnames.index('Inactive 1')
    reward_col_begin = colnames.index('Reward 1')
    timeout_col_begin = colnames.index('Timeout Press 1')
    df['Active Timestamps'] = df.iloc[:, active_col_begin:inactive_col_begin].values.tolist()
    df['Inactive Timestamps'] = df.iloc[:, inactive_col_begin:reward_col_begin].values.tolist()
    df['Reward Timestamps'] = df.iloc[:, reward_col_begin:timeout_col_begin].values.tolist()
    df['Timeout Timestamps'] = df.iloc[:, timeout_col_begin:].values.tolist()
    
    # reorganize the columns
    timestamp_col_begin = df.columns.tolist().index('Active Timestamps')
    df.drop(df.iloc[:, active_col_begin:timestamp_col_begin], inplace=True, axis=1)
    df.rename(columns={"Reward": "Reward Presses"}, inplace=True)
    df['Timeout Presses'] = df['Timeout Timestamps'].apply(lambda x: len([i for i in x if i != 0]))
    
    # parse the filename
    if file[0] == 'C':
        parser = parsers[1]
        cohort, trial_id = re.findall(parser, file)[0]
        room = 'N/A'
    else:
        parser = parsers[0]
        room, cohort, trial_id = re.findall(parser, file)[0]
        
    df['Room'] = [room] * len(df)
    df['Cohort'] = [cohort] * len(df)
    df['Cohort'] = df['Cohort'].apply(lambda x: int(x[1:]))
    df['Trial ID'] = [trial_id] * len(df)
    df['Drug'] = [drug] * len(df)
    
    # get the final output
    new_columns = ['Subject','Room','Cohort','Trial ID','Drug','Box','Start Time','End Time','Start Date','End Date',
                   'Active Lever Presses','Inactive Lever Presses','Reward Presses','Timeout Presses',
                   'Active Timestamps','Inactive Timestamps','Reward Timestamps','Timeout Timestamps']
    df = df[new_columns]
    
    return df


# -----------------------------------------------------------------------------------
if __name__ == "__main__":
    input_path = '__file path for input excel LGA or SHA data__'
    output_path = '__file path for output transformed LGA or SHA data__'
    parsers = [r"(\A[A-Z]+[0-9]+[A-Z|0-9]{1})(C[0-9]{2})HS[OXY]*((?:LGA|SHA)[0-9]{2})",
               r"(\AC[0-9]{2})HS[OXY]*((?:LGA|SHA)[0-9]{2})"]
    drug = '__use oxycodone or cocaine__'
    files = [i for i in sorted(os.listdir(input_path)) if i != '.DS_Store']

    for i in tqdm(range(len(files))):
        df = transform_data(input_path, files[i], parsers, drug)
        filename = files[i][:-11] + 'transformed.csv'
        df.to_csv(os.path.join(output_path, filename))