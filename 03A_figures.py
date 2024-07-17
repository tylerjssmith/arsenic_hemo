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
    .melt()\
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
fig, axes = plt.subplots()

fig.suptitle('Maternal Hemoglobin by Study Visit')

sns.kdeplot(data = df_fig, x = 'HEMO', hue = 'Visit',
    fill = True)

axes.set(
    xlabel = 'Hemoglobin (g/dL)',
    ylabel = 'Density')

plt.show()

##### Figure: Hemoglobin by Gestational Week ###################################
# Prepare Data
# (Select Variables)
df_fig = df_slb[[
    'SEGSTAGE',
    'SVXGSTAGE',
    'SEHEMO',
    'SVXHEMO']]

# (Reshape Data)
df_fig = pd.melt(df_fig, 
    id_vars = [
        'SEGSTAGE',
        'SVXGSTAGE'])
        
df_fig = df_fig.rename(
    columns = {
        'variable': 'Visit', 
        'value'   : 'HEMO'})

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
df_fig = df_fig[['Visit','WEEK','HEMO']]
df_fig.head()

# Make Figure
fig, axes = plt.subplots()

g = sns.scatterplot(
    x = 'WEEK', y = 'HEMO', hue = 'Visit', data = df_fig,
        alpha = 0.4)
    
g.set_title('Maternal Hemoglobin by Gestational Age')
g.set_xlabel('Gestational Age (weeks)')
g.set_ylabel('Hemoglobin (g/dL)')

plt.show()

##### Figure: Hemoglobin by Drinking Water Arsenic and Iron ####################
# Scatter Plots
fig, ax = plt.subplots(1, 2)

ax[0].plot(df['ln_wAs'], df['SEHEMO'],
    marker = 'o', markersize = 4, linestyle = 'None', 
    alpha = 0.4, color = 'gray')

ax[1].plot(df['ln_wFe'], df['SEHEMO'],
    marker = 'o', markersize = 4, linestyle = 'None', 
    alpha = 0.4, color = 'gray')

ax[0].set_title('Arsenic')
ax[1].set_title('Iron')

fig.suptitle('Hemoglobin by Drinking Water Arsenic and Iron at Visit 1')

plt.show()

##### Figure: Plasma Ferritin by Drinking Water Iron ###########################
# Scatter Plots
fig, ax = plt.subplots(1, 2)

ax[0].plot(df['wFe'], df['SEFER'],
    marker = 'o', markersize = 4, linestyle = 'None', 
    alpha = 0.4, color = 'blue')

ax[1].plot(df['ln_wFe'], df['ln_SEFER'],
    marker = 'o', markersize = 4, linestyle = 'None', 
    alpha = 0.4, color = 'orange')

ax[0].set_title('Original')
ax[1].set_title('Log')

fig.suptitle('Plasma Ferritin by Drinking Water Iron in Pregnancy by Scale')
fig.supxlabel('Drinking Water Iron (µg/L)')
fig.supylabel('Plasma Ferritin (ng/mL)')

plt.show()

##### Figure: Linear Regression Estimates ######################################

