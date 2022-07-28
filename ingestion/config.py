import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(dirname(__file__)), '.env')
load_dotenv(dotenv_path)

COCAINE_COHORT_07 = os.environ.get("COCAINE_7_FILEPATH")
DATABASE_HOST = os.environ.get("DATABASE_HOST")
DATABASE_PORT = os.environ.get("DATABASE_PORT")
DATABASE_NAME = os.environ.get("DATABASE_NAME")
DATABASE_USERNAME = os.environ.get("DATABASE_USERNAME")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")

CHARACTERISTIC_TABLE_NAME = 'datastream.subject'
CHARACTERISTIC_TABLE_COLUMNS_COUNT = 38
MEASUREMENT_TABLE_COLUMNS_COUNT = 6

# These are all the columns that will be accessed for its value to be inserted into its respective column in the
# characteristic table
cocaine_characteristics_list = [
    'RFID', 'RAT', 'Arrival Date', 'Brevital', 'Brevital Date', 'Brevital Done By', 'LgA15 Date',
    'LgA16 Date', 'LgA17 Date', 'LgA18 Date', 'Long Access Start Date',
    'Long Access End Date', 'Short Access Start Date', 'Short Access End Date',
    'Pre-Shock Date', 'Shock (0.1mA) Date', 'Shock (0.2mA) Date', 'Shock (0.3mA) Date',
    'Coat Color', 'Date of Birth', 'Date of Eye Bleed', 'Date of Ship', 'Date of Wean',
    'Dissection Date', 'Ear Punch', 'Group for Pre-Shock', 'Group for Shock', 'Handled By',
    'Litter Number', 'Litter Size', 'Rack', 'Recatheter Surgeon', 'Recatheter Surgery Date',
    'Shipping Box', 'Surgeon', 'Surgery Assist', 'Surgery Date', 'Date of Death'
]

'''
    - col_name refers name
    - Collection refers to value
    - Date refers to date_measured
    - By refers to technician
    - counts refers to measure_number
'''

# From the master tample, these are the known columns that are classified as measurements. 
# Also denoted is the number of instances of the measurement. 
# col_suffix is used to get other information about that instance of measurement
cocaine_measurements_list = [
    {'measurement_name': 'feces', 'col_name': 'Feces', 'counts': 4, 'col_suffix': ['Collection', 'Date']},
    {'measurement_name': 'female_swap', 'col_name': 'Female Swab', 'counts': 3, 'col_suffix': ['By', 'Date']},
    {'measurement_name': 'irritability', 'col_name': 'Irritability', 'counts': 2, 'col_suffix': ['By', 'Date']},
    {'measurement_name': 'progressive_ratio', 'col_name': 'Progressive Ratio', 'counts': 3, 'col_suffix': ['Date']},
    {'measurement_name': 'urine', 'col_name': 'Urine', 'counts': 1, 'col_suffix': ['Collection', 'Date']},
    {'measurement_name': 'weight', 'col_name': 'Weight', 'counts': 10, 'col_suffix': ['', 'Date']}
]

oxycodone_characteristics_list = [

]

oxycodone_measurements_list = [

]


