import math
import pandas as pd
import numpy as np
from config import *
from collections import defaultdict
from datetime import date, datetime
from pipeline import Pipeline

class Subject(Pipeline):

    def __init__(self, subject_row):
        '''
            characteristics are only one value
            Measurements are repeated (numbered) values
        '''
        # self.rfid = int(subject_row['rfid'])
        self.characteristics = defaultdict(lambda: None)
        self.measurements = []
        self.subject_row = subject_row
        super().__init__()
        # self.conn, self.cur = Pipeline.connect_db()

    def process_characteristics(self):
        '''
            Get all the information about the subject
            that isn't a measurement
        '''

        for characteristic in final_characteristics_list:
            
            characteristic_value = self.subject_row.get(characteristic, default=None)
            if 'date' in characteristic.lower() or 'exit day' in characteristic.lower():
                self.characteristics[characteristic] = self.format_date(characteristic_value)
            # Assign multiple values into list
            elif any(technician_col in characteristic.lower() for technician_col in ['collection']):
                # Checking the format of each column with comma-separated values for error
                # print(f'The characteristic is {characteristic}')
                # print(f'Characteristics value is {characteristic_value}')
                # print(f'Its type is {type(characteristic_value)}')
                self.characteristics[characteristic] = self.format_multiple_values_into_array(characteristic_value)
            else:
                self.characteristics[characteristic] = characteristic_value

    # def process_measurements(self):
    #     for measurement_dict in cocaine_measurements_list:
    
    #         counts = measurement_dict['counts']
    #         suffixes = measurement_dict['col_suffix']

    #         # Loop through each count of the measurement
    #         for i in range(1, counts+1):

    #             # Use default dict as we will need all access all values to insert into database
    #             insert_dict = defaultdict(lambda: None)
    #             col_name = measurement_dict['col_name']
    #             current_number = i

    #             insert_dict['name'] = measurement_dict['measurement_name']
    #             insert_dict['measure_number'] = current_number
                
    #             for suffix in suffixes:
    #                 # This is used to query for the value of a specific column referencing a measurement value for the current subject (row)
    #                 # TODO: Strip is to account for columns whose value that are denoted by empty str instead of 'Value'
    #                 full_col_name = ' '.join([col_name, str(current_number), suffix]).strip()                    

    #                 if suffix == 'Value':
    #                     insert_dict['value'] = self.subject_row[full_col_name]
    #                 elif suffix == 'By' or suffix == 'Collection':
    #                     insert_dict['technician'] = self.subject_row[full_col_name]
    #                 elif suffix == 'Date':
    #                     insert_dict['date_measured'] = self.subject_row[full_col_name]

    #             self.measurements.append(insert_dict)

    #     return 

    @staticmethod
    def format_date(date: datetime):
        '''
            Convert all date values into a consistent format. If the value is null, replace it with None
            for insertion into the database
        '''
        if pd.isnull(date):
            return None
        else:
            return datetime.strftime(date, "%m/%d/%Y %H:%M:%S")
    
    @staticmethod
    def format_multiple_values_into_array(comma_separated_string: str):
        '''
            Formats csv values into insertable format
        '''
        if not comma_separated_string or comma_separated_string.lower() == 'nan':
            return None

        css_formatted = ','.join([f'\"{value}\"' for value in comma_separated_string.split(',')])
        return f'{{{css_formatted}}}'

    def construct_characteristic_sql_string(self):
        values = ','.join(['%s'] * CHARACTERISTIC_TABLE_COLUMNS_COUNT)
        sql_string = f"""INSERT INTO {CHARACTERISTIC_TABLE_NAME} VALUES ({values}) ON CONFLICT (rfid) DO NOTHING;""" 
        sql_string_values = list([self.characteristics[key] for key in final_characteristics_list])
        for i in range(len(sql_string_values)):
            if sql_string_values[i] is not None and isinstance(sql_string_values[i], float):
                if math.isnan(sql_string_values[i]):
                    sql_string_values[i] = None
        return sql_string, sql_string_values

    def insert_characteristics(self):
        sql_string, sql_string_values = self.construct_characteristic_sql_string()
        # print(sql_string)
        # print(sql_string_values)
        # print(f'The value is {sql_string_values[-19]} with {type(sql_string_values[-19])}')
        # print(f'The value is {sql_string_values[-18]} with {type(sql_string_values[-18])}')
        # print(len(sql_string_values))
        self.cur.execute(sql_string, sql_string_values)
        self.cur.execute(f"SELECT * FROM {CHARACTERISTIC_TABLE_NAME};")
        self.conn.commit()
        self.cur.close()


        

    

