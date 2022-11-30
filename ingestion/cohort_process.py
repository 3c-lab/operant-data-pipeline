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
        if type == 'cocaine':
            self.df_sheets = pd.read_excel(self.excel_filepath, sheet_name = None, converters = cocaine_excel_converters)
        else:
            self.df_sheets = pd.read_excel(self.excel_filepath, sheet_name = None, converters= oxycodone_excel_converters)
        self.df_timeline = self.get_df_excel_file(self.df_sheets['Timeline']) if 'Timeline' in self.df_sheets.keys() else self.get_df_excel_file(self.df_sheets['Information Sheet'])
        self.df_exit_tab = self.get_df_excel_file(self.df_sheets['Exit Tab'])
        self.df_exit_tab = self.df_exit_tab.drop(['rat', 'cohort'], axis=1)

        # Left join for timeline and exit tab sheets to add details on deaths and replacements
        self.df_final = pd.merge(self.df_timeline, self.df_exit_tab, how='left', on='rfid')
        # Testing to replace 'nan' values with None to solve type errors from inserting into DB
        # self.df_final =  self.df_final.where(self.df_final.notnull(), None)
        # self.df_final.replace('nan', None)
        # self.df_final.fillna(np.nan).replace([np.nan], [-100])

        # Another attempt to fix types 
        # list_integer_cols = ['cohort', 'litter number', 'litter size', 'shipping box']
        # self.df_final[list_integer_cols] = self.df_final[list_integer_cols].astype(int)

 
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

    def insert_cohort(self):
        '''
            Loop through all subjects of the cohort and insert them into the database
        '''
        for index, subject_row in self.df_final.iterrows():
            subject = Subject(subject_row)
            self.insert_subject(subject)
        print(self.df_final)
        return

def main():
    # for cocaine_cohort in COCAINE_COHORT_ALL:
    #     cohort = CohortProcess(cocaine_cohort, "cocaine")
    #     cohort.insert_cohort()
    for oxy_cohort in OXYCODONE_COHORT_ALL:
        cohort = CohortProcess(oxy_cohort, "oxycodone")
        cohort.insert_cohort()


if __name__ == '__main__':
    main()