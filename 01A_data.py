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
import matplotlib.pyplot as plt
import seaborn as sns

##### Define Plotting Functions ################################################
def density_plot(data, x, xlab):
    plt.clf()
    ax = sns.kdeplot(data = data, x = x)
    ax.set(xlabel = xlab, ylabel = 'Density')
    plt.show()
    
def box_plot(data, y, ylab):
    plt.clf()
    ax = sns.boxplot(data = data, y = y)
    ax.set(xlabel = '', ylabel = ylab)
    plt.show()

##### Read Data ################################################################
# Set Working Directory
os.chdir('../../research/2024_0108_pair_data/')

# Read Data
pregtrak = pd.read_csv("j7pregtrak/pair_pregtrak_2022_0309.csv")
kidtrak  = pd.read_csv("j7kidtrak/pair_kidtrak_2022_0310.csv")
water_pe = pd.read_csv("assay_water_metals/pair_watermetals_pef_2022_1030.csv")
water_vx = pd.read_csv("assay_water_metals/pair_watermetals_vaxf_2022_1030.csv")
pefsst   = pd.read_csv("pefsst/pair_pefsst_2022_0310.csv")
vaxfsst  = pd.read_csv("vaxfsst/pair_vaxfsst_2022_0310.csv")
mdab     = pd.read_csv("mdab/pair_mdab_2022_0310.csv")
m3mopsst = pd.read_csv("m3mopsst/pair_m3mopsst_2022_0310.csv")
parity   = pd.read_csv("pair_reprohistory/pair_reprohistory_2022_0328.csv")
ses      = pd.read_csv("ses/pair_ses_2022_0310.csv")
pef      = pd.read_csv("pef/pair_pef_2022_0310.csv")
ferritin = pd.read_csv("assay_ocm/pair_ocm_2023_0328.csv")

##### Rename and Select Variables ##############################################
# J7PREGTRAK
# (From all pregnancies, keep only enrolled pregnancies.)
pregtrak = pregtrak[(pregtrak['PEF'] == 1) & (pregtrak['PEFSST'] == 1)]

pregtrak = pregtrak[[
    'UID', 
    'DOBYY', 
    'BGLMPWK']]

# J7KIDTRAK
# (Standardize name of UID for joining.)
kidtrak = kidtrak.rename(columns = {
    'MOMUID': 'UID'})

kidtrak = kidtrak[[
    'UID', 
    'CHILDUID', 
    'CHILDDOB']]

# Drinking Arsenic and Iron
water_pe = water_pe[[
    'UID', 
    'PE_wMetals_As', 
    'PE_wMetals_Fe']]
  
water_vx = water_vx[[
    'UID', 
    'VX_wMetals_As', 
    'VX_wMetals_Fe']]

# PEFSST
pefsst = pefsst[[
    'UID',
    'SESTATUS',
    'SEDATE',
    'SEWKINT',
    'SEHEMO',
    'SEFETABS',
    'medSEMUAC']]

# VAXFSST
vaxfsst = vaxfsst[[
    'UID',
    'SVXSTATUS',
    'SVXDATE',
    'SVXWKINT',
    'SVXHEMO',
    'SVXFETABS']]

# MDAB
mdab = mdab[[
    'UID',
    'SMSTATUS',
    'SMDATE',
    'SMWKINT',
    'SMHEMO',
    'SMFETABS']]

# M3MOPSST
m3mopsst = m3mopsst[[
    'UID',
    'SM3STATUS',
    'SM3DATE',
    'SM3WKINT',
    'SM3HEMO',
    'SM3FETABS']]

# Parity
# (Simplify variable name.)
parity = parity.rename(columns = {
    'FDPSR_PARITY': 'PARITY'})
  
parity = parity[[
    'UID',
    'PARITY']]

# SES
# (Simplify and standardize variable names.)
ses = ses.rename(columns = {
    'wehclass_mc2': 'EDUCATION', 
    'lsi': 'LSI'})

ses = ses[[
    'UID',
    'EDUCATION',
    'LSI']]

# PEF
pef = pef[[
    'UID',
    'PEHCIGAR']]

# Plasma Ferritin
ferritin = ferritin[[
    'UID',
    'SEFER']]

##### Join Data ################################################################
# Join Data
# (Join data frames on UID, which is inferred as key.)
df = pregtrak.merge(kidtrak, how = 'left') \
    .merge(water_pe, how = 'left') \
    .merge(water_vx, how = 'left') \
    .merge(pefsst,   how = 'left') \
    .merge(vaxfsst,  how = 'left') \
    .merge(mdab,     how = 'left') \
    .merge(m3mopsst, how = 'left') \
    .merge(parity,   how = 'left') \
    .merge(ses,      how = 'left') \
    .merge(pef,      how = 'left') \
    .merge(ferritin, how = 'left')

# Set Index
#df = df.set_index('UID')

# Format Dates
for i in ['CHILDDOB','SEDATE','SVXDATE','SMDATE','SM3DATE']:
  df[i] = pd.to_datetime(df[i])

# Inspect Data
df.head()

# Remove Data Objects
del pregtrak
del kidtrak
del water_pe
del water_vx 
del pefsst
del vaxfsst
del mdab
del m3mopsst
del parity
del ses
del pef
del ferritin

##### Limit to 1 Row/Woman #####################################################
# Indicate Live Birth
df['LIVEBIRTH'] = np.where(df['CHILDUID'].notna(), 1, 0)
df.value_counts('LIVEBIRTH')

# Indicate Singleton
# (Count Live Births/Pregnant Woman)
births = pd.DataFrame()
births['BIRTHCOUNT'] = df.groupby('UID')['UID'].size()

df = df.merge(
    births, 
    left_on = 'UID', 
    left_index = False,
    right_on = births.index, 
    right_index = True)
    
# (Indicate Singleton)
df['SINGLETON'] = np.where((df['LIVEBIRTH'] == 1), 1, pd.NA)
df['SINGLETON'] = np.where((df['LIVEBIRTH'] == 1) & (df['BIRTHCOUNT'] > 1), 0, df['SINGLETON'])

# Reduce to 1 Row/Pregnant Woman
df = df.sort_values(['UID','CHILDDOB']).groupby('UID').first()

# Check Counts
df['LIVEBIRTH'].value_counts(dropna = False)
df.groupby('LIVEBIRTH')['SINGLETON'].value_counts(dropna = False)

del df['BIRTHCOUNT'], births

# Inspect Data
df.head()

##### Prepare Hemoglobin #######################################################
# Convert to Numeric
df['SVXHEMO'] = df['SVXHEMO'].str.replace("$", "")
df['SVXHEMO'] = pd.to_numeric(df['SVXHEMO'], errors = 'coerce')

# Standardize Missing Values
for i in ['SEHEMO','SVXHEMO','SMHEMO','SM3HEMO']:
    df[i] = np.where(df[i] == 99.9, pd.NA, df[i])
    
# Set Erroneous Hemoglobin Value to Missing
df['SEHEMO'] = np.where(df['SEHEMO'] > 16, pd.NA, df['SEHEMO'])

# Drop if Given Iron Supplements
for i in ['SEFETABS','SVXFETABS','SMFETABS','SM3FETABS']:
    print(df.value_counts(i, dropna = False))
    
# Visit 1/PEF
for i in ['SVXHEMO','SMHEMO','SM3HEMO']:
    df[i] = np.where(df['SEFETABS'] == 1, pd.NA, df[i])

# Visit 3/MDAB
df['SM3HEMO'] = np.where(df['SMFETABS'] == 1, pd.NA, df['SM3HEMO'])

##### Prepare Drinking Water Elements ##########################################
# Drinking Water Arsenic
df['wAs'] = np.where(
    # if arsenic at visit 1 is missing
    np.isnan(df['PE_wMetals_As']), 
  
    # use arsenic at visit 2
    df['VX_wMetals_As'], 
  
    # else use arsenic at visit 1
    df['PE_wMetals_As'])

# Drinking Water Iron
df['wFe'] = np.where(
    # if iron at visit 1 is missing
    np.isnan(df['PE_wMetals_Fe']), 
    
    # use iron at visit 2
    df['VX_wMetals_Fe'], 
    
    # else use iron at visit 1
    df['PE_wMetals_Fe'])
  
df['wFe'] = np.where(
    # if iron at visit 1 is erroneous (based on feedback from lab)
    df['PE_wMetals_Fe'] > 284000, 
    
    # use iron at visit 2
    df['VX_wMetals_Fe'],
    
    # else use iron at visit 1
    df['wFe'])

# Log-transform Drinking Water Elements
df['ln_wAs'] = np.log(df['wAs'])
df['ln_wFe'] = np.log(df['wFe'])

# Check Missingness
df['wAs'].groupby(df['wAs'].isnull()).count()
df['wFe'].groupby(df['wFe'].isnull()).count()

# Check Distributions
density_plot(data = df, x = 'wAs', 
    xlab = "Drinking Water Arsenic (µg/L)")
density_plot(data = df, x = 'wFe', 
    xlab = "Drinking Water Iron (µg/L)")

density_plot(data = df, x = 'ln_wAs', 
    xlab = "Drinking Water Arsenic (µg/L)")
density_plot(data = df, x = 'ln_wFe', 
    xlab = "Drinking Water Iron (µg/L)")

##### Maternal Age #############################################################
# Check Source Variables 
df['SEYEAR'] = df['SEDATE'].dt.year

# (Missingness)
df['SEYEAR'].isna().value_counts()
df['DOBYY'].isna().value_counts()

# (Values)
df['SEYEAR'].value_counts()
    
# Derive Maternal Age 
df['AGE'] = df['SEYEAR'] - df['DOBYY']

# Check Distribution
box_plot(data = df, y = 'AGE', 
    ylab = 'Maternal Age (years)')

density_plot(data = df, x = 'AGE', 
    xlab = 'Maternal Age (years)')

##### Gestational Age (Visits 1-2) #############################################
# Check Source Variables
box_plot(data = df, y = 'BGLMPWK', 
    ylab = 'J-Week at LMP')

box_plot(data = df, y = 'SEWKINT', 
    ylab = 'J-Week at Visit 1/PEF')
    
box_plot(data = df, y = 'SVXWKINT', 
    ylab = 'J-Week at Visit 2/VAXF')

# Derive Gestational Ages
df['SEGSTAGE']  = df['SEWKINT']  - df['BGLMPWK']
df['SVXGSTAGE'] = df['SVXWKINT'] - df['BGLMPWK']

# Check Values
df['SEGSTAGE'].value_counts(dropna = False)
df['SVXGSTAGE'].value_counts(dropna = False)

##### Days Postpartum (Visits 3-4) #############################################
# Check Source Variables
box_plot(data = df, y = 'CHILDDOB', ylab = 'Child Date of Birth')
box_plot(data = df, y = 'SMDATE', ylab = 'Date at Visit 3/MDAB')
box_plot(data = df, y = 'SM3DATE', ylab = 'Date at Visit 4/M3MOP')
    
# Derive Days Postpartum
df['SMDAYSPP']  = (df['SMDATE']  - df['CHILDDOB']).dt.days
df['SM3DAYSPP'] = (df['SM3DATE'] - df['CHILDDOB']).dt.days

# Check Distributions
box_plot(data = df, y = 'SMDAYSPP', ylab = 'Days Postpartum Visit 3/MDAB')
box_plot(data = df, y = 'SM3DAYSPP', ylab = 'Days Postpartum at Visit 4/M3MOP')

##### Parity ###################################################################
# Top-code Parity (0, 1, 2)
df['PARITY'] = np.where(df['PARITY'] > 2, 2, df['PARITY'])

# Label Parity (Nulliparous, Primiparous, Multiparous)
df['PARITY'] = df['PARITY'].astype('category')

tmp_parity = {
    0: 'Nulliparous',
    1: 'Primiparous',
    2: 'Multiparous'}
    
df['PARITY'] = df['PARITY'].cat.rename_categories(tmp_parity)

del tmp_parity

# Check Values
df['PARITY'].value_counts(sort = False, dropna = False)

##### Education ################################################################
# Top-code Education
df['EDUCATION'] = np.where(df['EDUCATION'] > 2, 2, df['EDUCATION'])

# Label Education (None, Class 1-0, Class ≥10)
df['EDUCATION'] = df['EDUCATION'].astype('category')

tmp_edu = {
    0: 'None', 
    1: 'Class 1-9', 
    2: 'Class ≥10'}

df['EDUCATION'] = df['EDUCATION'].cat.rename_categories(tmp_edu)

del tmp_edu

# Check Values
df['EDUCATION'].value_counts(sort = False, dropna = False)

##### Living Standards Index ###################################################
# Check Distributions
box_plot(
    data = df, 
    y = 'LSI', 
    ylab = 'Living Standards Index')

density_plot(
    data = df, 
    x = 'LSI', 
    xlab = 'Living Standards Index')

##### Mid-upper Arm Circumference ##############################################
# Check Distributions
box_plot(
    data = df, 
    y = 'medSEMUAC', 
    ylab = 'Mid-upper Arm Circumference (cm)')

density_plot(
    data = df, 
    x = 'medSEMUAC', 
    xlab = 'Mid-upper Arm Circumference (cm)')

##### Husband's Smoking ########################################################
# Label Husband's Smoking (Yes/No)
df['PEHCIGAR'] = df['PEHCIGAR'].astype('category')

tmp_smoke = {
    0: 'No',
    1: 'Yes'}
    
df['PEHCIGAR'] = df['PEHCIGAR'].cat.rename_categories(tmp_smoke)

del tmp_smoke

# Check Values
df['PEHCIGAR'].value_counts(sort = False, dropna = False)

##### Plasma Ferritin ##########################################################
# Log-transform Plasma Ferritin
df['ln_SEFER'] = np.log(df['SEFER'])

# Check Distributions
density_plot(data = df, x = 'SEFER', xlab = "Plasma Ferritin (ng/mL)")
density_plot(data = df, x = 'ln_SEFER', xlab = "Plasma Ferritin (ng/mL)")

##### Prepare Final Data Set ###################################################
df.head()
