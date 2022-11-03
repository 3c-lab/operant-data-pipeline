import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(dirname(__file__)), '.env')
load_dotenv(dotenv_path)

TRIAL_LGA_TEST = ["/Users/yunyihuang/Desktop/gl_data/TRIAL/COC_LGA/BSB273BC08HSLGA01_transformed.csv"]

TRIAL_SHA_TEST = ['/Users/yunyihuang/Desktop/gl_data/TRIAL/COC_SHA/BSB273BC08HSSHA02_transformed.csv',
                  '/Users/yunyihuang/Desktop/gl_data/TRIAL/COC_SHA/BSB273BC08HSSHA03_transformed.csv',]

TRIAL_PR_TEST = ['/Users/yunyihuang/Desktop/gl_data/TRIAL/COC_PR/BSB273BC08HSPR01_transformed.csv',
                 '/Users/yunyihuang/Desktop/gl_data/TRIAL/OXY_PR/BSB273BC04HSOXYPR01_transformed.csv',]

TRIAL_SHOCK_TEST = ['/Users/yunyihuang/Desktop/gl_data/TRIAL/COC_SHOCK/BSB273BC08HSSHOCK_transformed.csv',
                    '/Users/yunyihuang/Desktop/gl_data/TRIAL/COC_SHOCK/BSB273BC08HSSHOCK-1_transformed.csv']

TAIL_IMMERSION_PATH = '/Users/yunyihuang/Desktop/gl_data/Cleaned_Tail_Immersion'
TAIL_IMMERSION_FILES = [os.path.join(TAIL_IMMERSION_PATH, i) for i in sorted(os.listdir(TAIL_IMMERSION_PATH)) if (i != '.DS_Store')]

DATABASE_HOST = "localhost"
DATABASE_PORT = "1192"
DATABASE_NAME = "testDS"
DATABASE_SCHEMA = "public"
DATABASE_USERNAME = "postgres"
DATABASE_PASSWORD = "Gareth1192!"

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
characteristics_VF = []

integer_columns = ['rfid','cohort','box','active_lever_presses','inactive_lever_presses','reward_presses','timeout_presses',
                   'last_ratio', 'breakpoint', 'total_active_lever_presses', 'total_inactive_lever_presses',
                   'total_shocks', 'total_reward', 'rewards_after_first_shock']



