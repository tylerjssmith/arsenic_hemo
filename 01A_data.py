################################################################################
# Pregnancy, Arsenic, and Immune Response (PAIR) Study
# Drinking Water Arsenic and Hemoglobin -- Data

# Tyler Smith
# May 29, 2023

##### Preliminaries ############################################################
# Import Libraries
import os
import numpy as np
import pandas as pd

# Set Working Directory
os.chdir('../../research/2024_0108_pair_data/')

##### Read Data ################################################################
pregtrak = pd.read_csv("j7pregtrak/pair_pregtrak_2022_0309.csv")
kidtrak = pd.read_csv("j7kidtrak/pair_kidtrak_2022_0310.csv")
water_pe = pd.read_csv("assay_water_metals/pair_watermetals_pef_2022_1030.csv")
water_vx = pd.read_csv("assay_water_metals/pair_watermetals_vaxf_2022_1030.csv")
pefsst = pd.read_csv("pefsst/pair_pefsst_2022_0310.csv")
vaxfsst = pd.read_csv("vaxfsst/pair_vaxfsst_2022_0310.csv")
mdab = pd.read_csv("mdab/pair_mdab_2022_0310.csv")
m3mopsst = pd.read_csv("m3mopsst/pair_m3mopsst_2022_0310.csv")
parity = pd.read_csv("pair_reprohistory/pair_reprohistory_2022_0328.csv")
ses = pd.read_csv("ses/pair_ses_2022_0310.csv")
pef = pd.read_csv("pef/pair_pef_2022_0310.csv")
ferritin = pd.read_csv("assay_ocm/pair_ocm_2023_0328.csv")

##### Select Variables #########################################################
# J7PREGTRAK
pregtrak = pregtrak.loc[(pregtrak['PEF'] == 1) & (pregtrak['PEFSST'] == 1), :] 
pregtrak = pregtrak.loc[:, ['UID', 'DOBYY', 'BGLMPWK']]

# J7KIDTRAK
kidtrak = kidtrak.rename(columns = {'MOMUID': 'UID'})
kidtrak = kidtrak.loc[:, ['UID', 'CHILDUID', 'CHILDDOB']]

# Drinking Arsenic and Iron
water_pe = water_pe.loc[:, ['UID', 'PE_wMetals_As', 'PE_wMetals_Fe']]
water_vx = water_vx.loc[:, ['UID', 'VX_wMetals_As', 'VX_wMetals_Fe']]

# PEFSST
pefsst = pefsst.loc[:, ['UID','SESTATUS','SEDATE','SEWKINT','SEHEMO','SEFETABS','medSEMUAC']]

# VAXFSST
vaxfsst = vaxfsst.loc[:, ['UID','SVXSTATUS','SVXDATE','SVXWKINT','SVXHEMO','SVXFETABS']]

# MDAB
mdab = mdab.loc[:, ['UID','SMSTATUS','SMDATE','SMWKINT','SMHEMO','SMFETABS']]

# M3MOPSST
m3mopsst = m3mopsst.loc[:, ['UID','SM3STATUS','SM3DATE','SM3WKINT','SM3HEMO','SM3FETABS']]

# Parity
parity = parity.rename(columns = {'FDPSR_PARITY': 'PARITY'})
parity = parity.loc[:, ['UID','PARITY']]

# SES
ses = ses.rename(columns = {'wehclass_mc2': 'EDUCATION', 'lsi': 'LSI'})
ses = ses.loc[:, ['UID','EDUCATION','LSI']]

# PEF
pef = pef.loc[:, ['UID','PEHCIGAR']]

# Plasma Ferritin
ferritin = ferritin.loc[:, ['UID','SEFER']]

##### Join Data ################################################################
df = pd.merge(pregtrak, kidtrak, on = "UID", how = "left")
df = pd.merge(df, water_pe, on = "UID", how = "left")
df = pd.merge(df, water_vx, on = "UID", how = "left")
df = pd.merge(df, pefsst, on = "UID", how = "left")
df = pd.merge(df, vaxfsst, on = "UID", how = "left")
df = pd.merge(df, mdab, on = "UID", how = "left")
df = pd.merge(df, m3mopsst, on = "UID", how = "left")
df = pd.merge(df, parity, on = "UID", how = "left")
df = pd.merge(df, ses, on = "UID", how = "left")
df = pd.merge(df, pef, on = "UID", how = "left")
df = pd.merge(df, ferritin, on = "UID", how = "left")

df.head()

# Remove Data Objects
del pregtrak, kidtrak, water_pe, water_vx, 
del pefsst, vaxfsst, mdab, m3mopsst, 
del parity, ses, pef, ferritin

##### Limit to 1 Row/Woman #####################################################
# Indicate Live Birth
df['LIVEBIRTH'] = np.where(pd.notna(df['CHILDUID']), 1, 0)

# Indicate Singleton Live Birth
singleton = pd.DataFrame(columns = ['COUNT'])
singleton['COUNT'] = df.groupby('UID')['UID'].count()

df = pd.merge(df, singleton, left_on = 'UID', right_on = singleton.index, how = 'left')

df['SINGLETON'] = np.where((df['LIVEBIRTH'] == 1) & (df['COUNT'] == 1), 1, np.nan)
df['SINGLETON'] = np.where((df['LIVEBIRTH'] == 1) & (df['COUNT'] != 1), 0, df['SINGLETON'])

del singleton, df['COUNT']

# Reduce to 1 Row/Pregnant Woman
df = df.sort_values(['UID','CHILDDOB']).groupby('UID').first()

df.head()

##### Prepare Hemoglobin #######################################################
# Convert to Numeric

# Standardize Missing Values

# Set Erroneous Hemoglobin Value to Missing

# Drop if Given Iron Supplements

# (Iron Supplements at Visit 1/PEF)

# (Iron Supplements at Visit 3/MDAB)

##### Prepare Drinking Water Elements ##########################################
df['wAs'] = np.where(np.isnan(df['PE_wMetals_As']), df['VX_wMetals_As'], df['PE_wMetals_As'])
df['wFe'] = np.where(np.isnan(df['PE_wMetals_Fe']), df['VX_wMetals_Fe'], df['PE_wMetals_Fe'])
df['wFe'] = np.where(df['PE_wMetals_Fe'] > 284000, df['VX_wMetals_Fe'], df['wFe'])

df['wAs'].groupby(df['wAs'].isnull()).count()
df['wFe'].groupby(df['wFe'].isnull()).count()

df['ln_wAs'] = np.log(df['wAs'])
df['ln_wFe'] = np.log(df['wFe'])

df.head()

##### Maternal Age #############################################################
df['SEDATE'] = pd.to_datetime(df['SEDATE'])
df['SEYEAR'] = df['SEDATE'].dt.year

df['AGE'] = df['SEYEAR'] - df['DOBYY']

def simple_range(var):
  tmp = df.loc[:, var].agg(['min','max'])
  return tmp

simple_range('AGE')

##### Gestational Age (Visits 1-2) #############################################
df['SEGSTAGE']  = df['SEWKINT']  - df['BGLMPWK']
df['SVXGSTAGE'] = df['SVXWKINT'] - df['BGLMPWK']

def simple_count(var):
  tmp = df.loc[:, var].groupby(df[var]).agg(['count'])
  return tmp

simple_count('SEGSTAGE')
simple_count('SVXGSTAGE')

##### Days Postpartum (Visits 3-4) #############################################
df['SMDATE']   = pd.to_datetime(df['SMDATE'])
df['SM3DATE']  = pd.to_datetime(df['SM3DATE'])
df['CHILDDOB'] = pd.to_datetime(df['CHILDDOB'])

df['SMDAYSPP']  = (df['SMDATE']  - df['CHILDDOB']).dt.days
df['SM3DAYSPP'] = (df['SM3DATE'] - df['CHILDDOB']).dt.days

##### Parity ###################################################################
df['PARITY'] = np.where(df['PARITY'] > 2, 2, df['PARITY'])

simple_count('PARITY')

##### Education ################################################################
df['EDUCATION'] = np.where(df['EDUCATION'] > 2, 2, df['EDUCATION'])

simple_count('EDUCATION')

##### Living Standards Index ###################################################

##### Mid-upper Arm Circumference ##############################################

##### Husband's Smoking ########################################################
simple_count('PEHCIGAR')

##### Plasma Ferritin ##########################################################
df['ln_SEFER'] = np.log(df['SEFER'])

##### Prepare Final Data Set ###################################################
df.head()
