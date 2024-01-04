"""
Comparing the fraction cover from tally sheet and plot survey
Ting Zheng--tzheng39@wisc.edu
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import seaborn as sns



####--------------------temp, preliminary comparison between sample fcover and tally fcover---------------

df_tally = pd.read_csv('./data/quadrat_tally_fcover.csv')
df_s = pd.read_csv('./data/sample_list_process_s2.csv')
# fix the inconsistency in the phenophase:
df_tally.loc[df_tally['phenophase'] == 'Seeds', 'phenophase'] = 'seeds'
df_tally.loc[df_tally['phenophase'] == 'full leaf out ', 'phenophase'] = 'full leaf out'
df_tally.loc[df_tally['phenophase'] == 'na ', 'phenophase'] = 'na'
pheno = df_tally['phenophase'].unique()

# drop records with no sample number for both df:
df_tally = df_tally.loc[~df_tally['sample_number1'].isna(), :]
df_s = df_s.loc[~df_s['sample_number'].isna(), :]
# join by sample number
df_comp = pd.merge(df_tally, df_s.loc[:, ['sample_number', 'fcover']], left_on='sample_number1', right_on='sample_number', how='inner')
# drop rows with fcover is na
df_comp = df_comp.loc[~df_comp['fcover_y'].isna(), :].reset_index(drop=True)
# calculate the sd for fcover_x
std = np.std(df_comp.loc[:, ['NE', 'NW', 'SE', 'SW']].values, axis=1)
df_comp['fcover_x_sd'] = std
df_comp['fcover_x'] = df_comp['fcover_x']*100
df_comp['fcover_x_sd'] = df_comp['fcover_x_sd']*100

# plotting
fig, ax = plt.subplots(figsize=(4, 4))
ax.errorbar(df_comp['fcover_y'], df_comp['fcover_x'], yerr=df_comp['fcover_x_sd'], fmt='o')
plt.show()
# melt the df_comp for sns:
# df_plot = pd.melt(df_comp, id_vars='sample_number', value_vars=['NE', 'NW', 'SE', 'SW'])
# cols = df_comp.columns
# rm = ['NE', 'NW', 'SE', 'SW']
# cols = [x for x in cols if x not in rm]
# df_plot = pd.merge(df_plot, df_comp.loc[:, cols], on='sample_number', how='left')
#
# sns.scatterplot(data=df_plot, x='fcover_y', y='value', hue='sample_number')
# sns.scatterplot(data=df_plot, x='fcover_y', y='fcover_x', hue='sample_number')
# plt.show()
# only compare full leaf out:
idx = df_comp['phenophase'] == 'full leaf out'
df_sub = df_comp[idx]
# plotting
# create color for each observation
sites = df_sub['unique_ID'].unique()
color = cm.rainbow(np.linspace(0, 1, len(sites)))
df_cm = pd.DataFrame(data=color, columns=['a', 'b', 'c', 'd'])
df_cm['unique_ID'] = sites
df_sub_merge = pd.merge(df_sub, df_cm, on='unique_ID',  how='left')
color = df_sub_merge.loc[:, ['a', 'b', 'c', 'd']].values
fig, ax = plt.subplots(figsize=(4, 4))
for i, site in enumerate(sites):
    idx = df_sub['unique_ID'] == site
    ax.errorbar(df_sub.loc[idx, 'fcover_y'], df_sub.loc[idx, 'fcover_x'], yerr=df_sub.loc[idx, 'fcover_x_sd'], fmt='o', alpha=0.3)#c=color[i,:])
plt.show()

