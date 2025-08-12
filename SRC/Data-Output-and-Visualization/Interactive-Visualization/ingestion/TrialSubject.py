import math
import numpy as np
from config import *
from collections import defaultdict
from pipeline import Pipeline
from ast import literal_eval

class TrialSubject(Pipeline):

    def __init__(self, subject_row, table_id):
        """initialize the subject and create a default dict for data

        Args:
            subject_row (_type_): a row of data
        """
        self.subject_row = subject_row
        self.table_id = table_id
        self.characteristics = defaultdict(lambda: None)
        super().__init__()

        if self.table_id == "LGA":
            self.final_charactersitics_list = characteristics_LGA_SHA
            self.table_to_insert = TABLE_TRIAL_LGA
        if self.table_id == "SHA":
            self.final_charactersitics_list = characteristics_LGA_SHA
            self.table_to_insert = TABLE_TRIAL_SHA
        if self.table_id == "PR":
            self.final_charactersitics_list = characteristics_PR
            self.table_to_insert = TABLE_TRIAL_PR
        if self.table_id == "SHOCK":
            self.final_charactersitics_list = characteristics_SHOCK
            self.table_to_insert = TABLE_TRIAL_SHOCK
        if self.table_id == "NOTE":
            self.final_charactersitics_list = characteristics_NOTE
            self.table_to_insert = TABLE_TRIAL_NOTE
        if self.table_id == "VF":
            self.final_charactersitics_list = characteristics_VF
            self.table_to_insert = TABLE_VON_FREY
        if self.table_id == "TI":
            self.final_charactersitics_list = characteristics_TI
            self.table_to_insert = TABLE_TAIL_IMMERSION


    def serialize_timestamps(self, string_of_timestamps):
        """helper function to serialize list type data 

        Args:
            string_of_timestamps (_string_): timestamps data in subject_row
                                            that were converted to strings

        Returns:
            _string_: serialized timestamps data
        """

        timestamp_list = literal_eval(string_of_timestamps)

        # if timestamp_list is empty
        if len(timestamp_list) == 0:
            return "N/A"
        # if timestamp_list has nested lists
        while type(timestamp_list[-1]) == list:
            timestamp_list.pop()
        # if timestamp_list contains all zeros
        if sum(timestamp_list) == 0:
            return "N/A"
        # Strip the ending zeros
        while timestamp_list[-1] == 0:
            timestamp_list.pop()
        # Serialize the timestamps
        lst_strings = [str(i) for i in timestamp_list]
        return " ".join(lst_strings)


    def process_characteristics(self):
        """store the row data into a default dict
        """
        for characteristic in self.final_charactersitics_list:
            characteristic_value = self.subject_row.get(characteristic, default=None)
            if characteristic_value is not None and isinstance(characteristic_value, float) and np.isnan(characteristic_value):
                self.characteristics[characteristic] = None
            elif characteristic_value is None:
                self.characteristics[characteristic] = None
            elif (("timestamps" in characteristic.lower()) or (characteristic.lower() in ['ratios', 'rewards_got_shock'])): 
                # columns that contain list data
                self.characteristics[characteristic] = self.serialize_timestamps(characteristic_value)
            else: 
                # columns that contain 1 value per cell
                self.characteristics[characteristic] = characteristic_value


    def construct_characteristic_sql_string(self):
        values = ','.join(['%s'] * len(self.final_charactersitics_list))
        sql_string = f"""INSERT INTO {self.table_to_insert} VALUES ({values});""" 
        sql_string_values = list([self.characteristics[key] for key in self.final_charactersitics_list])
        for i in range(len(sql_string_values)):
            if sql_string_values[i] is not None and isinstance(sql_string_values[i], float):
                if math.isnan(sql_string_values[i]):
                    sql_string_values[i] = None
        return sql_string, sql_string_values


    def insert_characteristics(self):
        """insert data into the database
        """
        sql_string, sql_string_values = self.construct_characteristic_sql_string()
        #print(sql_string)
        #print(sql_string_values)
        self.cur.execute(sql_string, sql_string_values)
        self.cur.execute(f"SELECT * FROM {self.table_to_insert};")
        self.conn.commit()
        self.cur.close()
