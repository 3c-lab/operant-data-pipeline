import os
import pandas as pd
import numpy as np
import psycopg2
from config import *
from pipeline import Pipeline
from subject import Subject

class CohortProcess:

    def __init__(self, filepath, type):
        self.excel_filepath = filepath
        self.cohort_subjects = []
        self.subjects = []
        self.type = type
        if type == 'cocaine':
            self.df_sheets = pd.read_excel(self.excel_filepath, sheet_name = None, converters = cocaine_excel_converters)
        else:
            self.df_sheets = pd.read_excel(self.excel_filepath, sheet_name = None, converters= oxycodone_excel_converters)
        self.df_timeline = self.get_df_excel_file(self.df_sheets['Timeline']) if 'Timeline' in self.df_sheets.keys() else self.get_df_excel_file(self.df_sheets['Information Sheet'])
        self.df_exit_tab = self.get_df_excel_file(self.df_sheets['Exit Tab'])
        self.df_exit_tab = self.df_exit_tab.drop(['rat', 'cohort'], axis=1)

        self.df_final = pd.merge(self.df_timeline, self.df_exit_tab, how='left', on='rfid')
 
    def get_df_excel_file(self, df: pd.DataFrame):
        '''
            Function to modify passed in dataframe and convert all columns with 'date' in the column name 
            into datetime objects for easier processing into the database and other necessarily format handling.
            Converted all column names to be lowercase
        '''
        df['RFID'] = df['RFID'].astype(str)
        df.columns = (df.columns.str.replace(u'\xa0', u'')).str.strip()
        df.columns = df.columns.str.lower()
        list_date_cols = [col for col in df.columns if any(match in col.lower() for match in ['date', 'day'])]
        list_collection_cols = [col for col in df.columns if any(match in col.lower() for match in ['collection'])]
        df[list_date_cols] = df[list_date_cols].apply(pd.to_datetime, errors='coerce')
        df[list_collection_cols] = df[list_collection_cols].astype(str)
        return df

    def insert_subject(self, subject: Subject):
        subject.process_characteristics()
        subject.insert_characteristics()
        subject.process_measurements()
        subject.insert_measurements()

    def insert_cohort(self):
        '''
            Loop through all subjects of the cohort and insert them into the database
        '''
        for index, subject_row in self.df_final.iterrows():
            subject = Subject(subject_row, self.type)
            self.insert_subject(subject)
            subject.conn.close()
        
def main():
    for cocaine_cohort in COCAINE_COHORT_ALL:
        print(f'NAME OF THE COCAINE COHORT IS: {cocaine_cohort}')
        cohort = CohortProcess(cocaine_cohort, "cocaine")
        cohort.insert_cohort()
    for oxy_cohort in OXYCODONE_COHORT_ALL:
        print(f'NAME OF THE OXY COHORT IS: {oxy_cohort}')
        cohort = CohortProcess(oxy_cohort, "oxycodone")
        cohort.insert_cohort()

if __name__ == '__main__':
    main()