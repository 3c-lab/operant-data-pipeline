import pandas as pd
import re
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')
import os
from tqdm import tqdm

df_rfid_coc = pd.read_csv('rfid_cocaine.csv', index_col=0)
df_rfid_coc

def transform_shock(input_path, file, parsers):
    # import data and transpose
    filepath = os.path.join(input_path, file)
    df_raw = pd.read_excel(filepath)
    
    # ?
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
    int_columns = ['box','total shocks','total reward']

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
    
    reward_shock_begin = colnames.index('Reward # Got Shock 1')
    reward_col_begin = colnames.index('Reward 1')
    reward_col_end = colnames.index('Reward 201')

    df['Rewards Got Shock'] = df.iloc[:,reward_shock_begin:reward_col_begin].values.tolist()
    df['Reward Timestamps'] = df.iloc[:,reward_col_begin:reward_col_end+1].values.tolist()
    
    df.drop(df.iloc[:, reward_shock_begin:reward_col_end+1], inplace=True, axis=1)
    
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
    df['Drug'] = ['cocaine'] * len(df)
    
    # get the final output
    new_columns = ['Subject','Room','Cohort','Trial ID','Drug','Box','Start Time','End Time','Start Date','End Date',
                   'Total Active Lever Presses', 'Total Inactive Lever Presses','Total Shocks', 'Total Reward', 
                   'Rewards After First Shock','Rewards Got Shock', 'Reward Timestamps']
    
    df = df[new_columns]
    df = df.sort_values(by='Subject').reset_index(drop=True)
    df.rename(columns=str.lower,inplace=True)
    df = pd.merge(df, df_rfid_coc,  how='left', on = ['subject'])
    old_columns = df.columns.tolist()
    new_columns = [old_columns[-1]] + old_columns[:-1]
    df = df[new_columns]
    df.columns = df.columns.str.replace(' ','_')
    df.fillna({'rfid':-999}, inplace=True)
    
    # store the final output in csv
    filename = file[:-11] + 'transformed.csv'
    df.to_csv(os.path.join(output_path, filename))


# -----------------------------------------------------------------------------------
if __name__ == "__main__":
    input_path = '__file path for input excel SHOCK data__'
    output_path = '__file path for output transformed SHOCK data__'
    parsers = [r"(\A[A-Z]+[0-9]+[A-Z|0-9]{1})(C[0-9]{2})HS((?:PRESHOCK|SHOCK))",
               r"(\AC[0-9]{2})HS((?:PRESHOCK|SHOCK))"]
    files = [i for i in sorted(os.listdir(input_path)) if i != '.DS_Store']

    for i in tqdm(range(len(files))):
        transform_shock(input_path, files[i], parsers)