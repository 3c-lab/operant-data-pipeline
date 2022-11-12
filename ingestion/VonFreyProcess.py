import pandas as pd
from config import *
from VonFreySubject import VonFreySubject

class VonFreyProcess:

    def __init__(self, filepath):
        self.filepath = filepath
        self.df = pd.read_csv(self.filepath,index_col=0)


    def insert_subject(self, subject: VonFreySubject):
        subject.process_characteristics()
        subject.insert_characteristics()


    def insert_data(self):
        for index, subject_row in self.df.iterrows():
            subject = VonFreySubject(subject_row)
            self.insert_subject(subject)
        print("INSERTED SUCCESSFUL")
        return


def main():
    for file in VON_FREY_FILES:
        print(file)
        vf = VonFreyProcess(file)
        vf.insert_data()


if __name__ == '__main__':
    main()
    