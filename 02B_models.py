################################################################################
# Pregnancy, Arsenic, and Immune Response (PAIR) Study
# Drinking Water Arsenic and Hemoglobin -- Models

# Tyler Smith
# June 1, 2023

##### Preliminaries ############################################################
# Load Libraries
import numpy as np
import pandas as pd
from statsmodels.formula.api import ols

##### Assign Formula Components ################################################
# Outcomes
y_var = {
    'VISIT1': 'SEHEMO', 
    'VISIT2': 'SVXHEMO', 
    'VISIT3': 'SMHEMO', 
    'VISIT4': 'SM3HEMO'}

# Time Covariate
adj_tim = {
    'VISIT1': 'SEGSTAGE',
    'VISIT2': 'SVXGSTAGE',
    'VISIT3': 'SMDAYSPP',
    'VISIT4': 'SM3DAYSPP'}

# Other Covariates
adj_exp = 'ln_wAs_iqr + ln_wFe_iqr'
adj_con = 'AGE + PARITY + EDUCATION + LSI + medSEMUAC + PEHCIGAR'
adj_rhs = adj_exp + ' + ' + adj_con

##### Fit Models ###############################################################
# Unadjusted: Drinking Water Arsenic
for i in ['VISIT1','VISIT2','VISIT3','VISIT4']:

    frm = y_var[i] + ' ~ ln_wAs_iqr'
    dat = df_slb[df_slb[i] == 1]
    
    mdl = ols(frm, data = dat)
    globals()[f'mdl_unaj_{i}_wAs'] = mdl.fit()
    
    print('Model for ' + i + ' has been fitted.')

# Unadjusted: Drinking Water Iron
for i in ['VISIT1','VISIT2','VISIT3','VISIT4']:

    frm = y_var[i] + ' ~ ln_wFe_iqr'
    dat = df_slb[df_slb[i] == 1]
    
    mdl = ols(frm, data = dat)
    globals()[f'mdl_unaj_{i}_wFe'] = mdl.fit()

    print('Model for ' + i + ' has been fitted.')

# Adjusted
for i in ['VISIT1','VISIT2','VISIT3','VISIT4']:

    frm = y_var[i] + ' ~ ' + adj_rhs + ' + ' + adj_tim[i]
    dat = df_slb[df_slb[i] == 1]
    
    mdl = ols(frm, data = dat).fit()

    mdl = ols(frm, data = dat)
    globals()[f'mdl_adju_{i}'] = mdl.fit()

    print('Model for ' + i + ' has been fitted.')

###### Check Model Fit #########################################################
# Unadjusted: Arsenic
diagnostic_plots(mdl_unaj_VISIT1_wAs, name = 'Visit 1, Unadjusted, Arsenic')
diagnostic_plots(mdl_unaj_VISIT2_wAs, name = 'Visit 2, Unadjusted, Arsenic')
diagnostic_plots(mdl_unaj_VISIT3_wAs, name = 'Visit 3, Unadjusted, Arsenic')
diagnostic_plots(mdl_unaj_VISIT4_wAs, name = 'Visit 4, Unadjusted, Arsenic')

# Unadjusted: Iron
diagnostic_plots(mdl_unaj_VISIT1_wFe, name = 'Visit 1, Unadjusted, Iron')
diagnostic_plots(mdl_unaj_VISIT2_wFe, name = 'Visit 2, Unadjusted, Iron')
diagnostic_plots(mdl_unaj_VISIT3_wFe, name = 'Visit 3, Unadjusted, Iron')
diagnostic_plots(mdl_unaj_VISIT4_wFe, name = 'Visit 4, Unadjusted, Iron')

# Adjusted
diagnostic_plots(mdl_adju_VISIT1, name = 'Visit 1, Adjusted')
diagnostic_plots(mdl_adju_VISIT2, name = 'Visit 2, Adjusted')
diagnostic_plots(mdl_adju_VISIT3, name = 'Visit 3, Adjusted')
diagnostic_plots(mdl_adju_VISIT4, name = 'Visit 4, Adjusted')

##### Tidy Model Output ########################################################
# Unadjusted: Drinking Water Arsenic
df_est_unaj_wAs = tidy(
    models = [
        mdl_unaj_VISIT1_wAs, 
        mdl_unaj_VISIT2_wAs, 
        mdl_unaj_VISIT3_wAs, 
        mdl_unaj_VISIT4_wAs], 
    names  = [
        'VISIT1',
        'VISIT2',
        'VISIT3',
        'VISIT4'])

print(df_est_unaj_wAs)

# Unadjusted: Drinking Water Iron
df_est_unaj_wFe = tidy(
    models = [
        mdl_unaj_VISIT1_wFe, 
        mdl_unaj_VISIT2_wFe, 
        mdl_unaj_VISIT3_wFe, 
        mdl_unaj_VISIT4_wFe], 
    names  = [
        'VISIT1',
        'VISIT2',
        'VISIT3',
        'VISIT4'])

print(df_est_unaj_wFe)

# Adjusted
df_est_adju = tidy(
    models = [
        mdl_adju_VISIT1, 
        mdl_adju_VISIT2, 
        mdl_adju_VISIT3, 
        mdl_adju_VISIT4], 
    names  = [
        'VISIT1',
        'VISIT2',
        'VISIT3',
        'VISIT4'])

print(df_est_adju)
