import pandas as pd
import config
from collections import defaultdict
from datetime import datetime


class Subject:

    def __init__(self, subject_row):
        '''
            characteristics are only one value
            Measurements are repeated (numbered) values
        '''
        self.characteristics = {}
        self.measurements = {}
        self.subject_row = subject_row

    def process_characteristics(self):
        '''
            Get all the information about the subject
            that isn't a measurement
        '''
        self.characteristics['Arrival Date'] = self.format_date(self.subject_row['Arrival Date'])
        self.characteristics['Brevital'] = self.subject_row['Brevital']
        self.characteristics['Brevital Date'] = self.format_date(self.subject_row['Brevital Date'])
        # TODO: Consider brevital_done_by to be in measurements as it could have multiple technicians
        # self.characteristics['Brevital Done By'] = self.subject_row['Brevital Done By']
        self.characteristics['Coat Color'] = self.subject_row['Coat Color']
        self.characteristics['Date of Birth'] = self.format_date(self.subject_row['Date of Birth'])
        self.characteristics['Date of Death'] = self.format_date(self.subject_row['Date of Death'])
        self.characteristics['Date of Eye Bleed'] = self.format_date(self.subject_row['Date of Eye Bleed'])
        self.characteristics['Date of Ship'] = self.format_date(self.subject_row['Date of Ship'])
        self.characteristics['Date of Wean'] = self.format_date(self.subject_row['Date of Wean'])
        self.characteristics['Dissection Date'] = self.format_date(self.subject_row['Dissection Date'])
        self.characteristics['Ear Punch'] = self.subject_row['Ear Punch']
        self.characteristics['Group for Pre-Shock'] = self.subject_row['Group for Pre-Shock']
        self.characteristics['Group for Shock'] = self.subject_row['Group for Shock']
        # TODO: Consider handled_by to be in measurements as it could have multiple technicians
        # self.characteristics['Handled By'] = self.subject_row['Handled By']
        self.characteristics['LgA16 Date'] = self.format_date(self.subject_row['LgA16 Date'])
        self.characteristics['LgA15 Date'] = self.format_date(self.subject_row['LgA15 Date'])
        self.characteristics['LgA17 Date'] = self.format_date(self.subject_row['LgA17 Date'])
        self.characteristics['LgA18 Date'] = self.format_date(self.subject_row['LgA18 Date'])
        # TODO: Should we store litter number and size as integer or string?
        self.characteristics['Litter Number'] = self.subject_row['Litter Number']
        self.characteristics['Litter Size'] = self.subject_row['Litter Size']
        self.characteristics['Long Access End Date'] = self.format_date(self.subject_row['Long Access End Date'])
        self.characteristics['Long Access Start Date'] = self.format_date(self.subject_row['Long Access Start Date'])
        self.characteristics['Pre-Shock Date'] = self.format_date(self.subject_row['Pre-Shock Date'])
        self.characteristics['Rack'] = self.subject_row['Rack']
        self.characteristics['RAT'] = self.subject_row['RAT']
        self.characteristics['Recatheter Surgeon'] = self.subject_row['Recatheter Surgeon']
        self.characteristics['Recatheter Surgery Date'] = self.format_date(self.subject_row['Recatheter Surgery Date'])
        # TODO: Store as integer or string?
        self.characteristics['RFID'] = self.subject_row['RFID']
        self.characteristics['Shipping Box'] = self.subject_row['Shipping Box']
        self.characteristics['Shock (0.1mA) Date'] = self.format_date(self.subject_row['Shock (0.1mA) Date'])
        self.characteristics['Shock (0.2mA) Date'] = self.format_date(self.subject_row['Shock (0.2mA) Date'])
        self.characteristics['Shock (0.3mA) Date'] = self.format_date(self.subject_row['Shock (0.3mA) Date'])
        self.characteristics['Short Access End Date'] = self.format_date(self.subject_row['Short Access End Date'])
        self.characteristics['Short Access Start Date'] = self.format_date(self.subject_row['Short Access Start Date'])
        self.characteristics['Surgeon'] = self.subject_row['Surgeon']
        self.characteristics['Surgery Assist'] = self.subject_row['Surgery Assist']
        self.characteristics['Surgery Date'] = self.format_date(self.subject_row['Surgery Date'])

    def format_date(self, date):
        '''
            Convert all date values into a consistent format. If the value is null, replace it with None
            for insertion into the database
        '''
        if pd.isnull(date):
            return None
        else:
            return datetime.strftime(date, "%m/%d/%Y %H:%M:%S")

    def construct_charactersitic_sql_string(self):
        values = ','.join(['%s'] * len(self.characteristics))
        sql_string = f"""INSERT INTO subject VALUES ({values});""", tuple([value for key, value in sorted(self.characteristics.items())])
        print(sql_string)
        return sql_string

    def get_insert_sql_string(self):
        '''
            Function to join all the values of characteristics together, separated by comma, to insert into the database
        '''
        sql_string = self.construct_sql_string()
        # print([(value, type(value)) for kev, value in sorted(self.characteristics.items())])

    def process_measurements(self):

        return 

