################################################################################
# Pregnancy, Arsenic, and Immune Response (PAIR) Study
# Drinking Water Arsenic and Hemoglobin -- Subset

# Tyler Smith
# May 30, 2023

##### Preliminaries ############################################################
# Load Libraries
import numpy as np
import pandas as pd
from scipy.stats import iqr

##### Subset on Singleton Live Births ##########################################
df_slb = df[
    (df['LIVEBIRTH'] == 1) & 
    (df['SINGLETON'] == 1)]

df_slb.head()

##### Restrict to Complete Covariates ##########################################
# Count Missing Values
df_slb.isna().sum()

# Subset on Non-Missing Age
df_slb = df_slb[df_slb['AGE'].notna()]

df_slb.head()

##### Indicate Selection #######################################################
df_slb['VISIT1'] = np.where(df_slb['SEHEMO'].isna(), 0, 1)
df_slb['VISIT2'] = np.where(df_slb['SVXHEMO'].isna(), 0, 1)
df_slb['VISIT3'] = np.where(df_slb['SMHEMO'].isna(), 0, 1)
df_slb['VISIT4'] = np.where(df_slb['SM3HEMO'].isna(), 0, 1)

for i in ['VISIT1','VISIT2','VISIT3','VISIT4']:
    df_slb[i].value_counts(dropna = False)

df_slb.head()

##### Scale Exposure Variables #################################################
# Scale Exposure Variables
df_slb['ln_wAs_iqr'] = df_slb['ln_wAs'] / iqr(df_slb['ln_wAs'])
df_slb['ln_wFe_iqr'] = df_slb['ln_wFe'] / iqr(df_slb['ln_wFe'])

df_slb.head()

# Check Correlations
df_slb[['ln_wAs_iqr','ln_wFe_iqr']].corr()

##### Indicate >7 Days Postpartum ##############################################
# Initialize Column
df_slb['SMDAYSPP7'] = np.nan

# >7 Days Postpartum
df_slb['SMDAYSPP7'] = np.where(
    (df_slb['VISIT3'] == 1) & (df_slb['SMDAYSPP'] > 7), 
        1, df_slb['SMDAYSPP7'])

# ≤7 Days Postpartum
df_slb['SMDAYSPP7'] = np.where(
    (df_slb['VISIT3'] == 1) & (df_slb['SMDAYSPP'] <= 7), 
        0, df_slb['SMDAYSPP7'])

# Check Values
df_slb['SMDAYSPP7'].value_counts(dropna = False)

df_slb.head()

