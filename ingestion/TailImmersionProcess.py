import pandas as pd
from config import *
from TailImmersionSubject import TailImmersionSubject

class TailImmersionProcess:

    def __init__(self, filepath):
        self.filepath = filepath
        self.df = pd.read_csv(self.filepath,index_col=0)


    def insert_subject(self, subject: TailImmersionSubject):
        subject.process_characteristics()
        subject.insert_characteristics()


    def insert_data(self):
        for index, subject_row in self.df.iterrows():
            subject = TailImmersionSubject(subject_row)
            self.insert_subject(subject)
        print("INSERTED SUCCESSFUL")
        return


def main():
    for file in TAIL_IMMERSION_FILES:
        print(file)
        ti = TailImmersionProcess(file)
        ti.insert_data()


if __name__ == '__main__':
    main()
