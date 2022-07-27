import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

COCAINE_COHORT_07 = os.environ.get("COCAINE_7_FILEPATH")
DATABASE_USERNAME = os.environ.get("DATABASE_USERNAME")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")


cocaine_characteristics_list = [

]

'''
    - col_name refers name
    - Collection refers to value
    - Date refers to date_measured
    - By refers to technician
    - counts refers to measure_number
'''

cocaine_measurements_list = [
    {'measurement_name': 'feces', 'col_name': 'Feces', 'counts': 4, 'col_suffix': ['Collection', 'Date']},
    {'measurement_name': 'female_swap', 'col_name': 'Female Swab', 'counts': 3, 'col_suffix': ['By', 'Date']},
    {'measurement_name': 'irritability', 'col_name': 'Irritability', 'counts': 2, 'col_suffix': ['By', 'Date']},
    {'measurement_name': 'progressive_ratio', 'col_name': 'Progressive Ratio', 'counts': 3, 'col_suffix': ['Date']},
    {'measurement_name': 'shock_1', 'col_name': 'Shock (0.1mA)', 'counts': 1, 'col_suffix': ['Date']},
    {'measurement_name': 'shock_2', 'col_name': 'Shock (0.2mA)', 'counts': 1, 'col_suffix': ['Date']},
    {'measurement_name': 'shock_3', 'col_name': 'Shock (0.3mA)', 'counts': 1, 'col_suffix': ['Date']},
    {'measurement_name': 'urine', 'col_name': 'Urine', 'counts': 1, 'col_suffix': ['Collection', 'Date']},
    {'measurement_name': 'weight', 'col_name': 'Weight', 'counts': 1, 'col_suffix': ['Date']}
]

oxycodone_characteristics_list = [

]

oxycodone_measurements_list = [

]


