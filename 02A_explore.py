################################################################################
# Pregnancy, Arsenic, and Immune Response (PAIR) Study
# Drinking Water Arsenic and Hemoglobin -- Explore

# Tyler Smith
# May 31, 2023

##### Preliminaries ############################################################
# Load Libraries
import numpy as np
import pandas as pd
from tableone import TableOne
import openpyxl

##### Set Columns ##############################################################
# Set Columns
columns = [
    'AGE',
    'PARITY',
    'EDUCATION',
    'LSI',
    'medSEMUAC',
    'PEHCIGAR',
    'wAs',
    'wFe',
    'SEGSTAGE',
    'SVXGSTAGE',
    'SMDAYSPP',
    'SM3DAYSPP']

# Indicate Continuous Variables
continuous = [
    'AGE',
    'LSI',
    'medSEMUAC',
    'wAs',
    'wFe',
    'SEGSTAGE',
    'SVXGSTAGE',
    'SMDAYSPP',
    'SM3DAYSPP']

# Indicate Categorical Variables
categorical = [
    'PARITY',
    'EDUCATION',
    'PEHCIGAR']

##### Generate Columns #########################################################
for i in ['VISIT1','VISIT2','VISIT3','VISIT4']:
    out = TableOne(df_slb[df_slb[i] == 1].copy(), 
        columns = columns, continuous = continuous, categorical = categorical,
            nonnormal = continuous)
    
    file_name = 'table1_' + i + '.xlsx'
    out.to_excel('../../portfolio/arsenic_hemo/tables/' + file_name)
    
del columns, continuous, categorical, file_name, out

