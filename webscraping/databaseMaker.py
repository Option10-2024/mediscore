# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
from operator import itemgetter
from itertools import chain
from sorting_techniques import pysort
import copy

import funcs
import binarysearch as bs

# %%
lst_alpha_urls = funcs.CreateListAlphabeticalURLs()
print('-- Got URLs by letter -- \n')
all_drugs_urls = funcs.getAllDrugsUrls(lst_alpha_urls)
print('-- Fetching all the summaries -- \n')
all_summaries = funcs.getSummary(all_drugs_urls)
janus_len = sum(len(s) for s in all_summaries)
print('Done!\nFetched ' + str(janus_len) + ' drugs from janusinfo.se')

# %%
# Reformat data & sanity check
# -- Flatten 2D lists into 1D lists
drug_names = []
summary_1d = []

for i in range(len(all_drugs_urls)):
    for j in range(len(all_drugs_urls[i])):
        drug_name = all_drugs_urls[i][j].split('/')[-1].split('.')[0]
        summary_i = all_summaries[i][j]
        drug_names.append(drug_name)
        summary_1d.append(summary_i)

# %%
# -- check for duplicates
duplicate = False
for drug in drug_names:
    if drug_names.count(drug) > 1 :
        print('find duplicate for ' + str(drug))
        duplicate = True
if duplicate:
    print(' !! Found duplicate !!')
    # == TO DO ==
    # Deal with duplicates

# -- Make first basic DataFrame 
df = pd.DataFrame(
    {'drug_name' : drug_names,
     'summary' : summary_1d}
    )

df['uncertainty_atc_match']  = [False]*len(df['drug_name'])
df = df.set_index('drug_name')

# -- Import CBIP data with ATC codes & clean drugs names
cbip_data = pd.read_csv('ATCDPP.csv', sep=';')
cbip_df = copy.deepcopy(cbip_data)
cbip_df['atcnm_e'] = cbip_df['atcnm_e'].replace(', combinaisons', '')
cbip_df['atcnm_e'] = cbip_df['atcnm_e'].replace(' (human)', '')
atc_df = cbip_df[['atc', 'atcnm_e']]

# %%
# -- Find Janus x CBIP matches
atc_codes = []
no_match = []
no_match_idxs = []
atc_match = 0
no_atc = 0

# %%
### Look for Janus x CBIP matching ###
# -- First pass
for idx, drug in enumerate(drug_names):
    array = atc_df[atc_df['atcnm_e'].str.replace(' ','') == drug]['atc'].values  # to do : implement with .loc : ++ optimized
    if len(array) == 0 :
        df.loc[drug,'atc'] = 'no_atc'
        no_match.append(drug)
        no_match_idxs.append(idx)
    else:
        atc = array[0]
        atc_codes.append(atc)
        df.loc[drug,'atc'] = atc
        atc_match += 1 
        # delete rows where matching has occured
        atc_df = atc_df.drop(atc_df[atc_df['atc'] == str(atc)].index)
        
#%%
# -- Prepare for second pass : tokenize CBIP drug names that did not match
stopwords = stopwords.words('english')
dic = {} 
for tidx, name in zip(atc_df.index, atc_df['atcnm_e']):
    tokenized_lst = RegexpTokenizer(r'\w+').tokenize(name)
    for i in range(len(tokenized_lst)):
        if tokenized_lst[i] not in stopwords:
            if tokenized_lst[i] not in dic:
                dic[tokenized_lst[i]] = [tidx]
            dic[tokenized_lst[i]].append(tidx)


# %% 
# -- Sanity check : detect & remove "outliers"
counts = []
outliers = []

for elmnt, nb_occ in dic.items():
    c = len(nb_occ)
    counts.append(c)
    if c > 400 and elmnt not in outliers:
        print(elmnt +  " : counts = " + str(c))
        outliers.append(elmnt)

for outlier in outliers:
    dic.pop(outlier)
    
plt.figure()
plt.hist(np.log10(counts), bins=100)
plt.axvline(np.log10(400), c='r', linestyle='--')
plt.title('Histogram of $log_{10}$ words count from CBIP drugs names column')
plt.show()

    
# %%
cbip_unsorted = list(dic.keys())
sorted_names  = pysort.Sorting().heapSort(cbip_unsorted)


# -- Remove drugs that are known to not be used in Belgium
missing_df = pd.read_csv('./outputs/treated_only_missing_drugs.csv')
drugs_to_remove = list(missing_df['Nom médicament'])

for d in drugs_to_remove:
    if d in sorted_names:
        sorted_names.remove(d)
# %%
# -- Second pass 
missing_drugs = []
uncertain_trgt_drugs = []
nmc = 0   # new match counter
for drug in no_match:
    out = bs.BinarySearch(sorted_names, drug)
    if out == -1:
        no_atc += 1
        missing_drugs.append(drug)
    else:
        sortd_ixd  = out # index
        trgt_drug = sorted_names[sortd_ixd]
        nmc += 1
        arr_tidx = dic[trgt_drug]
        arr_atc = []
        arr_atc = [cbip_df.iloc[idx_i]['atc'] for idx_i in arr_tidx]
        
        # add new matches to the df
        df.loc[trgt_drug,'atc'] = arr_atc[0] 
        
        # check if ATC is consistent
        if not all(atc_i == arr_atc[0] for atc_i in arr_atc):
            uncertain_trgt_drugs.append(trgt_drug)
            df.loc[trgt_drug,'uncertainty_atc_match'] = True

unc_match = len(uncertain_trgt_drugs)

# %%
print('\n\n')
print('====  CBIP x Janus matching performance  ====')
print('1st pass : ' + str(atc_match))
print('2nd pass : ' + str(nmc) +', '+ str(unc_match) + ' of which are uncertain matches')
print('Total matches : ' + str(atc_match+nmc))
print(' -----------------------------------------------')
pc_match = (atc_match+nmc)/janus_len*100
pc_cert_match = (atc_match+nmc-unc_match)/janus_len*100

print('Total matching % : ' + str(round(pc_match,2)))
print('Total certain matching %: ' + str(round(pc_cert_match,2)))

# %%
# -- Add ATC column to basic database
# df['atc'] = atc_codes

# -- Filter out rows with no ATC code
final_db = df[df['atc'] != 'no_atc']
#final_db = final_db[['atc', 'summary', 'uncertainty_atc_match']]

# %%
# -- Export 
final_db.to_csv('./outputs/janus_webscraping.csv', index=True)
pd.DataFrame(
    missing_drugs,
    columns=['missing_drugs']
    ).to_csv(
    './outputs/missing_drugs.csv',
    index=False,
    )

print('"janus_webscraping.csv" & "missing_drugs.csv" written into ./outputs/')
# %%
# clean code
# check missing_drugs.csv