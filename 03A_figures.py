################################################################################
# Pregnancy, Arsenic, and Immune Response (PAIR) Study
# Drinking Water Arsenic and Hemoglobin -- Figures

# Tyler Smith
# June 2, 2023

##### Preliminaries ############################################################
# Load Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Seaborn Theme
sns.set_style('white')
sns.set_context('notebook')

##### Figure: Drinking Water Arsenic and Iron ##################################
# Box Plots
fig, axes = plt.subplots(2, 2)

fig.suptitle('Drinking Water Arsenic and Iron\nOriginal and Log Scales')

sns.boxplot(ax=axes[0, 0], data=df_slb, y='wAs',
    width = 0.4, color = 'white', linecolor = 'black')
sns.boxplot(ax=axes[0, 1], data=df_slb, y='ln_wAs',
    width = 0.4, color = 'white', linecolor = 'black')
sns.boxplot(ax=axes[1, 0], data=df_slb, y='wFe',
    width = 0.4, color = 'white', linecolor = 'black')
sns.boxplot(ax=axes[1, 1], data=df_slb, y='ln_wFe',
    width = 0.4, color = 'white', linecolor = 'black')

axes[0, 0].set(
    ylabel = 'Arsenic')
axes[0, 1].set(
    ylabel = 'Log Arsenic')
axes[1, 0].set(
    ylabel = 'Iron')
axes[1, 1].set(
    ylabel = 'Log Iron')

plt.show()

# Density Plots
# (Arsenic)
fig, axes = plt.subplots(1, 2)

fig.suptitle('Drinking Water Arsenic\nOriginal and Log Scales')

sns.kdeplot(ax=axes[0], data=df_slb, x='wAs',
    color = 'black')
sns.kdeplot(ax=axes[1], data=df_slb, x='ln_wAs',
    color = 'black')

axes[0].set(
    xlabel = 'Original', 
    ylabel = 'Density')
axes[1].set(
    xlabel = 'Log', 
    ylabel = None)

plt.show()
    
# (Iron)
fig, axes = plt.subplots(1, 2)

fig.suptitle('Drinking Water Iron\nOriginal and Log Scales')

sns.kdeplot(ax=axes[0], data=df_slb, x='wFe',
    color = 'black')
sns.kdeplot(ax=axes[1], data=df_slb, x='ln_wFe',
    color = 'black')

axes[0].set(
    xlabel = 'Original', 
    ylabel = 'Density')
axes[1].set(
    xlabel = 'Log', 
    ylabel = None)

plt.show()

##### Figure: Hemoglobin by Visit ##############################################
# Extract Data
df_fig = df_slb[['SEHEMO','SVXHEMO','SMHEMO','SM3HEMO']]\
    .reset_index()\
    .melt(id_vars = 'UID')\
    .rename(columns = {
        'variable': 'Visit',
        'value'   : 'HEMO'})

df_fig.head()

# Prepare Visit Names
df_fig['Visit'] = df_fig['Visit'].astype('category')

df_fig.dtypes

df_fig['Visit'] = df_fig['Visit']\
    .cat\
    .rename_categories({
        'SEHEMO'  : 'Visit 1', 
        'SVXHEMO' : 'Visit 2', 
        'SMHEMO'  : 'Visit 3', 
        'SM3HEMO' : 'Visit 4'})

df_fig['Visit'] = df_fig['Visit']\
    .cat\
    .reorder_categories(new_categories = [
        'Visit 1',
        'Visit 2',
        'Visit 3',
        'Visit 4'])

df_fig.head()

# Generate Figure
fig = plt.figure()

g = sns.kdeplot(data = df_fig, x = 'HEMO', hue = 'Visit',
    fill = True)

g.set_title('Maternal Hemoglobin by Study Visit\n\
    PAIR Study, Gaibandha District, Bangladesh, 2018-2019')
g.set_xlabel('Hemoglobin (g/dL)')
g.set_ylabel('Density')

plt.savefig('../../portfolio/arsenic_hemo/figures/hemo_by_study_visit.png',
    dpi = 400, bbox_inches = 'tight')

##### Figure: Hemoglobin by Gestational Week ###################################
# Prepare Data
# (Select Variables)
df_fig = df_slb.reset_index()

df_fig = df_fig[[
    'UID',
    'SEGSTAGE',
    'SVXGSTAGE',
    'SEHEMO',
    'SVXHEMO']]

df_fig.head()

# (Reshape Data)
df_fig = pd.melt(df_fig, 
    id_vars = [
        'UID',
        'SEGSTAGE',
        'SVXGSTAGE'])
        
df_fig = df_fig.rename(
    columns = {
        'variable': 'Visit', 
        'value'   : 'HEMO'})

df_fig.head()

# (Prepare Visit)
df_fig['WEEK'] = np.where(
    df_fig['Visit'] == 'SEHEMO', 
        df_fig['SEGSTAGE'], df_fig['SVXGSTAGE'])

df_fig['Visit'] = df_fig['Visit'].astype('category')

df_fig['Visit'] = df_fig['Visit']\
    .cat\
    .rename_categories({
        'SEHEMO':  'Visit 1',
        'SVXHEMO': 'Visit 2'})

# (Select Final Variables)
df_fig = df_fig[['UID','Visit','WEEK','HEMO']]
df_fig.head()

# Make Figure
fig = plt.figure()

g1 = sns.relplot(
    x = 'WEEK', y = 'HEMO', hue = 'Visit', data = df_fig, 
    kind = 'scatter', alpha = 0.4)

g2 = sns.regplot(
    x = 'WEEK', y = 'HEMO',  data = df_fig,
        lowess = True, scatter = False, 
        line_kws = {'color': 'black'})
    
g1.set(title = 'Maternal Hemoglobin in Pregnancy by Study Visit\n\
PAIR Study, Gaibandha District, Bangladesh, 2018-2019')
    
g1.set_axis_labels(
    x_var = 'Gestational Age (weeks)',
    y_var = 'Hemoglobin (g/dL)')

plt.savefig('../../portfolio/arsenic_hemo/figures/hemo_by_gestational_age.png',
    dpi = 400, bbox_inches = 'tight')

##### Figure: Hemoglobin by Drinking Water Arsenic and Iron ####################
# Scatter Plots
fig, (ax1, ax2) = plt.subplots(ncols = 2, sharey = True)

g1 = sns.regplot(ax = ax1, x = 'ln_wAs', y = 'SEHEMO', data = df_slb,
    lowess = True, scatter = True, line_kws = {'color': 'black'},
    scatter_kws = {'color': 'gray', 'alpha': 0.4})

g2 = sns.regplot(ax = ax2, x = 'ln_wFe', y = 'SEHEMO', data = df_slb,
    lowess = True, scatter = True, line_kws = {'color': 'black'},
    scatter_kws = {'color': 'gray', 'alpha': 0.4})

fig.suptitle('Hemoglobin at Visit 1 by Drinking Water Arsenic and Iron\n\
PAIR Study, Gaibandha District, Bangladesh, 2018-2019')

g1.set_xlabel('Log Drinking Water Arsenic (µg/L)')
g2.set_xlabel('Log Drinking Water Iron (µg/L)')

g1.set_ylabel('Hemoglobin (g/dL)')
g2.set_ylabel('Hemoglobin (g/dL)')

plt.show()

plt.savefig('../../portfolio/arsenic_hemo/figures/hemo_by_arsenic_iron.png',
    dpi = 400, bbox_inches = 'tight')


