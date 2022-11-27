import math
from config import *
from collections import defaultdict
from pipeline import Pipeline

class OtherSubject(Pipeline):

    def __init__(self, subject_row, table_id):
        """initialize the subject and create a default dict for data

        Args:
            subject_row (_type_): a row of data
        """
        self.subject_row = subject_row
        self.table_id = table_id
        self.characteristics = defaultdict(lambda: None)
        super().__init__()

        if self.table_id == "VF":
            self.final_charactersitics_list = characteristics_VF
            self.table_to_insert = TABLE_VON_FREY
        if self.table_id == "TI":
            self.final_charactersitics_list = characteristics_TI
            self.table_to_insert = TABLE_TAIL_IMMERSION


    def process_characteristics(self):
        """store the row data into a default dict
        """
        for characteristic in self.final_charactersitics_list:
            characteristic_value = self.subject_row.get(characteristic, default=None)
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
