import os
import pandas as pd
import psycopg2
from config import *
from pipeline import Pipeline
from subject import Subject

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
        df = pd.read_excel(self.excel_filepath)[0:70]
        df['RFID'] = df['RFID'].astype(int)
        df.columns = (df.columns.str.replace(u'\xa0', u'')).str.strip()
        list_date_cols = [col for col in df.columns if 'date' in col.lower()]
        df[list_date_cols] = df[list_date_cols].apply(pd.to_datetime, errors='coerce')
        df.columns = df.columns.str.lower()
        return df

    def insert_subject(self, subject: Subject):
        subject.process_characteristics()
        # subject.process_measurements()
        subject.insert_characteristics()
        # subject.insert_measurements()



    def insert_cohort(self):
        '''
            Loop through all subjects of the cohort and insert them into the database
        '''
        for index, subject_row in self.df[0:1].iterrows():
            subject = Subject(subject_row)
            self.insert_subject(subject)
        return



def main():
    process_7 = CohortProcess(COCAINE_COHORT_07)
    # N/A and empty cell both return NaT value
    process_7.insert_cohort()


if __name__ == '__main__':
    main()