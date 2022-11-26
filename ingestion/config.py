import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(dirname(__file__)), '.env')
load_dotenv(dotenv_path)

# Test filenames
TRIAL_LGA_PATH_A = '/Users/yunyihuang/Desktop/gl_data/TRIAL/COC_LGA'
TRIAL_LGA_PATH_B = '/Users/yunyihuang/Desktop/gl_data/TRIAL/OXY_LGA'
TRIAL_LGA_TEST = ["/Users/yunyihuang/Desktop/gl_data/TRIAL/COC_LGA/BSB273BC08HSLGA01_transformed.csv"]
TRIAL_LGA_FILES = (
    #[os.path.join(TRIAL_LGA_PATH_A, i) for i in sorted(os.listdir(TRIAL_LGA_PATH_A)) if (i != '.DS_Store')] + 
    [os.path.join(TRIAL_LGA_PATH_B, i) for i in sorted(os.listdir(TRIAL_LGA_PATH_B)) if (i != '.DS_Store')]
)

TRIAL_SHA_PATH_A = '/Users/yunyihuang/Desktop/gl_data/TRIAL/COC_SHA'
TRIAL_SHA_PATH_B = '/Users/yunyihuang/Desktop/gl_data/TRIAL/OXY_SHA'
TRIAL_SHA_TEST = ['/Users/yunyihuang/Desktop/gl_data/TRIAL/COC_SHA/BSB273BC08HSSHA02_transformed.csv',
                  '/Users/yunyihuang/Desktop/gl_data/TRIAL/COC_SHA/BSB273BC08HSSHA03_transformed.csv',]
TRIAL_SHA_FILES = (
    [os.path.join(TRIAL_SHA_PATH_A, i) for i in sorted(os.listdir(TRIAL_SHA_PATH_A)) if (i != '.DS_Store')] + 
    [os.path.join(TRIAL_SHA_PATH_B, i) for i in sorted(os.listdir(TRIAL_SHA_PATH_B)) if (i != '.DS_Store')]
)

TRIAL_PR_PATH_A = '/Users/yunyihuang/Desktop/gl_data/TRIAL/COC_PR'
TRIAL_PR_PATH_B = '/Users/yunyihuang/Desktop/gl_data/TRIAL/OXY_PR'
TRIAL_PR_TEST = ['/Users/yunyihuang/Desktop/gl_data/TRIAL/COC_PR/BSB273BC08HSPR01_transformed.csv',
                 '/Users/yunyihuang/Desktop/gl_data/TRIAL/OXY_PR/BSB273BC04HSOXYPR01_transformed.csv',]
TRIAL_PR_FILES = (
    [os.path.join(TRIAL_PR_PATH_A, i) for i in sorted(os.listdir(TRIAL_PR_PATH_A)) if (i != '.DS_Store')] + 
    [os.path.join(TRIAL_PR_PATH_B, i) for i in sorted(os.listdir(TRIAL_PR_PATH_B)) if (i != '.DS_Store')]
)

TRIAL_SHOCK_PATH = '/Users/yunyihuang/Desktop/gl_data/TRIAL/COC_SHOCK'
TRIAL_SHOCK_TEST = ['/Users/yunyihuang/Desktop/gl_data/TRIAL/COC_SHOCK/BSB273BC08HSSHOCK_transformed.csv',
                    '/Users/yunyihuang/Desktop/gl_data/TRIAL/COC_SHOCK/BSB273BC08HSSHOCK-1_transformed.csv']
TRIAL_SHOCK_FILES = [os.path.join(TRIAL_SHOCK_PATH, i) for i in sorted(os.listdir(TRIAL_SHOCK_PATH)) if (i != '.DS_Store')]

TRIAL_NOTE_PATH = '/Users/yunyihuang/Desktop/gl_data/Cleaned_Note'
TRIAL_NOTE_FILES = [os.path.join(TRIAL_NOTE_PATH, i) for i in sorted(os.listdir(TRIAL_NOTE_PATH)) if (i != '.DS_Store')]

TAIL_IMMERSION_PATH = '/Users/yunyihuang/Desktop/gl_data/Cleaned_Tail_Immersion'
TAIL_IMMERSION_FILES = [os.path.join(TAIL_IMMERSION_PATH, i) for i in sorted(os.listdir(TAIL_IMMERSION_PATH)) if (i != '.DS_Store')]

VON_FREY_PATH = '/Users/yunyihuang/Desktop/gl_data/Cleaned_Von_Frey'
VON_FREY_FILES = [os.path.join(VON_FREY_PATH, i) for i in sorted(os.listdir(VON_FREY_PATH)) if (i != '.DS_Store')]

# database information
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
TABLE_TRIAL_NOTE = 'trial_note'
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

# characteristics for TRIAL NOTE data 
characteristics_NOTE = ['rfid', 'subject', 'cohort', 'sex', 'drug', 'experiment_group',
       'trial_id', 'start_date', 'code', 'to_do', 'note']

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



