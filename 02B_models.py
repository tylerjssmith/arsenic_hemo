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

##### Unadjusted ###############################################################
# Drinking Water Arsenic
tmp = df_slb[['SEHEMO','SVXHEMO','SMHEMO','SM3HEMO','ln_wAs_iqr']]\
    .melt(id_vars = 'ln_wAs_iqr')\
    .rename(columns = {
        'variable': 'VISIT',
        'value': 'HEMO'})

tmp.head()

for i in ['SEHEMO','SVXHEMO','SMHEMO','SM3HEMO']:

    data = tmp[tmp['VISIT'] == i]

    md_unaj = ols('HEMO ~ ln_wAs_iqr', data = data)
    md_unaj = md_unaj.fit()
    
    print(md_unaj.params)

# Drinking Water Iron
tmp = df_slb[['SEHEMO','SVXHEMO','SMHEMO','SM3HEMO','ln_wFe_iqr']]\
    .melt(id_vars = 'ln_wFe_iqr')\
    .rename(columns = {
        'variable': 'VISIT',
        'value': 'HEMO'})

tmp.head()

for i in ['SEHEMO','SVXHEMO','SMHEMO','SM3HEMO']:

    data = tmp[tmp['VISIT'] == i]

    md_unaj = ols('HEMO ~ ln_wFe_iqr', data = data)
    md_unaj = md_unaj.fit()
    
    print(md_unaj.params)

##### Adjusted #################################################################
