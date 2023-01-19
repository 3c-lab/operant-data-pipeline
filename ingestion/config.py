import os
import pandas as pd
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(dirname(__file__)), '.env')
load_dotenv(dotenv_path)

# TRIAL_LGA_TEST = ["/Users/yunyihuang/Desktop/gl_data/TRIAL/COC_LGA/BSB273BC08HSLGA01_transformed.csv"]

# TRIAL_SHA_TEST = ['/Users/yunyihuang/Desktop/gl_data/TRIAL/COC_SHA/BSB273BC08HSSHA02_transformed.csv',
#                   '/Users/yunyihuang/Desktop/gl_data/TRIAL/COC_SHA/BSB273BC08HSSHA03_transformed.csv',]

# TRIAL_PR_TEST = ['/Users/yunyihuang/Desktop/gl_data/TRIAL/COC_PR/BSB273BC08HSPR01_transformed.csv',
#                  '/Users/yunyihuang/Desktop/gl_data/TRIAL/OXY_PR/BSB273BC04HSOXYPR01_transformed.csv',]

# TRIAL_SHOCK_TEST = ['/Users/yunyihuang/Desktop/gl_data/TRIAL/COC_SHOCK/BSB273BC08HSSHOCK_transformed.csv',
#                     '/Users/yunyihuang/Desktop/gl_data/TRIAL/COC_SHOCK/BSB273BC08HSSHOCK-1_transformed.csv']

# TAIL_IMMERSION_PATH = '/Users/yunyihuang/Desktop/gl_data/Cleaned_Tail_Immersion'
# TAIL_IMMERSION_FILES = [os.path.join(TAIL_IMMERSION_PATH, i) for i in sorted(os.listdir(TAIL_IMMERSION_PATH)) if (i != '.DS_Store')]

# VON_FREY_PATH = '/Users/yunyihuang/Desktop/gl_data/Cleaned_Von_Frey'
# VON_FREY_FILES = [os.path.join(VON_FREY_PATH, i) for i in sorted(os.listdir(VON_FREY_PATH)) if (i != '.DS_Store')]

# DATABASE_HOST = "localhost"
# DATABASE_PORT = "1192"
# DATABASE_NAME = "testDS"
# DATABASE_SCHEMA = "public"
# DATABASE_USERNAME = "postgres"
# DATABASE_PASSWORD = "Gareth1192!"

TABLE_TRIAL_LGA = 'trial_lga'
TABLE_TRIAL_SHA = 'trial_sha'
TABLE_TRIAL_PR = 'trial_pr'
TABLE_TRIAL_SHOCK = 'trial_shock'
TABLE_TAIL_IMMERSION = 'tail_immersion'
TABLE_VON_FREY = 'von_frey'

# characteristics for TRIAL LGA, SHA data
characteristics_LGA_SHA = ['rfid','subject','room','cohort','trial_id','drug','box', 'start_time', 'end_time',
 'start_date','end_date','active_lever_presses','inactive_lever_presses','reward_presses','timeout_presses',
 'active_timestamps','inactive_timestamps','reward_timestamps','timeout_timestamps']

# characteristics for TRIAL PR data
characteristics_PR = ['rfid', 'subject', 'room', 'cohort', 'trial_id', 'drug', 'box','start_time', 'end_time', 
 'start_date', 'end_date', 'last_ratio', 'breakpoint', 'active_lever_presses', 'inactive_lever_presses',
 'reward_presses', 'reward_points']

# characteristics for TRIAL SHOCK data
characteristics_SHOCK = ['rfid', 'subject', 'room', 'cohort', 'trial_id', 'drug', 'box',
       'start_time', 'end_time', 'start_date', 'end_date',
       'total_active_lever_presses', 'total_inactive_lever_presses',
       'total_shocks', 'total_reward', 'rewards_after_first_shock',
       'rewards_got_shock', 'reward_timestamps']

# characteristics for TAIL IMMERSION data
characteristics_TI = ['rfid', 'subject', 'cohort', 'sex', 'experiment_group', 'drug', 'tail_immersion_1_time', 
    'tail_immersion_2_time','tail_immersion_3_time', 'tail_immersion_difference_tolerance',
    'tail_immersion_1_date', 'tail_immersion_2_date','tail_immersion_3_date']

# characteristics for VON FREY data
characteristics_VF = ['rfid', 'subject', 'cohort', 'sex', 'experiment_group', 'drug',
                        'vf1_right_force_1', 'vf1_right_force_2', 'vf1_right_force_3',
                        'vf1_right_force_avg', 'vf1_right_time_1', 'vf1_right_time_2',
                        'vf1_right_time_3', 'vf1_right_avg', 'vf1_left_force_1',
                        'vf1_left_force_2', 'vf1_left_force_3', 'vf1_left_force_avg',
                        'vf1_left_time_1', 'vf1_left_time_2', 'vf1_left_time_3', 'vf1_left_avg',
                        'von_frey_1_date', 'vf2_right_force_1', 'vf2_right_force_2',
                        'vf2_right_force_3', 'vf2_right_force_avg', 'vf2_right_time_1',
                        'vf2_right_time_2', 'vf2_right_time_3', 'vf2_right_avg',
                        'vf2_left_force_1', 'vf2_left_force_2', 'vf2_left_force_3',
                        'vf2_left_force_avg', 'vf2_left_time_1', 'vf2_left_time_2',
                        'vf2_left_time_3', 'vf2_left_avg', 'von_frey_2_date',
                        'von_frey_1_force', 'von_frey_1_time', 'von_frey_2_force',
                        'von_frey_2_time', 'von_frey_difference_force']

integer_columns = ['rfid','cohort','box','active_lever_presses','inactive_lever_presses','reward_presses','timeout_presses',
                   'last_ratio', 'breakpoint', 'total_active_lever_presses', 'total_inactive_lever_presses',
                   'total_shocks', 'total_reward', 'rewards_after_first_shock']

COCAINE_COHORT_07 = os.environ.get("COCAINE_7_FILEPATH")
COCAINE_COHORT_04 = os.environ.get("COCAINE_4_FILEPATH")
COCAINE_COHORT_18 = os.environ.get("COCAINE_18_FILEPATH")
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
                        os.environ.get("OXYCODONE_17_FILEPATH"), os.environ.get("OXYCODONE_18_FILEPATH")
                    ]
DATABASE_HOST = os.environ.get("A_DATABASE_HOST")
DATABASE_PORT = os.environ.get("A_DATABASE_PORT")
DATABASE_NAME = os.environ.get("A_DATABASE_NAME")
DATABASE_SCHEMA = os.environ.get("A_DATABASE_SCHEMA")
DATABASE_USERNAME = os.environ.get("A_DATABASE_USERNAME")
DATABASE_PASSWORD = os.environ.get("A_DATABASE_PASSWORD")

CHARACTERISTIC_TABLE_NAME = 'subject'
MEASUREMENT_TABLE_NAME = 'measurement'
# These are all the columns that will be accessed for its value to be inserted into its respective column in the
# characteristic table
cocaine_characteristics_list = [
    'Rat', 'Experiment Group', 'Drug Group', 'Cohort', 'Sex', 'RFID', 'D.O.B', 'Date of Wean', 'Date of Ship',
    'Litter Number', 'Litter Size', 'Coat Color', 'Ear Punch',
    'Shipping Box', 'Rack', 'Arrival Date', 'Handled Collection', 'Surgery Date',
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

cocaine_measurements_list = [
    {'measurement_name': 'urine', 'col_name': 'Urine', 'counts': [i for i in range(1, 3)], 'col_suffix': ['Date', 'Collection']},
    {'measurement_name': 'weight', 'col_name': 'Weight', 'counts': [i for i in range(1, 11)], 'col_suffix': ['Value', 'Date']},
    {'measurement_name': 'feces', 'col_name': 'Feces', 'counts': [i for i in range(1, 5)], 'col_suffix': ['Date', 'Collection']},
]

cocaine_excel_converters = {
    'Rat': str, 
    'Experiment Group': str, 
    'Drug Group': str, 
    'Cohort': int, # int
    'Sex': str, 
    'RFID': str, 
    'D.O.B': pd.Timestamp, 
    'Date of Wean': pd.Timestamp, 
    'Date of Ship': pd.Timestamp,
    'Litter Number': int, 
    'Litter Size': int, 
    'Coat Color': str, 
    'Ear Punch': str,
    'Shipping Box': str, 
    'Rack': str, 
    'Arrival Date': pd.Timestamp, 
    'Handled Collection': str, 
    'Surgery Date': pd.Timestamp,
    'Surgeon': str, 
    'Surgery Assist': str, 
    'Date of Eye Bleed': pd.Timestamp,
    'Short Access Start Date': pd.Timestamp, 
    'Short Access End Date': pd.Timestamp,
    'Long Access Start Date': pd.Timestamp, 
    'Long Access End Date': pd.Timestamp, 
    'LgA15 Date': pd.Timestamp,
    'LgA16 Date': pd.Timestamp, 
    'LgA17 Date': pd.Timestamp, 
    'LgA18 Date': pd.Timestamp, 
    'LgA19 Date': pd.Timestamp, 
    'LgA20 Date': pd.Timestamp,
    'Irritability 1 Collection': str, 
    'Irritability 1 Date': pd.Timestamp, 
    'Irritability 2 Collection': str, 
    'Irritability 2 Date': pd.Timestamp,
    'Progressive Ratio 1 Date': pd.Timestamp, 
    'Progressive Ratio 2 Date': pd.Timestamp, 
    'Progressive Ratio 3 Date': pd.Timestamp,
    'Brevital': str, # Pass/Fail 
    'Brevital Date': pd.Timestamp, 
    'Brevital Collection': str,
    'Pre-Shock Date': pd.Timestamp, 
    'Shock (0.1mA) Date': pd.Timestamp, 
    'Shock (0.2mA) Date': pd.Timestamp,
    'Shock (0.3mA) Date': pd.Timestamp, 
    'Group for Pre-Shock': int, 
    'Group for Shock': int,
    'Recatheter Surgeon': str, 
    'Recatheter Surgery Date': pd.Timestamp,
    'Dissection': str, 
    'Dissection Date': pd.Timestamp, 
    'Date of Death': pd.Timestamp
}

oxycodone_excel_converters = {
    'Rat': str, 
    'RFID': str, 
    'Cohort': int, # int
    'Sex': str, 
    'D.O.B': pd.Timestamp, 
    'Coat Color': str, 
    'Ear Punch': str, 
    'Shipping Box': str, 
    'Date of Wean': pd.Timestamp, 
    'Date of Ship': pd.Timestamp, 
    'Litter Number': int, # int
    'Litter Size': int, # int
    'Rack': str, 
    'Arrival Date': pd.Timestamp, 
    'Age at Arrival': int, # int
    'Handled Collection': str, 
    'Experiment Group': str, 
    'Drug Group': str, 
    'Surgery Date': pd.Timestamp, 
    'Age at Surgery': int, # int
    'Surgeon': str, 
    'Surgery Assist': str, 
    'Date of Eye Bleed': pd.Timestamp,
    'UV': str, 
    'Age at ShA': int, # int
    'Short Access Start Date': pd.Timestamp, 
    'Short Access End Date': pd.Timestamp,
    'Age at LgA': int, # int
    'Long Access Start Date': pd.Timestamp, 
    'Long Access End Date': pd.Timestamp, 
    'Brevital Date': pd.Timestamp, 
    'Brevital': str, 
    'Von Frey 1 Collection': str, 
    'Von Frey 1 Date': pd.Timestamp, 
    'Von Frey 2 Collection': str, 
    'Von Frey 2 Date': pd.Timestamp,
    'Tail Immersion 1 Collection': str, 
    'Tail Immersion 1 Date': pd.Timestamp, 
    'Tail Immersion 2 Collection': str, 
    'Tail Immersion 2 Date': pd.Timestamp, 
    'Tail Immersion 3 Collection': str, 
    'Tail Immersion 3 Date': pd.Timestamp,
    'Progressive Ratio 1 Date': pd.Timestamp, 
    'Progressive Ratio 2 Date': pd.Timestamp, 
    'LgA Pre-Treatment 1 Date': pd.Timestamp, 
    'LgA Pre-Treatment 2 Date': pd.Timestamp,
    'LgA Pre-Treatment 3 Date': pd.Timestamp, 
    'LgA Pre-Treatment 4 Date': pd.Timestamp, 
    'LgA Post-Treatment 1 Date': pd.Timestamp, 
    'LgA Post-Treatment 2 Date': pd.Timestamp, 
    'LgA Post-Treatment 3 Date': pd.Timestamp, 
    'LgA Pre-Treatment 4 Date': pd.Timestamp,
    'Treatment 1 Date': pd.Timestamp, 
    'Treatment 1 Group': str, 
    'Treatment 1 Start Time': str, # Currently stored as string. Ideally as time format
    'Treatment 2 Date': pd.Timestamp,
    'Treatment 2 Group': str,
    'Treatment 2 Start Time': str,
    'Treatment 3 Date': pd.Timestamp,
    'Treatment 3 Group': str,
    'Treatment 3 Start Time': str,
    'Age at Dissection': int, # int 
    'Dissection Date': pd.Timestamp, 
    'Dissection Group': str, 
    'Date of Death': pd.Timestamp, 
    # 'Days of Experiment': int
    # Save for separate
    # 'Days of Experiment', 'Reason for Removal from Study', 'Was Replaced', 'Replaced', 'Last Session'
}

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
    {'measurement_name': 'urine', 'col_name': 'Urine', 'counts': [i for i in range(1, 3)], 'col_suffix': ['Date', 'Collection']},
    {'measurement_name': 'weight', 'col_name': 'Weight', 'counts': [i for i in range(1, 13)], 'col_suffix': ['Value', 'Date']},
    {'measurement_name': 'feces', 'col_name': 'Feces', 'counts': [i for i in range(1, 4)], 'col_suffix': ['Date', 'Collection']},
]

exit_tab_list = [
    'exit day', 'last good session', 'exit code', 'complete', 'tissue collected', 'exit notes', 'replaced by'
]

# Union of characteristics from Cocaine and Oxycodone
final_characteristics_list = [
    'rfid', 'rat', 'cohort', 'experiment group', 'drug group', 'sex', 'arrival date', 'age at arrival', 'uv', 'brevital', 'brevital date', 'brevital collection', 'lga15 date',
    'lga16 date', 'lga17 date', 'lga18 date', 'lga19 date', 'lga20 date', 'age at lga', 'long access start date', 'long access end date', 'age at sha', 'short access start date',
    'short access end date', 'pre-shock date', 'shock (0.1ma) date', 'shock (0.2ma) date', 'shock (0.3ma) date',
    'female swab 1 collection', 'female swab 1 date', 'female swab 1 analysis', 'female swab 2 collection', 'female swab 2 date', 'female swab 2 analysis', 'female swab 3 collection', 'female swab 3 date', 'female swab 3 analysis',
    'irritability 1 collection', 'irritability 1 date', 'irritability 2 collection', 'irritability 2 date',  'von frey 1 collection', 'von frey 1 date', 'von frey 2 collection', 'von frey 2 date',
    'tail immersion 1 collection', 'tail immersion 1 date', 'tail immersion 2 collection', 'tail immersion 2 date', 'tail immersion 3 collection', 'tail immersion 3 date', 'lga pre-treatment 1 date', 'lga pre-treatment 2 date', 
    'lga pre-treatment 3 date', 'lga pre-treatment 4 date', 'lga post treatment 1 date', 'lga post treatment 2 date', 'lga post treatment 3 date', 'lga post treatment 4 date', 'progressive ratio 1 date', 'progressive ratio 2 date', 'progressive ratio 3 date', 
    'treatment 1 date', 'treatment 1 group', 'treatment 1 start time', 'treatment 2 date', 'treatment 2 group', 'treatment 2 start time', 'treatment 3 date', 'treatment 3 group', 'treatment 3 start time',
    'treatment 4 date', 'treatment 4 group', 'treatment 4 start time' , 'coat color', 'd.o.b', 'date of eye bleed', 'date of ship', 'date of wean', 'age at dissection', 'dissection group', 'dissection date', 'ear punch', 'group for pre-shock',
    'group for shock', 'handled collection', 'litter number', 'litter size', 'rack', 'recatheter surgeon', 'recatheter surgery date', 'shipping box', 'surgeon', 'surgery assist', 'surgery date',
    'age at surgery', 'date of death', 'days of experiment', 'exit day', 'last good session', 'exit code', 'complete', 'tissue collected', 'exit notes', 'replaced by'
]

measurement_table_cols = [
    'rfid', 'measurement_name', 'measurement_value', 'drug_group', 'cohort', 'measure_number', 'date_measured', 'technician'
]

CHARACTERISTIC_TABLE_COLUMNS_COUNT = len(final_characteristics_list)