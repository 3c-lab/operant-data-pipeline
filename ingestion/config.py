import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(dirname(__file__)), '.env')
load_dotenv(dotenv_path)

COCAINE_COHORT_07 = os.environ.get("COCAINE_7_FILEPATH")
COCAINE_COHORT_04 = os.environ.get("COCAINE_4_FILEPATH")
COCAINE_COHORT_ALL = [
                        os.environ.get("COCAINE_1_FILEPATH"), os.environ.get("COCAINE_2_FILEPATH"),
                        os.environ.get("COCAINE_3_FILEPATH"), os.environ.get("COCAINE_4_FILEPATH"),
                        os.environ.get("COCAINE_5_FILEPATH"), os.environ.get("COCAINE_7_FILEPATH"),
                        os.environ.get("COCAINE_8_FILEPATH"), os.environ.get("COCAINE_9_FILEPATH"),
                        os.environ.get("COCAINE_10_FILEPATH"), os.environ.get("COCAINE_11_FILEPATH"),
                        os.environ.get("COCAINE_13_FILEPATH"), os.environ.get("COCAINE_14_FILEPATH"),
                        os.environ.get("COCAINE_15_FILEPATH"), os.environ.get("COCAINE_16_FILEPATH"),
                        os.environ.get("COCAINE_17_FILEPATH"), os.environ.get("COCAINE_18_FILEPATH"),
                        os.environ.get("COCAINE_19_FILEPATH"), os.environ.get("COCAINE_20_FILEPATH")
                    ]
OXYCODONE_COHORT_ALL = [
                        os.environ.get("OXYCODONE_1_FILEPATH"), os.environ.get("OXYCODONE_3_FILEPATH"),
                        os.environ.get("OXYCODONE_4_FILEPATH"), os.environ.get("OXYCODONE_5_FILEPATH"),
                        os.environ.get("OXYCODONE_6_FILEPATH"), os.environ.get("OXYCODONE_7_FILEPATH"),
                        os.environ.get("OXYCODONE_9_FILEPATH"), os.environ.get("OXYCODONE_10_FILEPATH"),
                        os.environ.get("OXYCODONE_11_FILEPATH"), os.environ.get("OXYCODONE_12_FILEPATH"),
                        os.environ.get("OXYCODONE_13_FILEPATH"), os.environ.get("OXYCODONE_14_FILEPATH"),
                        os.environ.get("OXYCODONE_15_FILEPATH"), os.environ.get("OXYCODONE_16_FILEPATH"),
                        os.environ.get("OXYCODONE_17_FILEPATH")
                    ]
DATABASE_HOST = os.environ.get("DATABASE_HOST")
DATABASE_PORT = os.environ.get("DATABASE_PORT")
DATABASE_NAME = os.environ.get("DATABASE_NAME")
DATABASE_SCHEMA = os.environ.get("DATABASE_SCHEMA")
DATABASE_USERNAME = os.environ.get("DATABASE_USERNAME")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")

CHARACTERISTIC_TABLE_NAME = 'subject'
# MEASUREMENT_TABLE_COLUMNS_COUNT = len(final_measurements_list)

# These are all the columns that will be accessed for its value to be inserted into its respective column in the
# characteristic table
cocaine_characteristics_list = [
    'Rat', 'Experiment Group', 'Drug Group', 'Cohort', 'Sex', 'RFID', 'D.O.B', 'Date of Wean', 'Date of Ship',
    'Litter Number', 'Litter Size', 'Coat Color', 'Ear Punch',
    'Shipping Box', 'Rack', 'Arrival Date', 'Handled By', 'Surgery Date',
    'Surgeon', 'Surgery Assist', 'Date of Eye Bleed',
    'Short Access Start Date', 'Short Access End Date',
    'Long Access Start Date', 'Long Access End Date', 'LgA15 Date',
    'LgA16 Date', 'LgA17 Date', 'LgA18 Date', 'LgA19 Date', 'LgA20 Date',
    'Irritability 1 By', 'Irritability 1 Date', 'Irritability 2 By', 'Irritability 2 Date',
    'Progressive Ratio 1 Date', 'Progressive Ratio 2 Date', 'Progressive Ratio 3 Date'
    'Brevital', 'Brevital Date', 'Brevital By',
    'Pre-Shock Date', 'Shock (0.1mA) Date', 'Shock (0.2mA) Date',
    'Shock (0.3mA) Date', 'Group for Pre-Shock', 'Group for Shock',
    'Recatheter Surgeon', 'Recatheter Surgery Date',
    'Dissection', 'Dissection Date', 'Date of Death'

    # Saved for seoarate
    # 'Date Excluded', 'Exclude Reason'
]

oxycodone_characteristics_list = [
    'Rat', 'RFID', 'Cohort', 'Sex', 'D.O.B', 'Coat Color', 'Ear Punch', 'Shipping Box', 
    'Date of Wean', 'Date of Ship', 'Litter Number', 'Litter Size', 'Rack', 
    'Arrival Date', 'Age at Arrival', 'Handled Collection', 'Experiment Group', 'Drug Group', 
    'Surgery Date', 'Age at Surgery', 'Surgeon ', 'Surgery Assist', 'Date of Eye Bleed',
    'UV', 'Age at ShA', 'Short Access Start Date', 'Short Access End Date ',
    'Age at LgA', 'Long Access Start Date', 'Long Access End Date', 'Brevital Date', 'Brevital', 
    'Von Frey 1 Collection', 'Von Frey 1 Date', 'Von Frey 2 Collection', 'Von Frey 2 Date',
    'Tail Immersion 1 Collection', 'Tail Immersion 1 Date', 'Tail Immersion 2 Collection', 'Tail Immersion 2 Date', 'Tail Immersion 3 Collection', 'Tail Immersion 3 Date',
    'Progressive Ratio 1 Date', 'Progressive Ratio 2 Date', 'LgA Pre-Treatment 1 Date', 'LgA Pre-Treatment 2 Date',
    'LgA Pre-Treatment 3 Date', 'LgA Pre-Treatment 4 Date', 'LgA Post-Treatment 1 Date', 'LgA Post-Treatment 2 Date', 
    'LgA Post-Treatment 3 Date', 'LgA Pre-Treatment 4 Date',
    'Treatment 1 Date', 'Treatment 1 Group', 'Treatment 1 Start Time',
    'Treatment 2 Date', 'Treatment 2 Group', 'Treatment 2 Start Time', 'Treatment 3 Date', 'Treatment 3 Group', 'Treatment 3 Start Time',
    'Age at Dissection', 'Dissection Date', 'Dissection Group', 'Date of Death', 'Days of Experiment'
    # Save for separate
    # 'Days of Experiment', 'Reason for Removal from Study', 'Was Replaced', 'Replaced', 'Last Session'
]

oxycodone_measurements_list = [
    {'measurement_name': 'urine', 'col_name': 'Urine', 'counts': [i for i in range(1, 3)], 'col_suffix': ['Date', 'By']},
    {'measurement_name': 'female_swab', 'col_name': 'Female Swab', 'counts': [i for i in range(1, 4)], 'col_suffix': ['Date', 'By', 'Analysis']},
    {'measurement_name': 'weight', 'col_name': 'Weight', 'counts': [i for i in range(1, 13)], 'col_suffix': ['Value', 'Date']},
    {'measurement_name': 'feces', 'col_name': 'Feces', 'counts': [i for i in range(1, 4)], 'col_suffix': ['Date', 'By']},
]

exit_tab_list = [
    'exit day', 'last good session', 'exit code', 'complete', 'tissue collected', 'exit notes', 'replaced by'
]

# Union of characteristics from Cocaine and Oxycodone
final_charactersitics_list = [
    'rfid', 'rat', 'cohort', 'experiment group', 'drug group', 'sex', 'arrival date', 'age at arrival', 'uv', 'brevital', 'brevital date', 'brevital collection', 'lga15 date',
    'lga16 date', 'lga17 date', 'lga18 date', 'lga19 date', 'lga20 date', 'age at lga', 'long access start date', 'long access end date', 'age at sha', 'short access start date',
    'short access end date', 'pre-shock date', 'shock (0.1ma) date', 'shock (0.2ma) date', 'shock (0.3ma) date', 'irritability 1 collection', 'irritability 1 date', 'irritability 2 collection', 
    'irritability 2 date',  'von frey 1 collection', 'von frey 1 date', 'von frey 2 collection', 'von frey 2 date',
    'tail immersion 1 collection', 'tail immersion 1 date', 'tail immersion 2 collection', 'tail immersion 2 date', 'tail immersion 3 collection', 'tail immersion 3 date', 'lga pre-treatment 1 date', 'lga pre-treatment 2 date', 
    'lga pre-treatment 3 date', 'lga pre-treatment 4 date', 'lga post treatment 1', 'lga post treatment 2', 'lga post treatment 3', 'lga post treatment 4', 'progressive ratio 1 date', 'progressive ratio 2 date', 'progressive ratio 3 date', 
    'treatment 1 date', 'treatment 1 group', 'treatment 1 start time', 'treatment 2 date', 'treatment 2 group', 'treatment 2 start time', 'treatment 3 date', 'treatment 3 group', 'treatment 3 start time',
    'coat color', 'd.o.b', 'date of eye bleed', 'date of ship', 'date of wean', 'age at dissection', 'dissection group', 'dissection date', 'ear punch', 'group for pre-shock',
    'group for shock', 'handled collection', 'litter number', 'litter size', 'rack', 'recatheter surgeon', 'recatheter surgery date', 'shipping box', 'surgeon', 'surgery assist', 'surgery date',
    'age at surgery', 'date of death', 'days of experiment', 'exit day', 'last good session', 'exit code', 'complete', 'tissue collected', 'exit notes', 'replaced by'
]

CHARACTERISTIC_TABLE_COLUMNS_COUNT = len(final_charactersitics_list)







