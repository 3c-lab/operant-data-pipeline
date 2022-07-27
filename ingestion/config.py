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

cocaine_measurements_list = [
    {'measurement_name': 'feces', 'measurement_col_name': 'Feces', 'measurement_counts': 4, 'measurement_col_suffix': ['Collection', 'Date']},
    {'measurement_name': 'female_swap', 'measurement_col_name': 'Female Swab', 'measurement_counts': 3, 'measurement_col_suffix': ['By', 'Date']},
    {'measurement_name': 'irritability', 'measurement_col_name': 'Irritability', 'measurement_counts': 2, 'measurement_col_suffix': ['By', 'Date']},
    {'measurement_name': 'progressive_ratio', 'measurement_col_name': 'Progressive Ratio', 'measurement_counts': 3, 'measurement_col_suffix': ['Date']},
    {'measurement_name': 'shock_1', 'measurement_col_name': 'Shock (0.1mA)', 'measurement_counts': 1, 'measurement_col_suffix': ['Date']},
    {'measurement_name': 'shock_2', 'measurement_col_name': 'Shock (0.2mA)', 'measurement_counts': 1, 'measurement_col_suffix': ['Date']},
    {'measurement_name': 'shock_3', 'measurement_col_name': 'Shock (0.3mA)', 'measurement_counts': 1, 'measurement_col_suffix': ['Date']},
    {'measurement_name': 'urine', 'measurement_col_name': 'Urine', 'measurement_counts': 1, 'measurement_col_suffix': ['Collection', 'Date']},
    {'measurement_name': 'weight', 'measurement_col_name': 'Weight', 'measurement_counts': 1, 'measurement_col_suffix': ['Date']},
    {'measurement_name': '', 'measurement_col_name': '', 'measurement_counts': 1, 'measurement_col_suffix': ['']},
    {'measurement_name': '', 'measurement_col_name': '', 'measurement_counts': 1, 'measurement_col_suffix': ['']},
    {'measurement_name': '', 'measurement_col_name': '', 'measurement_counts': 1, 'measurement_col_suffix': ['']},
]

oxycodone_characteristics_list = [

]

oxycodone_measurements_list = [
    {},
    {},
    {}
]


