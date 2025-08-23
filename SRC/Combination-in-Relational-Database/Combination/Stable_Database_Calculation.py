# Databricks notebook source
pip install openpyxl

import pandas as pd
import io
import datetime
import re
import numpy as np
from ast import literal_eval
import warnings
import os
from openpyxl import load_workbook
import math

# Configuration for file paths
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
COMBINED_TABLE_PATH = os.path.join(DATA_DIR, 'combined_table', 'database_combined.csv')
STABLE_COLUMNS_PATH = os.path.join(DATA_DIR, 'stable_database_columns.csv')
STABLE_DATABASE_PATH = os.path.join(DATA_DIR, 'stable_database', 'stable_combined.csv')

database = pd.read_csv(COMBINED_TABLE_PATH)
database_naive = (database['experiment_group']!='Drug')
database = database[(database['complete']!='No')&(database['experiment_group']=='Drug')]


def total_intake_calc(row):
    out = 0
    for i in range(1,15):
        ses = 'reward_presses_LGA'
        if i <10:
            ses+='0'
        ses += str(i)
        if np.isnan(row[ses]):
            out = np.nan
            break
        out += row[ses]
    row['total_intake_lga'] = out
    out = 0
    ceil = 11
    if row['drug_group'] == 'Oxycodone':
        ceil = 5
    for i in range(1,ceil):
        ses = 'reward_presses_SHA'
        if i <10:
            ses+='0'
        ses += str(i)
        if np.isnan(row[ses]):
            out = np.nan
            break
        out += row[ses]
    row['total_intake_sha'] = out
    return row

database = database.apply(total_intake_calc,axis=1)
database

def ses_delete_list(ses):
    out = [
        'active_lever_presses_'+ses,
        'inactive_lever_presses_'+ses,
        'timtout_presses_'+ses,
        'active_timestamps_'+ses,
        'inactive_timestamps_'+ses,
        'reward_timestamps_'+ses,
    ]
    if 'pr' in ses.lower() or 'treatment' in ses.lower():
        out += ['breakpoint_'+ses]
    return out

sha_bound = [
    "reward_presses_SHA01",
    "reward_presses_SHA02",
    "reward_presses_SHA03",
    "reward_presses_SHA04",
    "reward_presses_SHA05",
    "reward_presses_SHA06",
    "reward_presses_SHA07",
    "reward_presses_SHA08",
    "reward_presses_SHA09",
    "reward_presses_SHA10"
]
lga_bound = [
    "reward_presses_LGA01",
    "reward_presses_LGA02",
    "reward_presses_LGA03",
    "reward_presses_LGA04",
    "reward_presses_LGA05",
    "reward_presses_LGA06",
    "reward_presses_LGA07",
    "reward_presses_LGA08",
    "reward_presses_LGA09",
    "reward_presses_LGA10",
    "reward_presses_LGA11"
]
pr_bound = ['reward_presses_PR01',
          'reward_presses_PR02',
          'reward_presses_PR03',
          'reward_presses_TREATMENT01', 
          'reward_presses_TREATMENT03', 
          'reward_presses_TREATMENT02',
          'reward_presses_TREATMENT04']

shock_bound = ['total_reward_SHOCK_V1',
               'total_reward_SHOCK_V2',
               'total_reward_SHOCK_V3',
               'total_reward_PRESHOCK']


flag_list = []

def abnormal_impute(row):

    global flag_list
    def cha_ses(ses):
        r = int(ses[-2:])
        session1 = ses[:-2]+str(r+1)
        if r+1<10:
            session1 = ses[:-2]+'0'+str(r+1)
        session2 = ses[:-2]+str(r-1)
        if r==1:
            session2 = ses[:-2]+'03'
        elif r-1<10:
            session2 = ses[:-2]+'0'+str(r-1)
        
        return (row[session1]+row[session1])/2
    
    for ses in lga_bound:
        if np.isnan(row[ses]):
            row[ses] = cha_ses(ses)
            for s in ses_delete_list(ses):
                row[s] = np.nan

    lga_over = []
    for ses in lga_bound:
        if np.isnan(row[ses]) == False and row[ses]>250:
            lga_over+=[ses]

    if len(lga_over) ==1:
        row[lga_over[0]] = np.nan
        for s in ses_delete_list(lga_over[0]):
            row[s] = np.nan
    elif len(lga_over) >1:
        for ses in lga_over:
            row[ses] = 250
            for s in ses_delete_list(ses):
                row[s] = np.nan
        flag_list+=[row]

    
    shas = sha_bound
    if row['drug_group'] == 'Oxycodone':
        shas = sha_bound[:4]
    sha_miss = []
    for ses in shas:
        if np.isnan(row[ses]):
            row[ses] = cha_ses(ses)
            for s in ses_delete_list(ses):
                row[s] = np.nan
    
    sha_over = []
    for ses in shas:
        if np.isnan(row[ses]) == False and row[ses]>250:
            sha_miss+=[ses]
    if len(sha_over) ==1:
        row[sha_over[0]] = np.nan
        for s in ses_delete_list(sha_over[0]):
            row[s] = np.nan
    elif len(sha_over)>1:
        for ses in sha_over:
            row[ses] = 250
        for s in ses_delete_list(ses):
            row[s] = np.nan
        flag_list+=[row]

    pr_over = []
    prs = pr_bound
    if row['drug_group'] == 'Cocaine':
        prs = pr_bound[:3]
    for ses in pr_bound:
        if row[ses]>250:
            pr_over += [ses]
    
    if len(pr_over) == 1:       
        row[pr_over[0]] = np.nan
        for s in ses_delete_list(pr_over[0]):
            row[s] = np.nan
    elif len(pr_over)>1:
        for ses in pr_over:
            row[pr_over[0]] = 250
            for s in ses_delete_list(ses):
                row[s] = np.nan

    sh_over = []
    for ses in shock_bound:
        if row[ses]>250:
            sh_over += [ses]
    
    if len(sh_over) == 1:       
        row[sh_over[0]] = np.nan
        for s in ses_delete_list(sh_over[0]):
            row[s] = np.nan
    elif len(sh_over)>1:
        for ses in sh_over:
            row[sh_over[0]] = 250
            for s in ses_delete_list(ses):
                row[s] = np.nan
    
            
    return row


database = database.apply(abnormal_impute,axis=1)
database


pd.DataFrame(flag_list)

database_coc = database[database['drug_group']=='Cocaine']
database_oxy = database[database['drug_group']=='Oxycodone']

sexs = database['sex'].unique()
cohorts = database['cohort'].unique()

def shock_calc(row):
    A = row['rewards_after_first_shock_SHOCK_V3']
    B = row['total_shocks_PRESHOCK']
    if np.isnan(B):
        cnt1 = 0
        if type(row['reward_timestamps_LGA12']) == str and 'nan' not in row['reward_timestamps_LGA12']:
            lst = eval(row['reward_timestamps_LGA12'])
            for i in lst:
                if i<=3600:
                    cnt1 += 1
                else:
                    break
        else:
            cnt1 = np.nan
        cnt2 = 0
        if type(row['reward_timestamps_LGA13']) == str and 'nan' not in row['reward_timestamps_LGA13']:
            lst = eval(row['reward_timestamps_LGA13'])
            for i in lst:
                if i<=3600:
                    cnt2 += 1
                else:
                    break
        else:
            cnt2 = np.nan
        cnt3 = 0
        if type(row['reward_timestamps_LGA14']) == str and 'nan' not in row['reward_timestamps_LGA14']:
            lst = eval(row['reward_timestamps_LGA14'])
            for i in lst:
                if i<=3600:
                    cnt3 += 1
                else:
                    break
        else:
            cnt3 = np.nan
        B = np.nanmean([cnt1,cnt2,cnt3])
    if B == 0 or np.isnan(B):
        return np.nan
    return (A-B)/B

df_calc = pd.DataFrame()
   ###create a new database based upon the combined tables + the additional calculated values: 'Esc_i_sc', 'PR_i_sc', 'Withdrawal_i_sc', 'Tolerence_i_sc', 'AI_sc', 'Esc_i_s', 'PR_i_s', 'Withdrawal_i_s', 'Tolerence_i_s', 'AI_s', 'Esc_i', 'PR_i', 'Withdrawal_i', 'Tolerence_i', 'AI'
database_ind = database[database['complete'].apply(lambda x: type(x)!=str or 'no' not in x.lower())]
### Addiction Index, per sex and per cohort
for s in sexs:
    for c in cohorts:
       #For Oxy
        df = database_ind[(database_ind['sex']==s) & (database_ind['cohort']==c) & (database_ind['drug_group']=='Oxycodone')].copy().set_index('rfid')
        if len(df)>0:
            lga1mean = df['reward_presses_LGA01'].mean(skipna=True)
            lga1std = df['reward_presses_LGA01'].std()
            mean234 = ((df[['reward_presses_LGA11','reward_presses_LGA12','reward_presses_LGA13','reward_presses_LGA14']]- lga1mean)/lga1std).mean(axis=1,skipna=False)
            intk_avg = df[['reward_presses_LGA11','reward_presses_LGA12','reward_presses_LGA13','reward_presses_LGA14']].mean(axis=1,skipna=False)
            df['intk_avg'] = intk_avg
            df['mean234'] = mean234
            df['avg_intk_aio'] = (intk_avg - intk_avg.mean())/intk_avg.std()
            df['esc_aio'] = (mean234 - mean234.mean())/mean234.std()

            #not used in index calculation
            sha1mean = df['reward_presses_SHA01'].mean()
            sha1std = df['reward_presses_SHA01'].std()
            sha234 = ((df[['reward_presses_SHA02','reward_presses_SHA03','reward_presses_SHA04']] - sha1mean)/sha1std).mean(axis=1,skipna=False)
            df['esc_sha'] = (sha234 - sha234.mean())/sha234.std()
            ####
            pr2 = df['reward_presses_PR02']
            pr2 = (pr2-pr2.mean())/pr2.std()
            df['pr_aio'] = pr2
            tail23 = df['tail_immersion_2_time']- df['tail_immersion_3_time']
            tail23 = (tail23-tail23.mean())/tail23.std()
            df['tolerance_aio'] = tail23
            VFdiff = df['von_frey_difference_force']
            VFdiff = (VFdiff-VFdiff.mean())/VFdiff.std()
            df['withdrawal_aio'] = VFdiff
            df['intake_ai_aio'] = df[['avg_intk_aio', 'pr_aio', 'withdrawal_aio', 'tolerance_aio']].mean(axis=1,skipna=False)
            df['ai_aio'] = df[['esc_aio', 'pr_aio', 'withdrawal_aio', 'tolerance_aio']].mean(axis=1,skipna=False)
            df['shock_aio'] = np.nan
            df['lga_mean_delta_esc_11_14'] = mean234
            df_calc = pd.concat([df_calc, df[['esc_aio', 'pr_aio', 'withdrawal_aio', 'tolerance_aio', 'ai_aio','lga_mean_delta_esc_11_14','intake_ai_aio','avg_intk_aio','intk_avg','mean234']]])

        #For Cocaine
        df = database_ind[(database_ind['sex']==s) & (database_ind['cohort']==c) & (database_ind['drug_group']=='Cocaine')].copy().set_index('rfid')
        if len(df)>0:
            lga1mean = df['reward_presses_LGA01'].mean()
            lga1std = df['reward_presses_LGA01'].std()
            mean234 = ((df[['reward_presses_LGA11','reward_presses_LGA12','reward_presses_LGA13','reward_presses_LGA14']]- lga1mean)/lga1std).mean(axis=1,skipna=False)
            intk_avg = df[['reward_presses_LGA11','reward_presses_LGA12','reward_presses_LGA13','reward_presses_LGA14']].mean(axis=1,skipna=False)
            df['intk_avg'] = intk_avg
            df['mean234'] = mean234
            df['avg_intk_aio'] = (intk_avg - intk_avg.mean())/intk_avg.std()
            df['esc_aio'] = (mean234 - mean234.mean())/mean234.std()

            #not used in index calculation
            sha1mean = df['reward_presses_SHA01'].mean()
            sha234 = ((df[['reward_presses_SHA08','reward_presses_SHA09','reward_presses_SHA10']] - sha1mean)/sha1std).mean(axis=1,skipna=False)
            df['esc_sha'] = (sha234 - sha234.mean())/sha234.std()
            ####

            prmax = df[['reward_presses_PR02', 'reward_presses_PR03']].max(axis=1,skipna=False)
            pr_i = (prmax-prmax.mean())/prmax.std()
            df['pr_aio'] = pr_i
            ## previous way of calculating shock (A-B)/B format
            #shock = df.apply(shock_calc,axis=1)
            #shock = (shock-shock.mean())/shock.std()
            df['shock_aio'] = df['rewards_after_first_shock_SHOCK_V3']
            df['tolerance_aio'] = tail23
            df['intake_ai_aio'] = df[['avg_intk_aio', 'pr_aio', 'shock_aio']].mean(axis=1,skipna=False)
            df['ai_aio'] = df[['esc_aio', 'pr_aio', 'shock_aio']].mean(axis=1,skipna=False)
            df['lga_mean_delta_esc_11_14'] = mean234
            sha1mean = df['reward_presses_SHA01'].mean()
            sha1std = df['reward_presses_SHA01'].std()
            mean890 = ((df[['reward_presses_SHA08','reward_presses_SHA09','reward_presses_SHA10']] - sha1mean)/sha1std).mean(axis=1,skipna=False)
            df['sha_mean_delta_esc_08_10'] = mean890
            ###
            df_calc = pd.concat([df_calc, df[['esc_sha','esc_aio', 'pr_aio', 'shock_aio', 'tolerance_aio','ai_aio','sha_mean_delta_esc_08_10','lga_mean_delta_esc_11_14','intake_ai_aio','avg_intk_aio','intk_avg','mean234']]])

df_calc=df_calc.reset_index()
df_calc



add_ind_q = df_calc['ai_aio'].quantile(q=[0.25, 0.5, 0.75])
def add_ind_quart(row):
    x = row['ai_aio']
    if x<add_ind_q[0.25]:
        row['ai_aio_quartile'] = 1
        row['ai_aio_quartile_str'] = 'resilient'
    elif x<add_ind_q[0.5]:
        row['ai_aio_quartile'] = 2
        row['ai_aio_quartile_str'] = 'mild'
    elif x<add_ind_q[0.75]:
        row['ai_aio_quartile'] = 3
        row['ai_aio_quartile_str'] = 'moderate'
    elif x>=add_ind_q[0.75]:
        row['ai_aio_quartile'] = 4
        row['ai_aio_quartile_str'] = 'severe'
    else:
        row['ai_aio_quartile'] = np.nan
        row['ai_aio_quartile_str'] = np.nan
    return row
df_calc = df_calc.apply(add_ind_quart,axis=1)

add_ind_q = df_calc['intake_ai_aio'].quantile(q=[0.25, 0.5, 0.75])
def add_ind_quart(row):
    x = row['intake_ai_aio']
    if x<add_ind_q[0.25]:
        row['intake_ai_aio_quartile'] = 1
        row['intake_ai_aio_quartile_str'] = 'resilient'
    elif x<add_ind_q[0.5]:
        row['intake_ai_aio_quartile'] = 2
        row['intake_ai_aio_quartile_str'] = 'mild'
    elif x<add_ind_q[0.75]:
        row['intake_ai_aio_quartile'] = 3
        row['intake_ai_aio_quartile_str'] = 'moderate'
    elif x>=add_ind_q[0.75]:
        row['intake_ai_aio_quartile'] = 4
        row['intake_ai_aio_quartile_str'] = 'severe'
    else:
        row['intake_ai_aio_quartile'] = np.nan
        row['intake_ai_aio_quartile_str'] = np.nan
    return row
df_calc = df_calc.apply(add_ind_quart,axis=1)
df_calc[['ai_aio_quartile','ai_aio_quartile_str','intake_ai_aio_quartile','intake_ai_aio_quartile_str']].head()

df_calc2 = pd.DataFrame()
### Addiction Index, per cohort for both sexes
for c in cohorts:
    #For Oxy
    df = database_ind[(database_ind['cohort']==c) & (database_ind['drug_group']=='Oxycodone') & (database_ind['experiment_group']=='Drug')].copy().set_index('rfid') 
    lga1mean = df['reward_presses_LGA01'].mean()
    lga1std = df['reward_presses_LGA01'].std()
    if len(df)>0:
        mean234 = ((df[['reward_presses_LGA11','reward_presses_LGA12','reward_presses_LGA13','reward_presses_LGA14']]- lga1mean)/lga1std).mean(axis=1,skipna=False)
        intk_avg = df[['reward_presses_LGA11','reward_presses_LGA12','reward_presses_LGA13','reward_presses_LGA14']].mean(axis=1,skipna=False)
        df['avg_intk_i_s'] = (intk_avg - intk_avg.mean())/intk_avg.std()
        df['esc_i_s'] = (mean234 - mean234.mean())/mean234.std()

        #not used in index calculation
        sha1mean = df['reward_presses_SHA01'].mean()
        sha1std = df['reward_presses_SHA01'].std()
        sha234 = ((df[['reward_presses_SHA02','reward_presses_SHA03','reward_presses_SHA04']] - sha1mean)/sha1std).mean(axis=1,skipna=False)
        df['esc_sha_i_s'] = (sha234 - sha234.mean())/sha234.std()
        ####

        pr2 = df['reward_presses_PR02']
        pr2 = (pr2-pr2.mean())/pr2.std()
        df['pr_i_s'] = pr2
        tail23 = df['tail_immersion_2_time']- df['tail_immersion_3_time']
        tail23 = (tail23-tail23.mean())/tail23.std()
        df['tolerance_i_s'] = tail23
        VFdiff = df['von_frey_difference_force']
        VFdiff = (VFdiff-VFdiff.mean())/VFdiff.std()
        df['withdrawal_i_s'] = VFdiff
        df['intake_ai_s'] = df[['avg_intk_i_s', 'pr_i_s', 'withdrawal_i_s', 'tolerance_i_s']].mean(axis=1, skipna=False)
        df['ai_s'] = df[['esc_i_s', 'pr_i_s', 'withdrawal_i_s', 'tolerance_i_s']].mean(axis=1, skipna=False)

        df_calc2 = pd.concat([df_calc2, df[['esc_i_s', 'pr_i_s', 'withdrawal_i_s', 'tolerance_i_s','ai_s','intake_ai_s']]])

    #For Cocaine
    df = database_ind[(database_ind['cohort']==c) & (database_ind['drug_group']=='Cocaine') & (database_ind['experiment_group']=='Drug')].copy().set_index('rfid')
    lga1mean = df['reward_presses_LGA01'].mean()
    lga1std = df['reward_presses_LGA01'].std()
    if len(df)>0:
        mean234 = ((df[['reward_presses_LGA11','reward_presses_LGA12','reward_presses_LGA13','reward_presses_LGA14']]- lga1mean)/lga1std).mean(axis=1,skipna=False)
        intk_avg = df[['reward_presses_LGA11','reward_presses_LGA12','reward_presses_LGA13','reward_presses_LGA14']].mean(axis=1,skipna=False)
        df['avg_intk_i_s'] = (intk_avg - intk_avg.mean())/intk_avg.std()
        df['esc_i_s'] = (mean234 - mean234.mean())/mean234.std()

        #not used in index calculation
        sha1mean = df['reward_presses_SHA01'].mean()
        sha1std = df['reward_presses_SHA01'].std()
        sha234 = ((df[['reward_presses_SHA08','reward_presses_SHA09','reward_presses_SHA10']] - sha1mean)/sha1std).mean(axis=1,skipna=False)
        df['esc_sha_i_s'] = (sha234 - sha234.mean())/sha234.std()
        ####

        prmax = df[['reward_presses_PR02', 'reward_presses_PR03']].max(axis=1,skipna=False)
        pr_i = (prmax-prmax.mean())/prmax.std()
        df['pr_i_s'] = pr_i
        #shock = df.apply(shock_calc,axis=1)
        #shock = (shock-shock.mean())/shock.std()
        df['shock_i_s'] = df['rewards_after_first_shock_SHOCK_V3']
        df['intake_ai_s'] = df[['avg_intk_i_s', 'pr_i_s', 'shock_i_s']].mean(axis=1,skipna=False)
        df['ai_s'] = df[['esc_i_s', 'pr_i_s', 'shock_i_s']].mean(axis=1,skipna=False)
        df_calc2 = pd.concat([df_calc2, df[['esc_sha_i_s','esc_i_s', 'pr_i_s','shock_i_s','ai_s','intake_ai_s']]])

df_calc2=df_calc2.reset_index()
df_calc2




add_ind_q = df_calc2['ai_s'].quantile(q=[0.25, 0.5, 0.75])
def add_ind_quart(row):
    x = row['ai_s']
    if x<add_ind_q[0.25]:
        row['ai_s_quartile'] = 1
        row['ai_s_quartile_str'] = 'resilient'
    elif x<add_ind_q[0.5]:
        row['ai_s_quartile'] = 2
        row['ai_s_quartile_str'] = 'mild'
    elif x<add_ind_q[0.75]:
        row['ai_s_quartile'] = 3
        row['ai_s_quartile_str'] = 'moderate'
    elif x>=add_ind_q[0.75]:
        row['ai_s_quartile'] = 4
        row['ai_s_quartile_str'] = 'severe'
    else:
        row['ai_s_quartile'] = np.nan
        row['ai_s_quartile_str'] = np.nan
    return row
df_calc2 = df_calc2.apply(add_ind_quart,axis=1)

add_ind_q = df_calc2['intake_ai_s'].quantile(q=[0.25, 0.5, 0.75])
def add_ind_quart(row):
    x = row['intake_ai_s']
    if x<add_ind_q[0.25]:
        row['intake_ai_s_quartile'] = 1
        row['intake_ai_s_quartile_str'] = 'resilient'
    elif x<add_ind_q[0.5]:
        row['intake_ai_s_quartile'] = 2
        row['intake_ai_s_quartile_str'] = 'mild'
    elif x<add_ind_q[0.75]:
        row['intake_ai_s_quartile'] = 3
        row['intake_ai_s_quartile_str'] = 'moderate'
    elif x>=add_ind_q[0.75]:
        row['intake_ai_s_quartile'] = 4
        row['intake_ai_s_quartile_str'] = 'severe'
    else:
        row['intake_ai_s_quartile'] = np.nan
        row['intake_ai_s_quartile_str'] = np.nan
    return row
df_calc2 = df_calc2.apply(add_ind_quart,axis=1)
df_calc2[['ai_s_quartile','ai_s_quartile_str','intake_ai_s_quartile','intake_ai_s_quartile_str']].head()



df_calc3 = pd.DataFrame()
### Addiction Index, for all cohorts and both sexes
df = database_ind[(database_ind['drug_group']=='Oxycodone') & (database_ind['experiment_group']=='Drug')].copy() 
lga1mean = df['reward_presses_LGA01'].mean()
lga1std = df['reward_presses_LGA01'].std()
mean234 = ((df[['reward_presses_LGA11','reward_presses_LGA12','reward_presses_LGA13','reward_presses_LGA14']]- lga1mean)/lga1std).mean(axis=1,skipna=False)
intk_avg = df[['reward_presses_LGA11','reward_presses_LGA12','reward_presses_LGA13','reward_presses_LGA14']].mean(axis=1,skipna=False)
df['avg_intk_i_sc'] = (intk_avg - intk_avg.mean())/intk_avg.std()
df['esc_i_sc'] = (mean234 - mean234.mean())/mean234.std()

#not used in index calculation
sha1mean = df['reward_presses_SHA01'].mean()
sha1std = df['reward_presses_SHA01'].std()
sha234 = ((df[['reward_presses_SHA02','reward_presses_SHA03','reward_presses_SHA04']] - sha1mean)/sha1std).mean(axis=1,skipna=False)
df['esc_sha_i_sc'] = (sha234 - sha234.mean())/sha234.std()
####

pr2 = df['reward_presses_PR02']
pr2 = (pr2-pr2.mean())/pr2.std()
df['pr_i_sc'] = pr2
tail23 = df['tail_immersion_2_time']- df['tail_immersion_3_time']
tail23 = (tail23-tail23.mean())/tail23.std()
df['tolerance_i_sc'] = tail23
VFdiff = df['von_frey_difference_force']
VFdiff = (VFdiff-VFdiff.mean())/VFdiff.std()
df['withdrawal_i_sc'] = VFdiff
df['intake_ai_sc'] = df[['esc_i_sc', 'pr_i_sc', 'withdrawal_i_sc', 'tolerance_i_sc']].mean(axis=1,skipna=False)
df['ai_sc'] = df[['esc_i_sc', 'pr_i_sc', 'withdrawal_i_sc', 'tolerance_i_sc']].mean(axis=1,skipna=False)
df_calc3 = pd.concat([df_calc3,df[['rfid','esc_i_sc', 'pr_i_sc', 'withdrawal_i_sc', 'tolerance_i_sc','ai_sc','intake_ai_sc']]])

#For Cocaine
df = database_ind[(database_ind['drug_group']=='Cocaine') & (database_ind['experiment_group']=='Drug')].copy()
lga1mean = df['reward_presses_LGA01'].mean()
lga1std = df['reward_presses_LGA01'].std()
mean234 = ((df[['reward_presses_LGA11','reward_presses_LGA12','reward_presses_LGA13','reward_presses_LGA14']]- lga1mean)/lga1std).mean(axis=1,skipna=False)
intk_avg = df[['reward_presses_LGA11','reward_presses_LGA12','reward_presses_LGA13','reward_presses_LGA14']].mean(axis=1,skipna=False)
df['avg_intk_i_sc'] = (intk_avg - intk_avg.mean())/intk_avg.std()
df['esc_i_sc'] = (mean234 - mean234.mean())/mean234.std()

#not used in index calculation
sha1mean = df['reward_presses_SHA01'].mean()
sha1std = df['reward_presses_SHA01'].std()
sha234 = ((df[['reward_presses_SHA02','reward_presses_SHA03','reward_presses_SHA04']] - sha1mean)/sha1std).mean(axis=1,skipna=False)
df['esc_sha_i_sc'] = (sha234 - sha234.mean())/sha234.std()
####

prmax = df[['reward_presses_PR02', 'reward_presses_PR03']].max(axis=1,skipna=False)
pr_i = (prmax-prmax.mean())/prmax.std()
df['pr_i_sc'] = pr_i
#shock = df.apply(shock_calc,axis=1)
#shock = (shock-shock.mean())/shock.std()
df['shock_i_sc'] = df['rewards_after_first_shock_SHOCK_V3']
df['intake_ai_sc'] = df[['esc_i_sc', 'pr_i_sc', 'shock_i_sc']].mean(axis=1,skipna=False)
df['ai_sc'] = df[['esc_i_sc', 'pr_i_sc', 'shock_i_sc']].mean(axis=1,skipna=False)
df_calc3 = pd.concat([df_calc3,df[['rfid','esc_sha_i_sc','esc_i_sc', 'pr_i_sc', 'shock_i_sc','ai_sc','intake_ai_sc']]])
df_calc3



add_ind_q = df_calc3['ai_sc'].quantile(q=[0.25, 0.5, 0.75])
def add_ind_quart(row):
    x = row['ai_sc']
    if x<add_ind_q[0.25]:
        row['ai_sc_quartile'] = 1
        row['ai_sc_quartile_str'] = 'resilient'
    elif x<add_ind_q[0.5]:
        row['ai_sc_quartile'] = 2
        row['ai_sc_quartile_str'] = 'mild'
    elif x<add_ind_q[0.75]:
        row['ai_sc_quartile'] = 3
        row['ai_sc_quartile_str'] = 'moderate'
    elif x>=add_ind_q[0.75]:
        row['ai_sc_quartile'] = 4
        row['ai_sc_quartile_str'] = 'severe'
    else:
        row['ai_sc_quartile'] = np.nan
        row['ai_sc_quartile_str'] = np.nan
    return row
df_calc3 = df_calc3.apply(add_ind_quart,axis=1)

add_ind_q = df_calc3['intake_ai_sc'].quantile(q=[0.25, 0.5, 0.75])
def add_ind_quart(row):
    x = row['intake_ai_sc']
    if x<add_ind_q[0.25]:
        row['intake_ai_sc_quartile'] = 1
        row['intake_ai_sc_quartile_str'] = 'resilient'
    elif x<add_ind_q[0.5]:
        row['intake_ai_sc_quartile'] = 2
        row['intake_ai_sc_quartile_str'] = 'mild'
    elif x<add_ind_q[0.75]:
        row['intake_ai_sc_quartile'] = 3
        row['intake_ai_sc_quartile_str'] = 'moderate'
    elif x>=add_ind_q[0.75]:
        row['intake_ai_sc_quartile'] = 4
        row['intake_ai_sc_quartile_str'] = 'severe'
    else:
        row['intake_ai_sc_quartile'] = np.nan
        row['intake_ai_sc_quartile_str'] = np.nan
    return row
df_calc3 = df_calc3.apply(add_ind_quart,axis=1)
df_calc3[['ai_sc_quartile','ai_sc_quartile_str','intake_ai_sc_quartile','intake_ai_sc_quartile_str']].head()



#oxy



from statistics import mode
def iti_lga_01_02(row):
    nan = np.nan
    if type(row['reward_timestamps_LGA01']) != str or len(row['reward_timestamps_LGA01'])==0: 
        one = []
    else:
        one = eval(row['reward_timestamps_LGA01'])

    if type(row['reward_timestamps_LGA02']) != str or len(row['reward_timestamps_LGA02'])==0: 
        two = []
    else:
        two = eval(row['reward_timestamps_LGA02'])
    
    if type(row['reward_timestamps_LGA11']) != str or len(row['reward_timestamps_LGA11'])==0: 
        thr = []
    else:
        thr = eval(row['reward_timestamps_LGA11'])

    if type(row['reward_timestamps_LGA12']) != str or len(row['reward_timestamps_LGA12'])==0: 
        fou = []
    else:
        fou = eval(row['reward_timestamps_LGA12'])

    if type(row['reward_timestamps_LGA13']) != str or len(row['reward_timestamps_LGA13'])==0: 
        fiv = []
    else:
        fiv = eval(row['reward_timestamps_LGA13'])
    
    if type(row['reward_timestamps_LGA14']) != str or len(row['reward_timestamps_LGA14'])==0: 
        six = []
    else:
        six = eval(row['reward_timestamps_LGA14'])
    
    out1 = []
    for i in range(len(one)-1):
        out1.append(one[i+1]-one[i])
    for i in range(len(two)-1):
        out1.append(two[i+1]-two[i])
    out2 = []

    for i in range(len(thr)-1):
        out2.append(thr[i+1]-thr[i])
    for i in range(len(fou)-1):
        out2.append(fou[i+1]-fou[i])
    for i in range(len(fiv)-1):
        out2.append(fiv[i+1]-fiv[i])
    for i in range(len(six)-1):
        out2.append(six[i+1]-six[i])
    if row['drug_group']=='Oxycodone' and len(out1) != 0:
        row['lga_iti_median_01_02'] = np.median(out1)
        row['lga_iti_mode_01_02'] = mode(out1)
        row['lga_iti_coefficient_of_variation_01_02'] = np.std(out1)/np.mean(out1)
    if len(out2) !=0:
        if row['drug_group']=='Oxycodone':
            row['lga_iti_mode_11_14'] = mode(out2)
        row['lga_iti_median_11_14'] = np.median(out2)
        row['lga_iti_coefficient_of_variation_11_14'] = np.std(out2)/np.mean(out2)
    return row

iti_lga = database[['rfid','reward_timestamps_LGA01','reward_timestamps_LGA02']]
iti_lga = database.apply(iti_lga_01_02,axis=1)[['rfid','lga_iti_median_01_02','lga_iti_coefficient_of_variation_01_02','lga_iti_mode_01_02','lga_iti_median_11_14','lga_iti_coefficient_of_variation_11_14','lga_iti_mode_11_14']]
iti_lga



#lga means
def lga_mean(row):
    row['lga_mean_11_14'] = row[['reward_presses_LGA11','reward_presses_LGA12','reward_presses_LGA13','reward_presses_LGA14']].mean()
    row['lga_mean_inactive_11_14'] = row[['inactive_lever_presses_LGA11','inactive_lever_presses_LGA12','inactive_lever_presses_LGA13','inactive_lever_presses_LGA14']].mean()
    row['lga_mean_to_11_14'] = row[['timeout_presses_LGA11','timeout_presses_LGA12','timeout_presses_LGA13','timeout_presses_LGA14']].mean()
    if row['drug_group'] == 'Oxycodone':
        row['lga_mean_01_02'] = row[['reward_presses_LGA01','reward_presses_LGA02']].mean()
        row['lga_mean_active_01_02'] = row[['active_lever_presses_LGA01','active_lever_presses_LGA02']].mean()
        row['lga_mean_active_11_14'] = row[['active_lever_presses_LGA11','active_lever_presses_LGA12','active_lever_presses_LGA13','active_lever_presses_LGA14']].mean()
        row['lga_mean_inactive_01_02'] = row[['inactive_lever_presses_LGA01','inactive_lever_presses_LGA02']].mean()
        row['lga_mean_to_01_02'] = row[['timeout_presses_LGA01','timeout_presses_LGA02']].mean()
    return row

lga_mean = database.apply(lga_mean,axis=1)[['rfid','lga_mean_01_02','lga_mean_11_14','lga_mean_active_01_02','lga_mean_active_11_14','lga_mean_inactive_01_02','lga_mean_inactive_11_14','lga_mean_to_01_02','lga_mean_to_11_14']]
lga_mean




#sha means
def sha_mean(row):
    if row['drug_group'] == 'Oxycodone':
        row['sha_mean_01_02'] = row[['reward_presses_SHA01','reward_presses_SHA02']].mean()
        row['sha_mean_03_04'] = row[['reward_presses_SHA03','reward_presses_SHA04']].mean()
        row['sha_mean_inactive_01_02'] = row[['inactive_lever_presses_SHA01','inactive_lever_presses_SHA02']].mean()
        row['sha_mean_inactive_03_04'] = row[['inactive_lever_presses_SHA03','inactive_lever_presses_SHA04']].mean()
        row['sha_mean_to_01_02'] = row[['timeout_presses_SHA01','timeout_presses_SHA02']].mean()
        row['sha_mean_to_03_04'] = row[['timeout_presses_SHA03','timeout_presses_SHA04']].mean()
    if row['drug_group'] == 'Cocaine':
        row['sha_mean_01_03'] = row[['reward_presses_SHA01','reward_presses_SHA02','reward_presses_SHA03']].mean()
        row['sha_mean_08_10'] = row[['reward_presses_SHA08','reward_presses_SHA09','reward_presses_SHA10']].mean()
        row['sha_mean_inactive_01_03'] = row[['inactive_lever_presses_SHA01','inactive_lever_presses_SHA02','inactive_lever_presses_SHA03']].mean()
        row['sha_mean_inactive_08_10'] = row[['inactive_lever_presses_SHA08','inactive_lever_presses_SHA09','inactive_lever_presses_SHA10']].mean()
        row['sha_mean_to_01_03'] = row[['timeout_presses_SHA01','timeout_presses_SHA02','timeout_presses_SHA03']].mean()
        row['sha_mean_to_08_10'] = row[['timeout_presses_SHA08','timeout_presses_SHA09','timeout_presses_SHA10']].mean()

    return row

sha_mean = database.apply(sha_mean,axis=1)[['rfid','sha_mean_01_02','sha_mean_03_04','sha_mean_inactive_01_02','sha_mean_inactive_03_04','sha_mean_to_01_02','sha_mean_to_03_04','sha_mean_01_03','sha_mean_08_10','sha_mean_inactive_01_03','sha_mean_inactive_08_10','sha_mean_to_01_03','sha_mean_to_08_10']]
sha_mean



def iti_sha(row):
    if type(row['reward_timestamps_SHA01']) != str or len(row['reward_timestamps_SHA01'])==0: 
        one = []
    else:
        one = eval(row['reward_timestamps_SHA01'])

    if type(row['reward_timestamps_SHA02']) != str or len(row['reward_timestamps_SHA02'])==0: 
        two = []
    else:
        two = eval(row['reward_timestamps_SHA02'])

    if type(row['reward_timestamps_SHA03']) != str or len(row['reward_timestamps_SHA03'])==0: 
        thr = []
    else:
        thr = eval(row['reward_timestamps_SHA03'])

    if type(row['reward_timestamps_SHA04']) != str or len(row['reward_timestamps_SHA04'])==0: 
        fou = []
    else:
        fou = eval(row['reward_timestamps_SHA04'])
    out1 = []
    for i in range(len(one)-1):
        out1.append(one[i+1]-one[i])
    for i in range(len(two)-1):
        out1.append(two[i+1]-two[i])

    out2 = []
    for i in range(len(thr)-1):
        out2.append(thr[i+1]-thr[i])
    for i in range(len(fou)-1):
        out2.append(fou[i+1]-fou[i])
        
    if len(out1) != 0:
        row['sha_iti_mode_01_02'] = mode(out1)
        row['sha_iti_coefficient_of_variation_01_02'] = np.std(out1)/np.mean(out1)
    if len(out2) !=0:
        row['sha_iti_mode_03_04'] = mode(out2)
        row['sha_iti_median_03_04'] = np.median(out2)
        row['sha_iti_coefficient_of_variation_03_04'] = np.std(out2)/np.mean(out2)
    return row
iti_sha = database_oxy.apply(iti_sha,axis=1)[['rfid','sha_iti_median_03_04','sha_iti_coefficient_of_variation_01_02','sha_iti_coefficient_of_variation_03_04','sha_iti_mode_01_02','sha_iti_mode_03_04']]
iti_sha



def tr_gr_calc(row):
    group = {}
    tot_pr = 0
    if type(row['treatment_1_group']) == str:
        group[row['treatment_1_group'].lower().strip()] = [row['active_lever_presses_TREATMENT01'],row['breakpoint_TREATMENT01'],row['inactive_lever_presses_TREATMENT01'],row['reward_presses_TREATMENT01']]
    if type(row['treatment_2_group']) == str:
        group[row['treatment_2_group'].lower().strip()]= [row['active_lever_presses_TREATMENT02'],row['breakpoint_TREATMENT02'],row['inactive_lever_presses_TREATMENT02'],row['reward_presses_TREATMENT02']]
    if type(row['treatment_3_group']) == str:
        group[row['treatment_3_group'].lower().strip()] = [row['active_lever_presses_TREATMENT03'],row['breakpoint_TREATMENT03'],row['inactive_lever_presses_TREATMENT03'],row['reward_presses_TREATMENT03']]
    if type(row['treatment_4_group']) == str:
        group[row['treatment_4_group'].lower().strip()] = [row['active_lever_presses_TREATMENT04'],row['breakpoint_TREATMENT04'],row['inactive_lever_presses_TREATMENT04'],row['reward_presses_TREATMENT04']]
    
    for k in ['vehicle','saline','methadone','naltrexone']:
        if k in group:
            row['pr_'+str(k)+'_active'] = group[k][0]
            row['pr_'+str(k)+'_breakpoint'] = group[k][1]
            row['pr_'+str(k)+'_inactive'] = group[k][2]
            row['pr_'+str(k)+'_rewards'] = group[k][3]
            if row['reward_presses_PR02'] > 0 and row.isna()['reward_presses_PR02'] == False:
                row['treatments_pr_'+str(k)] = (group[k][3]/row['reward_presses_PR02'])*100
        else:
            row['pr_'+str(k)+'_active'] = np.nan
            row['pr_'+str(k)+'_breakpoint'] = np.nan
            row['pr_'+str(k)+'_inactive'] = np.nan
            row['pr_'+str(k)+'_rewards'] = np.nan
            row['treatments_pr_'+str(k)] = np.nan
    return row
    



prs = (database_oxy.apply(tr_gr_calc,axis=1)[['rfid','pr_vehicle_active',
                                              'pr_vehicle_breakpoint','pr_vehicle_inactive',
                                              'pr_vehicle_rewards',
                                              'treatments_pr_vehicle',
                                              'pr_saline_active',
                                              'pr_saline_breakpoint',
                                              'pr_saline_inactive',
                                              'pr_saline_rewards',
                                              'treatments_pr_saline',
                                              'pr_methadone_active',
                                              'pr_methadone_breakpoint',
                                              'pr_methadone_inactive',
                                              'pr_methadone_rewards',
                                              'treatments_pr_methadone',
                                              'pr_naltrexone_active',
                                              'pr_naltrexone_breakpoint',
                                              'pr_naltrexone_inactive',
                                              'pr_naltrexone_rewards',
                                              'treatments_pr_naltrexone']])
prs



def get_bursts(reward_timestamps, interval=120):
    if type(reward_timestamps)!=str:
        arr = []
    elif 'nan' in reward_timestamps:
        arr = []
    else:
        arr = eval(reward_timestamps)
    allBursts = []
    i = 0
    while i < len(arr):
        oneBurst = []
        limit = arr[i] + interval
        j = i
        while j < len(arr) and arr[j] <= limit:
            oneBurst.append(arr[j])
            limit = arr[j] + interval
            j += 1
        allBursts.append(oneBurst)
        i = j
    allBursts = [i for i in allBursts if len(i) > 1]
    return allBursts



def sha_burst_vars(row):
    s1 = get_bursts(row['reward_timestamps_SHA01'])
    s2 = get_bursts(row['reward_timestamps_SHA02'])
    s3 = get_bursts(row['reward_timestamps_SHA03'])
    s4 = get_bursts(row['reward_timestamps_SHA04'])

    s12 = s1+s2
    s34 = s3+s4

    row['sha_iti_numburst_01_02'] = len(s12)
    row['sha_iti_numburst_03_04'] = len(s34)

    num12 = [len(i) for i in s12]
    num34 = [len(i) for i in s34]

    if len(num12) == 0:
        row['sha_iti_maxburst_01_02'] = np.nan
    else:
        row['sha_iti_maxburst_01_02'] = max(num12)
    if len(num34) == 0:
        row['sha_iti_maxburst_03_04'] = np.nan
    else:
        row['sha_iti_maxburst_03_04'] = max(num34)
    if len(num12) == 0:
        row['sha_iti_meannumrewards_01_02'] = np.nan
    else:
        row['sha_iti_meannumrewards_01_02'] = np.mean(num12)
    if len(num34) == 0:
        row['sha_iti_meannumrewards_03_04'] = np.nan
    else:
        row['sha_iti_meannumrewards_03_04'] = np.mean(num34)
    burs1 = 0
    for i in s12:
        burs1+=len(i)
    burs2 = 0
    for i in s34:
        burs2+=len(i)
    if (row['reward_presses_SHA01']+row['reward_presses_SHA02']) > 0:
        row['sha_iti_pctnumrewards_01_02'] = burs1/(row['reward_presses_SHA01']+row['reward_presses_SHA02'])
    if (row['reward_presses_SHA03']+row['reward_presses_SHA04']) > 0:
        row['sha_iti_pctnumrewards_03_04'] = burs2/(row['reward_presses_SHA03']+row['reward_presses_SHA04'])
    
    return row



#burst
sha_burst = database.apply(sha_burst_vars,axis=1)[['rfid','sha_iti_numburst_01_02','sha_iti_numburst_03_04','sha_iti_maxburst_01_02','sha_iti_maxburst_03_04','sha_iti_meannumrewards_01_02','sha_iti_meannumrewards_03_04']]



def lga_burst_vars(row):
    nan = np.nan
    l1 = get_bursts(row['reward_timestamps_LGA01'])
    l2 = get_bursts(row['reward_timestamps_LGA02'])
    l3 = get_bursts(row['reward_timestamps_LGA11'])
    l4 = get_bursts(row['reward_timestamps_LGA12'])
    l5 = get_bursts(row['reward_timestamps_LGA13'])
    l6 = get_bursts(row['reward_timestamps_LGA14'])

    l12 = l1+l2
    l34 = l3+l4+l5+l6

    row['lga_iti_numburst_01_02'] = len(l12)
    row['lga_iti_numburst_11_14'] = len(l34)

    num12 = [len(i) for i in l12]
    num34 = [len(i) for i in l34]

    if len(num12) == 0:
        row['lga_iti_maxburst_01_02'] = np.nan
    else: 
        row['lga_iti_maxburst_01_02'] = max(num12)
    if len(num34) == 0:
        row['lga_iti_maxburst_11_14'] = np.nan
    else: 
        row['lga_iti_maxburst_11_14'] = max(num34)
    if len(num12) == 0:
        row['lga_iti_meannumrewards_01_02'] = np.nan
    else: 
        row['lga_iti_meannumrewards_01_02'] = np.mean(num12)
    if len(num34) == 0:
        row['lga_iti_meannumrewards_11_14'] = np.nan
    else: 
        row['lga_iti_meannumrewards_11_14'] = np.mean(num34)
    burs1 = 0
    for i in l12:
        burs1+=len(i)
    burs2 = 0
    for i in l34:
        burs2+=len(i)
    if (row['reward_presses_LGA01']+row['reward_presses_LGA02']) !=0:
        row['lga_iti_pctnumrewards_01_02'] = burs1/(row['reward_presses_LGA01']+row['reward_presses_LGA02'])
    if (row['reward_presses_LGA11']+row['reward_presses_LGA12']+row['reward_presses_LGA13']+row['reward_presses_LGA14']) != 0:
        row['lga_iti_pctnumrewards_11_14'] = burs2/(row['reward_presses_LGA11']+row['reward_presses_LGA12']+row['reward_presses_LGA13']+row['reward_presses_LGA14'])
    
    return row



lga_burst = database.apply(lga_burst_vars,axis=1)[['rfid','lga_iti_numburst_01_02','lga_iti_numburst_11_14','lga_iti_maxburst_01_02','lga_iti_maxburst_11_14','lga_iti_meannumrewards_01_02','lga_iti_meannumrewards_11_14','lga_iti_pctnumrewards_01_02','lga_iti_pctnumrewards_11_14']]



def phase_calc_sha_oxy(row):
    cnt1 = 0
    cnt2 = 0
    if type(row['reward_timestamps_SHA01']) ==str:
        for i in eval(row['reward_timestamps_SHA01']):
            if i <= 600:
                cnt1+=1
            if i>=3600:
                cnt2+=1
    if type(row['reward_timestamps_SHA02']) ==str:
        cnt1 = 0
        cnt2 = 0
        for i in eval(row['reward_timestamps_SHA02']):
            if i <= 600:
                cnt1+=1
            if i>=3600:
                cnt2+=1
    row['sha_loading_phase_intake_01_02'] = cnt1
    row['sha_titration_phase_01_02'] = cnt2
    cnt1 = 0
    cnt2 = 0
    if type(row['reward_timestamps_SHA03']) ==str:
        for i in eval(row['reward_timestamps_SHA03']):
            if i <= 600:
                cnt1+=1
            if i>=3600:
                cnt2+=1
    if type(row['reward_timestamps_SHA04']) ==str:
        for i in eval(row['reward_timestamps_SHA04']):
            if i <= 600:
                cnt1+=1
            if i>=3600:
                cnt2+=1
    
    row['sha_loading_phase_intake_03_04'] = cnt1
    row['sha_titration_phase_03_04'] = cnt2
    
    return row
    
sha_phase_oxy = database_oxy.apply(phase_calc_sha_oxy,axis=1)[['rfid','sha_loading_phase_intake_01_02','sha_titration_phase_01_02','sha_loading_phase_intake_03_04','sha_titration_phase_03_04']]

sha_phase_oxy



import pandas as pd
import numpy as np

def phase_calc_sha_coc(row):
    cnt1 = 0
    cnt2 = 0
    
    # Helper function to process the timestamp columns
    def process_timestamps(timestamp_column):
        nonlocal cnt1, cnt2
        if isinstance(row[timestamp_column], str):  # Ensure the value is a string before eval
            try:
                # Replace "nan" with float('nan') to handle invalid 'nan' strings
                timestamp_list = eval(row[timestamp_column].replace("nan", "float('nan')"))
                for i in timestamp_list:
                    if i <= 600:
                        cnt1 += 1
                    if i >= 3600:
                        cnt2 += 1
            except Exception as e:
                print(f"Error processing {timestamp_column} for row {row.name}: {e}")
    
    # Process the SHA01, SHA02, and SHA03 columns
    process_timestamps('reward_timestamps_SHA01')
    process_timestamps('reward_timestamps_SHA02')
    process_timestamps('reward_timestamps_SHA03')
    
    row['sha_loading_phase_intake_01_03'] = cnt1
    row['sha_titration_phase_01_03'] = cnt2
    
    # Reset counters for the next set of columns
    cnt1 = 0
    cnt2 = 0
    
    # Process the SHA08, SHA09, and SHA10 columns
    process_timestamps('reward_timestamps_SHA08')
    process_timestamps('reward_timestamps_SHA09')
    process_timestamps('reward_timestamps_SHA10')
    
    row['sha_loading_phase_intake_08_10'] = cnt1
    row['sha_titration_phase_08_10'] = cnt2
    
    return row

# Applying the function to the DataFrame
sha_phase_coc = database_coc.apply(phase_calc_sha_coc, axis=1)[['rfid', 'sha_loading_phase_intake_01_03', 'sha_titration_phase_01_03', 'sha_loading_phase_intake_08_10', 'sha_titration_phase_08_10']]

sha_phase_coc




def phase_calc_lga(row):
    cnt1 = []
    cnt2 = []
    if type(row['reward_timestamps_LGA01']) ==str and 'nan' not in row['reward_timestamps_LGA01']:
        temp1 = 0
        temp2 = 0
        for i in eval(row['reward_timestamps_LGA01']):
            if i <= 600:
                temp1+=1
            if i>=21600:
                temp2+=1
        cnt1 += [temp1]
        cnt2 += [temp2]
    if type(row['reward_timestamps_LGA02']) ==str and 'nan' not in row['reward_timestamps_LGA02']:
        temp1 = 0
        temp2 = 0
        for i in eval(row['reward_timestamps_LGA02']):
            if i <= 600:
                temp1+=1
            if i>=21600:
                temp2+=1
        cnt1 += [temp1]
        cnt2 += [temp2]
    if row['drug_group']=='Oxycodone':
        if type(row['reward_timestamps_LGA01']) !=str and type(row['reward_timestamps_LGA02']) !=str:
            row['lga_loading_phase_intake_01_02'] = np.nan
            row['lga_titration_phase_01_02'] = np.nan
        else:
            row['lga_loading_phase_intake_01_02'] = np.mean(cnt1)
            row['lga_titration_phase_01_02'] = np.mean(cnt2)
    else:
        row['lga_loading_phase_intake_01_02'] = np.nan
        row['lga_titration_phase_01_02'] = np.nan
    cnt1 = []
    cnt2 = []
    if type(row['reward_timestamps_LGA11']) ==str and 'nan' not in row['reward_timestamps_LGA11']:
            temp1 = 0
            temp2 = 0
            for i in eval(row['reward_timestamps_LGA11']):
                if i <= 600:
                    temp1+=1
                if i>=21600:
                    temp2+=1
            cnt1 += [temp1]
            cnt2 += [temp2]

    if type(row['reward_timestamps_LGA12']) ==str and 'nan' not in row['reward_timestamps_LGA12']:
        temp1 = 0
        temp2 = 0
        for i in eval(row['reward_timestamps_LGA12']):
            if i <= 600:
                temp1+=1
            if i>=21600:
                temp2+=1
        cnt1 += [temp1]
        cnt2 += [temp2]
    if type(row['reward_timestamps_LGA13']) ==str and 'nan' not in row['reward_timestamps_LGA13']:
        temp1 = 0
        temp2 = 0
        for i in eval(row['reward_timestamps_LGA13']):
            if i <= 600:
                temp1+=1
            if i>=21600:
                temp2+=1
        cnt1 += [temp1]
        cnt2 += [temp2]
    if type(row['reward_timestamps_LGA14']) ==str and 'nan' not in row['reward_timestamps_LGA14']:
        temp1 = 0
        temp2 = 0
        for i in eval(row['reward_timestamps_LGA14']):
            if i <= 600:
                temp1+=1
            if i>=21600:
                temp2+=1
        cnt1 += [temp1]
        cnt2 += [temp2]
    
    if len(cnt1)==0 or len(cnt2)==0:
        row['lga_loading_phase_intake_11_14'] = np.nan
        row['lga_titration_phase_11_14'] = np.nan
    else:
        row['lga_loading_phase_intake_11_14'] = np.mean(cnt1)
        row['lga_titration_phase_11_14'] = np.mean(cnt2)
    return row
lga_phase = database.apply(phase_calc_lga,axis=1)[['rfid','lga_loading_phase_intake_01_02','lga_titration_phase_01_02','lga_loading_phase_intake_11_14','lga_titration_phase_11_14']]



def tail_imm(row):
    row['tail_immersion_analgesia'] = row['tail_immersion_2_time'] - row['tail_immersion_1_time']
    row['tail_immersion_tolerance'] = row['tail_immersion_2_time'] - row['tail_immersion_3_time']
    row['tail_immersion_baseline'] = row['tail_immersion_1_time']
    row['tail_immersion_oxypresa'] = row['tail_immersion_2_time']
    row['tail_immersion_oxypostsa'] = row['tail_immersion_3_time']
    return row

tail_imms = database_oxy.apply(tail_imm,axis=1)[['rfid','tail_immersion_analgesia','tail_immersion_tolerance','tail_immersion_baseline','tail_immersion_oxypresa','tail_immersion_oxypostsa']]



def pr_rename(row):
    row['pr_01_sha'] = row['reward_presses_PR01']
    row['pr_01_sha_breakpoint'] = row['breakpoint_PR01']
    row['pr_02_lga'] = row['reward_presses_PR02']
    row['pr_02_lga_breakpoint'] = row['breakpoint_PR02']
    if row['drug_group'] == 'Oxycodone':
        row['pr_02_inactive'] = row['inactive_lever_presses_PR02']
        row['pr_02_active'] = row['active_lever_presses_PR02']
        row['pr_01_inactive'] = row['inactive_lever_presses_PR01']
        row['pr_01_active'] = row['active_lever_presses_PR01']
    elif row['drug_group'] == 'Cocaine':
        row['pr_03_postshock'] = row['reward_presses_PR03']
        row['pr_03_postshock_breakpoint'] = row['breakpoint_PR03']
        row['pr_max_02_03'] = max(row['reward_presses_PR02'],row['reward_presses_PR03'])
        row['pr_max_02_03_breakpoint'] = max(row['breakpoint_PR02'],row['breakpoint_PR03'])
    return row
pr_res = database.apply(pr_rename,axis=1)[['rfid','pr_01_sha','pr_01_inactive','pr_01_active','pr_01_sha_breakpoint','pr_02_lga','pr_02_inactive','pr_02_active','pr_02_lga_breakpoint','pr_03_postshock','pr_03_postshock_breakpoint','pr_max_02_03','pr_max_02_03_breakpoint']]
pr_res



def von_frey(row):
    row['von_frey_force_bsl'] = row['von_frey_1_force']
    row['von_frey_force_difference'] = row['von_frey_1_force'] - row['von_frey_2_force']
    row['von_frey_force_percent'] = (row['von_frey_1_force'] - row['von_frey_2_force'])/(row['von_frey_1_force'])
    row['von_frey_force_withdrawl'] = row['von_frey_2_force']
    row['von_frey_time_bsl'] = row['von_frey_1_time']
    row['von_frey_time_difference'] = row['von_frey_1_time'] - row['von_frey_2_time']
    row['von_frey_time_percent'] = (row['von_frey_1_time'] - row['von_frey_2_time'])/(row['von_frey_1_time'])
    row['von_frey_time_withdrawl'] = row['von_frey_2_time']
    return row
vons = database_oxy.apply(von_frey,axis=1)[['rfid','von_frey_force_bsl','von_frey_force_difference','von_frey_force_percent','von_frey_force_withdrawl','von_frey_time_bsl','von_frey_time_difference','von_frey_time_percent','von_frey_time_withdrawl']]
vons



import numpy as np

def intervals_calc(arr):
    out = []
    for i in range(len(arr) - 1):
        out.append(arr[i + 1] - arr[i])
    return out

def sha_behave(row):
    meds = []
    itis = []
    
    # Function to handle timestamp processing with nan handling
    def process_timestamps(timestamp_column, meds_list, itis_list):
        if isinstance(row[timestamp_column], str):
            try:
                # Replace "nan" with actual NaN values
                timestamp_list = eval(row[timestamp_column].replace("nan", "float('nan')"))
                temp = intervals_calc(timestamp_list)
                if len(temp) > 0:
                    meds_list.append(np.median(temp))
                    itis_list.extend(temp)
            except Exception as e:
                print(f"Error processing {timestamp_column} for row {row.name}: {e}")

    # Process the SHA01, SHA02, and SHA03 columns
    process_timestamps('reward_timestamps_SHA01', meds, itis)
    process_timestamps('reward_timestamps_SHA02', meds, itis)
    process_timestamps('reward_timestamps_SHA03', meds, itis)
    
    # Calculate behavior stability and coefficient of variation for SHA01_03
    if len(meds) > 0:
        row['sha_behavior_stability_01_03'] = np.std(meds)
    if len(itis) > 0:
        row['sha_coefficient_of_variation_2'] = np.std(itis) / np.mean(itis)
    
    meds1 = []
    meds2 = []
    itis = []
    
    # Process the SHA08, SHA09, and SHA10 columns
    process_timestamps('reward_timestamps_SHA08', meds1, itis)
    process_timestamps('reward_timestamps_SHA09', meds1, itis)
    process_timestamps('reward_timestamps_SHA10', meds1, itis)
    
    # Handle the 'meds2' list and fill it with zeros where necessary
    if len(meds1) == 0:
        meds2.append(0)
    else:
        meds2.append(np.median(meds1))  # if meds1 is non-empty, we use its median
    
    # Fill meds2 with zeros for SHA08, SHA09, SHA10 if no valid data
    for _ in range(3 - len(meds1)):  # Ensure meds2 has the same number of elements
        meds2.append(0)
    
    # Calculate behavior stability and coefficient of variation for SHA08_10
    if len(meds1) > 0:
        row['sha_behavior_stability_08_10'] = np.std(meds1)
    if len(itis) > 0:
        row['sha_coefficient_of_variation'] = np.std(itis) / np.mean(itis)
        row['sha_iti_median_08_10'] = np.median(itis)
    
    # Behavior stability for meds2
    row['sha_behavior_stability_08_10_na'] = np.std(meds2)
    
    return row

# Applying the function to the DataFrame
sha_coc_bh = database_coc.apply(sha_behave, axis=1)[['rfid', 'sha_behavior_stability_01_03', 'sha_coefficient_of_variation_2', 'sha_behavior_stability_08_10', 'sha_coefficient_of_variation', 'sha_iti_median_08_10', 'sha_behavior_stability_08_10_na']]

sha_coc_bh




def lga_behave(row):
    meds1=[]
    meds2=[]
    itis = []
    if type(row['reward_timestamps_LGA11'])==str:
        temp = intervals_calc(eval(row['reward_timestamps_LGA11']))
        if len(temp)>0:
            meds1.append(np.median(temp))
            meds2.append(np.median(temp))
            itis += temp
    else:
        meds2.append(0)
    if type(row['reward_timestamps_LGA12'])==str:
        temp = intervals_calc(eval(row['reward_timestamps_LGA12']))
        if len(temp)>0:
            meds1.append(np.median(temp))
            meds2.append(np.median(temp))
            itis += temp
    else:
        meds2.append(0)
    if type(row['reward_timestamps_LGA13'])==str:
        temp = intervals_calc(eval(row['reward_timestamps_LGA13']))
        if len(temp)>0:
            meds1.append(np.median(temp))
            meds2.append(np.median(temp))
            itis += temp
    else:
        meds2.append(0)
    if type(row['reward_timestamps_LGA14'])==str:
        temp = intervals_calc(eval(row['reward_timestamps_LGA14']))
        if len(temp)>0:
            meds1.append(np.median(temp))
            meds2.append(np.median(temp))
            itis += temp
    else:
        meds2.append(0)

    if len(meds1)>0:
        row['lga_behavior_stability_11_14'] = np.std(meds1)
    row['lga_behavior_stability_11_14_na'] = np.std(meds2)
    
    return row
lga_coc_bh = database_coc.apply(lga_behave,axis=1)[['rfid','lga_behavior_stability_11_14','lga_behavior_stability_11_14_na']]
lga_coc_bh



def irr_calc(row):
    row['irr_agg_change'] = row['diff_ave_agg']
    row['irr_def_change'] = row['diff_ave_def']
    row['irr_total_change'] = row['diff_ave_total']
    return row

irrs = database_coc.apply(irr_calc,axis=1)[['rfid','irr_agg_change','irr_def_change','irr_total_change']]



def shock_perc_pre(row):
    A = row['rewards_after_first_shock_SHOCK_V3']
    B = row['total_shocks_PRESHOCK']
    if np.isnan(B):
        cnt1 = 0
        if type(row['reward_timestamps_LGA12']) == str and 'nan' not in row['reward_timestamps_LGA12']:
            lst = eval(row['reward_timestamps_LGA12'])
            for i in lst:
                if i<=3600:
                    cnt1 += 1
                else:
                    break
        else:
            cnt1 = np.nan
        cnt2 = 0
        if type(row['reward_timestamps_LGA13']) == str and 'nan' not in row['reward_timestamps_LGA13']:
            lst = eval(row['reward_timestamps_LGA13'])
            for i in lst:
                if i<=3600:
                    cnt2 += 1
                else:
                    break
        else:
            cnt2 = np.nan
        cnt3 = 0
        if type(row['reward_timestamps_LGA14']) == str and 'nan' not in row['reward_timestamps_LGA14']:
            lst = eval(row['reward_timestamps_LGA14'])
            for i in lst:
                if i<=3600:
                    cnt3 += 1
                else:
                    break
        else:
            cnt3 = np.nan
        B = np.nanmean([cnt1,cnt2,cnt3])
    if B == 0 or np.isnan(B):
        return np.nan
    return A/B

def shock_rn(row):
    row['shock_03'] = row['total_reward_SHOCK_V3']
    row['shock_percentage_pre'] = shock_perc_pre(row)
    if row['total_reward_PRESHOCK']>0:
        row['shock_03_pre'] = (row['total_reward_SHOCK_V3']/row['total_reward_PRESHOCK'])*100
    if row['cohort'] == 1:
        row['shock_percent_rewards'] = row['total_reward_SHOCK_V3']
        cnt = 0
        if type(row['reward_timestamps_LGA14']) == str:
            for ts in eval(row['reward_timestamps_LGA14']):
                if float(ts)<3600:
                    cnt+=1
                else:
                    break
        if cnt > 0:
            row['shock_percent_rewards'] = row['shock_percent_rewards']/cnt
        else:
            row['shock_percent_rewards'] = np.nan
    else:
        if row['total_reward_PRESHOCK'] >0:
            row['shock_percent_rewards'] = (row['total_reward_SHOCK_V3']/row['total_reward_PRESHOCK'])*100
        else:
            row['shock_percent_rewards'] = np.nan
    return row
shocks = database_coc.apply(shock_rn,axis=1)[['rfid','shock_03','shock_percentage_pre','shock_03_pre','shock_percent_rewards']]

database = pd.concat([database,database_naive])
database

combine = (database.merge(df_calc, how='left', on='rfid')
           .merge(df_calc2, how='left', on='rfid')
           .merge(df_calc3,how='left', on='rfid')
           .merge(iti_lga, how='left', on='rfid')
           .merge(lga_mean, how='left', on='rfid')
           .merge(iti_sha, how='left', on='rfid')
           .merge(sha_mean, how='left', on='rfid')
           .merge(prs, how='left', on='rfid')
           .merge(lga_phase, how='left', on='rfid')
           .merge(sha_burst, how='left', on='rfid')
           .merge(sha_phase_oxy, how='left', on='rfid')
           .merge(sha_phase_coc, how='left', on='rfid')
           .merge(lga_burst, how='left', on='rfid')
           .merge(tail_imms, how='left', on='rfid')
           .merge(pr_res, how='left', on='rfid')
           .merge(vons, how='left', on='rfid')
           .merge(sha_coc_bh, how='left', on='rfid')
           .merge(lga_coc_bh, how='left', on='rfid')
           .merge(shocks, how='left', on='rfid')
           .merge(irrs, how='left', on='rfid'))

combine

cols = list(pd.read_csv(STABLE_COLUMNS_PATH)['Keeping columns'].dropna())
cols



combine = combine[cols]
combine

combine.to_csv(STABLE_DATABASE_PATH, index=False)

