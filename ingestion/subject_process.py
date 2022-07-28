import pandas as pd
import config
from collections import defaultdict
from datetime import date, datetime


class Subject:

    def __init__(self, subject_row):
        '''
            characteristics are only one value
            Measurements are repeated (numbered) values
        '''
        self.rfid = subject_row['RFID']
        self.characteristics = {}
        self.measurements = []
        self.subject_row = subject_row

    def process_characteristics(self):
        '''
            Get all the information about the subject
            that isn't a measurement
        '''

        # TODO: Consider brevital_done_by to be in measurements as it could have multiple technicians
        # TODO: Consider handled_by to be in measurements as it could have multiple technicians
        for characteristic in config.cocaine_characteristics_list:
            if 'date' in characteristic.lower():
                self.characteristics[characteristic] = self.format_date(self.subject_row[characteristic])
            else:
                self.characteristics[characteristic] = self.subject_row[characteristic]

        # self.characteristics['Arrival Date'] = self.format_date(self.subject_row['Arrival Date'])
        # self.characteristics['Brevital'] = self.subject_row['Brevital']
        # self.characteristics['Brevital Date'] = self.format_date(self.subject_row['Brevital Date'])
        # # self.characteristics['Brevital Done By'] = self.subject_row['Brevital Done By']
        # self.characteristics['Coat Color'] = self.subject_row['Coat Color']
        # self.characteristics['Date of Birth'] = self.format_date(self.subject_row['Date of Birth'])
        # self.characteristics['Date of Death'] = self.format_date(self.subject_row['Date of Death'])
        # self.characteristics['Date of Eye Bleed'] = self.format_date(self.subject_row['Date of Eye Bleed'])
        # self.characteristics['Date of Ship'] = self.format_date(self.subject_row['Date of Ship'])
        # self.characteristics['Date of Wean'] = self.format_date(self.subject_row['Date of Wean'])
        # self.characteristics['Dissection Date'] = self.format_date(self.subject_row['Dissection Date'])
        # self.characteristics['Ear Punch'] = self.subject_row['Ear Punch']
        # self.characteristics['Group for Pre-Shock'] = self.subject_row['Group for Pre-Shock']
        # self.characteristics['Group for Shock'] = self.subject_row['Group for Shock']
        # # self.characteristics['Handled By'] = self.subject_row['Handled By']
        # self.characteristics['LgA16 Date'] = self.format_date(self.subject_row['LgA16 Date'])
        # self.characteristics['LgA15 Date'] = self.format_date(self.subject_row['LgA15 Date'])
        # self.characteristics['LgA17 Date'] = self.format_date(self.subject_row['LgA17 Date'])
        # self.characteristics['LgA18 Date'] = self.format_date(self.subject_row['LgA18 Date'])
        # # TODO: Should we store litter number and size as integer or string?
        # self.characteristics['Litter Number'] = self.subject_row['Litter Number']
        # self.characteristics['Litter Size'] = self.subject_row['Litter Size']
        # self.characteristics['Long Access End Date'] = self.format_date(self.subject_row['Long Access End Date'])
        # self.characteristics['Long Access Start Date'] = self.format_date(self.subject_row['Long Access Start Date'])
        # self.characteristics['Pre-Shock Date'] = self.format_date(self.subject_row['Pre-Shock Date'])
        # self.characteristics['Rack'] = self.subject_row['Rack']
        # self.characteristics['RAT'] = self.subject_row['RAT']
        # self.characteristics['Recatheter Surgeon'] = self.subject_row['Recatheter Surgeon']
        # self.characteristics['Recatheter Surgery Date'] = self.format_date(self.subject_row['Recatheter Surgery Date'])
        # # TODO: Store as integer or string?
        # self.characteristics['RFID'] = self.subject_row['RFID']
        # self.characteristics['Shipping Box'] = self.subject_row['Shipping Box']
        # self.characteristics['Shock (0.1mA) Date'] = self.format_date(self.subject_row['Shock (0.1mA) Date'])
        # self.characteristics['Shock (0.2mA) Date'] = self.format_date(self.subject_row['Shock (0.2mA) Date'])
        # self.characteristics['Shock (0.3mA) Date'] = self.format_date(self.subject_row['Shock (0.3mA) Date'])
        # self.characteristics['Short Access End Date'] = self.format_date(self.subject_row['Short Access End Date'])
        # self.characteristics['Short Access Start Date'] = self.format_date(self.subject_row['Short Access Start Date'])
        # self.characteristics['Surgeon'] = self.subject_row['Surgeon']
        # self.characteristics['Surgery Assist'] = self.subject_row['Surgery Assist']
        # self.characteristics['Surgery Date'] = self.format_date(self.subject_row['Surgery Date'])

    def process_measurements(self):
        for measurement_dict in config.cocaine_measurements_list:
    
            counts = measurement_dict['counts']
            suffixes = measurement_dict['col_suffix']

            # Loop through each count of the measurement
            for i in range(1, counts+1):

                # Use default dict as we will need all access all values to insert into database
                insert_dict = defaultdict(lambda: None)
                col_name = measurement_dict['col_name']
                current_number = i

                insert_dict['name'] = measurement_dict['measurement_name']
                insert_dict['measure_number'] = current_number
                
                for suffix in suffixes:
                    # This is used to query for the value of a specific column referencing a measurement value for the current subject (row)
                    # TODO: Strip is to account for columns whose value that are denoted by empty str instead of 'Value'
                    full_col_name = ' '.join([col_name, str(current_number), suffix]).strip()                    

                    if suffix == '':
                        insert_dict['value'] = self.subject_row[full_col_name]
                    elif suffix == 'By' or suffix == 'Collection':
                        insert_dict['technician'] = self.subject_row[full_col_name]
                    elif suffix == 'Date':
                        insert_dict['date_measured'] = self.subject_row[full_col_name]

                self.measurements.append(insert_dict)

        return 

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
        values = ','.join(['%s'] * config.CHARACTERISTIC_TABLE_COLUMNS_COUNT)
        sql_string = f"""INSERT INTO {config.CHARACTERISTIC_TABLE_NAME} VALUES ({values});""", tuple([value for key, value in self.characteristics.items()])
        return sql_string

    def construct_measurement_sql_string(self, single_subject_measurement: defaultdict):
        
        values = ','.join(['%s'] * config.MEASUREMENT_TABLE_COLUMNS_COUNT)
        rfid = self.rfid
        name = single_subject_measurement['name']
        value = single_subject_measurement['value']
        measure_number = single_subject_measurement['measure_number']
        date_measured = single_subject_measurement['date_measured']
        technician = single_subject_measurement['technician']
        sql_string = f"""INSERT INTO measurement VALUES ({values});""", tuple([rfid, name, measure_number, value, date_measured, technician])
        return sql_string

    def insert_characteristics(self):
        sql_string = self.construct_charactersitic_sql_string()
        print(sql_string)

    def insert_measurements(self):
        sql_string = self.construct_measurement_sql_string(self.measurements[0])
        print(sql_string)

        

    

