import numpy as np
import pandas as pd
import re
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')
import os
from tqdm import tqdm


def transform_data_pr(input_path, file, parsers, drug):
    # import data and transpose
    filepath = os.path.join(input_path, file)
    df_raw = pd.read_excel(filepath)
    num_subjects = len(set([i for i in df_raw.iloc[5,:].values if isinstance(i, int)]))
    
    if df_raw.shape[1] > num_subjects+1:
        df_raw = df_raw.iloc[:,:num_subjects+1]
    
    df_raw = df_raw.T
    df_raw.reset_index(inplace=True)

    # modify the header
    new_header = df_raw.iloc[0]   #grab the first row for the header
    df = df_raw[1:]               #take the data except the header row
    df.columns = new_header 
    df.reset_index(drop=True, inplace=True)
    df.drop(['Filename', 'Experiment', 'Group', 'MSN', 'FR'], axis=1, inplace=True)
    
    # change data types
    cols = df.columns.tolist()
    int_columns = ['box','last ratio']

    for col in cols:
        name = col.lower()
        if ('active' in name) or ('reward' in name) or (name in int_columns):
            df[col] = df[col].astype('int32')
        elif ('date' in name):
            df[col] = df[col].apply(lambda x: datetime.strptime(x, "%Y-%m-%d").date())
        elif ('time' in name):
            df[col] = df[col].apply(lambda x: datetime.strptime(x, "%H:%M:%S").time())
        else:
            pass
        
    # reorganize the columns
    colnames = df.columns.tolist()
    reward_col_begin = colnames.index('Reward 1')
    df['Reward Points'] = df.iloc[:, reward_col_begin:].values.tolist()
    points_col_begin = df.columns.tolist().index('Reward Points')
    df.drop(df.iloc[:, reward_col_begin:points_col_begin], inplace=True, axis=1)
    df.rename(columns={"Reward": "Reward Presses"}, inplace=True)
    df['Reward Points'] = df['Reward Points'].apply(lambda x: [i for i in x if i > 0])
    df['Breakpoint'] = df['Reward Points'].apply(lambda lst: lst[-1] if len(lst) > 0 else 0)
    
    # parse the file name
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
               'Last Ratio','Breakpoint','Active Lever Presses','Inactive Lever Presses','Reward Presses','Reward Points']
    df = df[new_columns]
    df = df.sort_values(by='Subject').reset_index(drop=True)
    
    return df


# -----------------------------------------------------------------------------------
if __name__ == "__main__":
    input_path = '__file path for input excel PR data__'
    output_path = '__file path for output transformed PR data__'
    parsers = [r"(\A[A-Z]+[0-9]+[A-Z|0-9]{1})(C[0-9]{2})HS[OXY]*((?:LGA|SHA|PR|TREATMENT)[0-9]+)_output",
               r"(\AC[0-9]{2})HS[OXY]*((?:LGA|SHA|PR|TREATMENT)[0-9]+)_output"]
    drug = '__use oxycodone or cocaine__'
    files = [i for i in sorted(os.listdir(input_path)) if i != '.DS_Store']

    for i in tqdm(range(len(files))):
        df = transform_data_pr(input_path, files[i], parsers, drug)
        filename = files[i][:-11] + 'transformed.csv'
        df.to_csv(os.path.join(output_path, filename))