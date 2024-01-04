"""
Aggregate leaf level trait to plot level
Ting Zheng--tzheng39@wisc.edu
"""

import pandas as pd
import numpy as np

# include NPV sample or not:
NPV = False
# include Flowers or not:
Flowers = False
# use Bulk sample or not:
Bulk = False
# use Tally fcover or not:
Tally = False
# df_tally = pd.read_csv('./data/quadrat_tally_fcover.csv')

df_fcover = pd.read_csv('./data/sample_list_process_s2.csv')
df_t = pd.read_csv('./data/SHIFT_sample_LMA_LWC_Chl_070723.csv')
t_cols = ['sample_number', 'LWC', 'CHL_CCM', 'LMA']
traits = ['LWC', 'CHL_CCM', 'LMA']
if ~NPV:
    df_fcover = df_fcover.loc[~(df_fcover['type'] == 'NPV'), :].reset_index(drop=True)
if ~Bulk:
    df_fcover = df_fcover.loc[~(df_fcover['species_or_type'] == 'Bulk sample'), :].reset_index(drop=True)
if ~Flowers:
    df_fcover = df_fcover.loc[~(df_fcover['type'] == 'Flowers'), :].reset_index(drop=True)

# drop Bare and Seeds:
df_fcover = df_fcover.loc[~((df_fcover['type'] == 'Bare') | (df_fcover['type'] == 'Seeds')), :].reset_index(drop=True)

# join the trait to fcover by sample_number

df_merge = pd.merge(df_fcover, df_t.loc[:, t_cols], how='left', on='sample_number')



# Aggregate
for i, plot in enumerate(df_merge['ID'].unique()):
    df_sub = df_merge.loc[df_merge['ID'] == plot, :].reset_index(drop=True)
    df_temp = df_sub[['ID', 'sample_date', 'plot_name']].iloc[[0]]
    # if df_sub has more than one record, drop the rows with no fcover
    if len(df_sub) > 1:
        df_sub = df_sub.loc[~(df_sub['fcover'].isna()), :].reset_index(drop=True)
    # if not empty:
    if len(df_sub) > 0:
        df_sub['f_scaled'] = df_sub['fcover']
        idx = df_sub['f_scaled'].isna()
        if sum(idx) > 0: # one record plot with nan fcover:
            df_sub.loc[idx, 'f_scaled'] = 1
            df_temp['vege_cover'] = np.nan
        else:
            df_sub['f_scaled'] = df_sub['f_scaled']/df_sub['fcover'].sum()
            df_temp['vege_cover'] = df_sub['fcover'].sum()
        # aggregate by each trait:
        for t in traits:
            idx = (df_sub[t].isna()) | (df_sub[t] == -9999)
            # if missing value
            if sum(idx) > 0:
                df_temp[t] = np.nan
            else:
                df_temp[t] = sum(df_sub[t]*df_sub['f_scaled'])

    else:
        df_temp['vege_cover'] = np.nan
        df_temp[traits] = np.nan

    if i == 0:
        df_result = df_temp
    else:
        df_result = pd.concat((df_result, df_temp), axis=0, ignore_index=True)




