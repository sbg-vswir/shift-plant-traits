"""
organize the fraction cover for different samples
Ting Zheng--tzheng39@wisc.edu
"""
import numpy as np
import pandas as pd

df_sample = pd.read_csv('./data/sample_list.csv', encoding='ISO-8859-1')
fcover_class = df_sample['fractional_cover_class'].unique()
fcover_class_dict = {'<1% cover': 0, '1-10% cover': 5, '10-25% cover': 17.5, '25-50% cover': 37.5, '50-75% cover': 62.5, '75-100% cover': 87.5}

pheno_class = ['Early leaf out', 'Full leaf out', 'Flowers', 'Seeds', 'Early senescence', 'Full senescence']
exclusion_ls = ['Bulk sample']
NA_species = ['Bare', 'NPV', 'Water']
NA_pheno = ['Full senescence', 'Flowers', 'Seeds']

# Check samples in plot, locate missing records:
# drop understory rows:
df_s = df_sample.loc[df_sample['understory'] == 'No', :].reset_index(drop=True)
# drop rows with less than 1% cover:
df_s = df_s.loc[df_s['fractional_cover_class'] != '<1% cover', :].reset_index(drop=True)
# assign numeric fcover
df_s['fcover'] = ''
for key in fcover_class_dict.keys():
    df_s.loc[df_s['fractional_cover_class']==key, 'fcover'] = fcover_class_dict[key]

# add new 'type' column
df_s['type'] = ''
idx = ~df_s['species_or_type'].isin(NA_species)
df_s.loc[idx, 'type'] = 'species'

# consider the phenophase, treat 'Full senescence' as NPV
idx = df_s['phenophase'].str.contains('Full senescence')
idx[idx.isna()] = False
df_s.loc[idx, 'type'] = 'NPV'
# 'NPV' also as 'NPV'
df_s.loc[df_s['species_or_type']=='NPV', 'type'] = 'NPV'
df_s.loc[df_s['species_or_type']=='Bare', 'type'] = 'Bare'
df_s.loc[df_s['species_or_type']=='Water', 'type'] = 'Water'

# 'Flowers' as 'Flowers', seeds as seeds, flowers, seeds as flowers
df_s.loc[df_s['phenophase']=='Flowers', 'type'] = 'Flowers'
df_s.loc[df_s['phenophase']=='Seeds', 'type'] = 'Seeds'
df_s.loc[df_s['phenophase']=='Flowers, Seeds', 'type'] = 'Flowers'
df_s.to_csv('./data/sample_list_process_s1.csv', index=False)
# #### --------------------sample list diagnosis --------------------
# ## Drop Bulksample
# df_s.drop(df_s[df_s['species_or_type']=='Bulk sample'].index, inplace=True)
#
# # Locate species with no sample number
# idx = (df_s['type'] == 'species') & (df_s['sample_number'].isna())
# df_missing = df_s[idx]
# df_missing.to_csv('./data/df_missing2.csv', index=False)
#
# # Check how many of the plot has Bulk sample
# UID_bulk = df_sample.loc[df_sample['species_or_type']=='Bulk sample', 'ID']
# UID_miss = set(df_missing['ID']).difference(set(UID_bulk))
# UID_com = set(df_missing['ID']).intersection(set(UID_bulk))
#
# # df missing without bulksample
# df_missing_nobulk = df_missing.loc[df_missing['ID'].isin(UID_miss), :]
# df_missing_nobulk.to_csv('./data/df_missing_nobulk2.csv', index=False)

#### ------------------------- drop the missing cases with fcover < 10, no sample were collected for them, add info for  Elsa's trees----------------
# drop the rows with no sample number and fcover <10
df_s.loc[df_s['fcover']=='', 'fcover'] = np.nan
idx =(~df_s['sample_number'].isna()) | (df_s['fcover'] >= 10)
df_s = df_s.loc[idx, :].reset_index(drop=True)

# fill the fcover for samples from Elsa's trees
ucla_df = pd.read_csv('./data/UCLA_plotevent_all.csv')
# step 1. remove all ucla samples collected before April 1 and in Sep
idx = (ucla_df['Date']<='4/1/2022') | (ucla_df['Date'] > '8/31/2022')
sID_drop = ucla_df.loc[idx, 'sID']
df_s = df_s.loc[~df_s['ID'].isin(sID_drop), :].reset_index(drop=True)
ucla_df = ucla_df.loc[~idx, :].reset_index(drop=True)

# step 2. for each ucla plot, look for fcover and fill the gaps
plots = ucla_df['JPL_plot'].unique()
for p in plots:
    # if there is space:
    p = p.strip()
    s_sub = (df_s['plot_name'].str.strip() == p) & (df_s['type'] == 'species')
    covers = df_s.loc[s_sub, 'fcover']
    if sum(list(~covers.isna())) > 0:
        fcover = list(covers[~covers.isna()])
        fcover = fcover[0]

    df_s.loc[s_sub, 'fcover'] = fcover

df_s.to_csv('./data/sample_list_process_s2.csv', index=False)
