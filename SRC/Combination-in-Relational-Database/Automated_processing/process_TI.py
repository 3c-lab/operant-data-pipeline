

import pandas as pd
import os
import io

RFID_OXY = pd.read_csv('target_csv_for_rfid_oxycodone.csv', index_col=0)
RFID_OXY.head()

def transform_ti(filepath):
    with open(filepath, "rb") as f:
        file_content = f.read()
    # Load the binary data into a pandas DataFrame
    df = pd.read_excel(io.BytesIO(file_content), engine='openpyxl')
    df['Drug'] = df['Drug'].str.lower()
    df.rename(columns=str.lower,inplace=True)
    df.columns = df.columns.str.replace(' ','_')
    dff = pd.merge(df, RFID_OXY,  how='left', on = ['subject'])
    old_columns = dff.columns.tolist()
    new_columns = [old_columns[-1]] + old_columns[:-1]
    dff = dff[new_columns]

    output_path = 'target_csv_for_ti_output/'
    dff.to_csv(os.path.join(output_path, f.name.split('/')[-1].split('.')[0] + '.csv'), index=False)
    return dff

dfs = []
for f in dbutils.fs.ls('target_csv_for_ti_input'):
    filepath = "/" + f.path.replace(':','')
    dfs += [transform_ti(filepath)]

final = pd.concat(dfs)
if len(final) != final['rfid'].nunique() or final['rfid'].isna().sum()>0:
    wrongs = final['rfid'].value_counts()[final['rfid'].value_counts()>1]
    print("duplicates: ")
    for i in wrongs.index:
        print(final[final['rfid']==i][['cohort','subject','drug']])
    print("null rfid: ")
    print(final[final['rfid'].isna()][['cohort','subject','drug']])
    if final['rfid'].isna().sum()==0:
        raise Exception("Duplicate Data")
    elif len(final) == final['rfid'].nunique():
        raise Exception("Null Data")
    else:
        raise Exception("Dup data and Null data")