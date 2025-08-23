import pandas as pd
import os
import io
from datetime import datetime

RFID_OXY = pd.read_csv('target_csv_for_rfid_oxycodone.csv', index_col=0)
RFID_OXY['rfid'].isna().sum()

def parse_date(date_string):
    first_date = date_string.split('-')[0]
    date = datetime.strptime(first_date, "%m/%d/%y").date()
    return date

def transform_vf(filepath):
    with open(filepath, "rb") as f:
        file_content = f.read()
    # Load the binary data into a pandas DataFrame
    df = pd.read_excel(io.BytesIO(file_content), engine='openpyxl')
    df['Drug'] = df['Drug'].str.lower()
    df.rename(columns=str.lower,inplace=True)
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace(' ','_')
    dff = pd.merge(df, RFID_OXY,  how='left', on = ['subject'])
    old_columns = dff.columns.tolist()
    new_columns = [old_columns[-1]] + old_columns[:-1]
    dff = dff[new_columns]

    for col in dff.columns:
        if ('date' in col) and dff[col].dtype != '<M8[ns]':
            dff[col] = dff[col].apply(lambda x: parse_date(x))

    output_path = 'target_csv_for_vf_output/'
    dff.to_csv(os.path.join(output_path, f.name.split('/')[-1].split('.')[0] + '.csv'), index=False)
    return dff

dfs = []
for f in dbutils.fs.ls('target_csv_for_vf_input'):
    filepath = "/" + f.path.replace(':','')
    print(filepath)
    dfs += [transform_vf(filepath)]

final = pd.concat(dfs)

if len(final) != final['rfid'].nunique() or final['rfid'].isna().sum() > 0:
    wrongs = final['rfid'].value_counts()[final['rfid'].value_counts() > 1]
    
    print("Duplicates:")
    for i in wrongs.index:
        rows = final[final['rfid'] == i][['cohort', 'subject', 'drug']]
        for _, row in rows.iterrows():
            print(f"Cohort: {row['cohort']}, Subject: {row['subject']}, Drug: {row['drug']}")

    print("\nNull RFID:")
    null_rows = final[final['rfid'].isna()][['cohort', 'subject', 'drug']]
    for _, row in null_rows.iterrows():
        print(f"Cohort: {row['cohort']}, Subject: {row['subject']}, Drug: {row['drug']}")

    # Raise appropriate exception
    if final['rfid'].isna().sum() == 0:
        raise Exception("Duplicate Data")
    elif len(final) == final['rfid'].nunique():
        raise Exception("Null Data")
    else:
        raise Exception("Dup data and Null data")


final = pd.concat(dfs)
if len(final) != final['rfid'].nunique() or final['rfid'].isna().sum()>0:
    wrongs = final['rfid'].value_counts()[final['rfid'].value_counts()>1]
    print("duplicates: ")
    for i in wrongs.index:
        print(final[final['pk']==i][['cohort','subject','drug']])
    print("null rfid: ")
    print(final[final['rfid'].isna()][['cohort','subject','drug']])
    if final['rfid'].isna().sum()==0:
        raise Exception("Duplicate Data")
    elif len(final) == final['rfid'].nunique():
        raise Exception("Null Data")
    else:
        raise Exception("Dup data and Null data")