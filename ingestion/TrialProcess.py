import pandas as pd
from config import *
from TrialSubject import TrialSubject

class TrialProcess:

    def __init__(self, filepath, table_id):
        self.filepath = filepath
        self.df = pd.read_csv(self.filepath,index_col=0)
        self.df_final = self.process_df(self.df)
        self.table_id = table_id

 
    def process_df(self, df: pd.DataFrame):
        # placeholder method for later revision (maybe add the cleaning script to here?)
        dff = df[df['rfid'] != -999].reset_index(drop=True)
        return dff


    def insert_subject(self, subject: TrialSubject):
        subject.process_characteristics()
        subject.insert_characteristics()


    def insert_trial(self):
        for index, subject_row in self.df_final.iterrows():
            subject = TrialSubject(subject_row, self.table_id)
            self.insert_subject(subject)
        print("INSERTED SUCCESSFUL")
        return


def main():
    for file in TRIAL_LGA_FILES:
        print(file)
        trial = TrialProcess(file, 'LGA')
        trial.insert_trial()


if __name__ == '__main__':
    main()