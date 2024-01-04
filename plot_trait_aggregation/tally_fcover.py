"""
calculate fraction cover based on tally sheet
Ting Zheng--tzheng39@wisc.edu
"""

import pandas as pd

df_tally = pd.read_csv('./data/quadrat_tallies.csv')

# for each unique species-phen, calculate the fcover for each corner, if not present for a certain corner, fill with 0.
# calculate final fcover by averaging four corners.
df_tally['sp_phen'] = df_tally['cover_species'] + '_' + df_tally['phenophase']
df_tally.loc[df_tally['quadrat_corner']=='NW ', 'quadrat_corner'] = 'NW'

# for each unique plot:
plots = df_tally['unique_ID'].unique()
corners = df_tally['quadrat_corner'].unique()
# columns to keep
cols = ['plot_name', 'cover_species', 'phenophase',
       'date',  'unique_ID', 'ID', 'sample_number1', 'sample_number2',
       'sample_number3', 'sample_number4', 'sp_phen']

for i, p in enumerate(plots):
    # unique sp_phen for each plot:
    sp_ls = df_tally.loc[df_tally['unique_ID'] == p, 'sp_phen'].unique()
    df_sp = pd.DataFrame(data=sp_ls, columns=['sp_phen'])
    for c in corners:
        df_sub = df_tally.loc[(df_tally['unique_ID'] == p) & (df_tally['quadrat_corner'] == c), :]
        temp = df_sub['count']/df_sub['count'].sum()
        temp = temp.to_frame(name=c)
        temp['sp_phen'] = df_sub['sp_phen']
        df_sp = pd.merge(df_sp, temp.reset_index(drop=True), on='sp_phen', how='left')

    # replace nan with 0
    df_sp = df_sp.fillna(0)
    # calculate final fcover
    df_sp['fcover'] = df_sp.loc[:, corners].mean(axis=1)

    # final df:
    df_p = df_tally.loc[df_tally['unique_ID'] == p, cols].groupby('sp_phen').first().reset_index(drop=False)
    df_p = pd.merge(df_p, df_sp, on='sp_phen', how='left')

    if i == 0:
        df_final = df_p
    else:
        df_final = pd.concat([df_final, df_p], axis=0)

df_final.to_csv('./data/quadrat_tally_fcover.csv', index=False)











