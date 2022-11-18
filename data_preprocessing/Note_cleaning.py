import pandas as pd
import os
from tqdm import tqdm
from datetime import datetime

input_path = 'INPUT_PATH'
output_path = 'OUTPUT_PATH'
files = ['ALL NOTE FILES (excelsheets)']

for f in files:
    print(f)
    test = pd.read_excel(os.path.join(input_path, f))
    # possible duplicates in the notes
    test.drop_duplicates(inplace=True)
    # modify column names & format
    test.rename(columns=str.lower,inplace=True)
    test.columns = test.columns.str.replace(' ','_')
    test.drug = test.drug.str.lower()
    test.trial_id = test.trial_id.str.upper()
    # "All" was used to represent the entire cohorts data in some files
    test.rfid.replace('All', 0, inplace = True)
    # also note that sometimes there will be missing rfid in the file
    test.to_csv(os.path.join(output_path, f.split('.')[0] + '.csv'))