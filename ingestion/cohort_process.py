import pandas as pd
import os
import config
from subject_process import Subject

class CohortProcess:

    def __init__(self, filepath):
        self.excel_filepath = filepath
        self.cohort_subjects = []
        self.subjects = []
        self.df = self.get_df_excel_file()
 
    def get_df_excel_file(self):
        '''
            Function to load in the excel file and convert all columns with 'date' in the column name 
            into datetime objects for easier processing into the database
        '''
        df = pd.read_excel(self.excel_filepath)
        list_date_cols = [col for col in df.columns if 'date' in col.lower()]
        df[list_date_cols] = df[list_date_cols].apply(pd.to_datetime, errors='coerce')
        return df

    def insert_cohort(self):
        '''
            Loop through all subjects of the cohort and insert them into the database
        '''
        for index, subject_row in self.df[0:1].iterrows():
            subject = Subject(subject_row)
            subject.process_characteristics()
            sql_string = subject.construct_charactersitic_sql_string()
        return

def main():
    process_17 = CohortProcess(config.COCAINE_COHORT_07)

if __name__ == '__main__':
    main()