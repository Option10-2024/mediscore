# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
from itertools import chain
from sorting_techniques import pysort
import copy

import createListURLs
import drugsURLsGetter
import summaryGetter
import binarysearch as bs

# %%
lst_alpha_urls = createListURLs.CreateListAlphabeticalURLs()
print('-- Got URLs by letter -- \n')
all_drugs_urls = drugsURLsGetter.getAllDrugsUrls(lst_alpha_urls)
print('-- Fetching all the summaries -- \n')
all_summaries = summaryGetter.getSummary(all_drugs_urls)
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
### Look for Janus - CBIP matching ###
# -- First pass
for idx, drug in enumerate(drug_names):
    array = atc_df[atc_df['atcnm_e'].str.replace(' ','') == drug]['atc'].values
    if len(array) == 0 :
        # print('No ATC code for ' + str(drug))
        atc_codes.append('no_atc')
        no_match.append(drug)
        no_match_idxs.append(idx)
        #no_atc += 1
    else:
        atc = array[0]
        atc_codes.append(atc)
        atc_match += 1 
        # delete rows where matching has occured
        atc_df = atc_df.drop(atc_df[atc_df['atc'] == str(atc)].index)

# -- Prepare for second pass : tokenize CBIP drug names 
stopwords = stopwords.words('english')
buffer = [] 
for tidx, name in zip(atc_df.index, atc_df['atcnm_e']):
    tokenized_lst = RegexpTokenizer(r'\w+').tokenize(name)
    for i in range(len(tokenized_lst)):
        if tokenized_lst[i] not in stopwords:
            buffer.append({tokenized_lst[i]:tidx})
flat_lst = list(chain.from_iterable(buffer))

# %% 
# -- Sanity check : detect & remove obvious outliers
counts = []
outliers = []

for elmnt in list(set(flat_lst)):
    c = flat_lst.count(elmnt)
    counts.append(c)
    if c > 400 and elmnt not in outliers:
        print(elmnt +  " : counts = " + str(c))
        outliers.append(elmnt)

plt.figure()
plt.hist(np.log10(counts), bins=100)
plt.axvline(np.log10(400), c='r', linestyle='--')
plt.title('Histogram of log words count from CBIP drugs names column')
plt.show()

flat_lst_clean = [e for e in flat_lst if e not in outliers]

    
# %%
cbip_unsorted = list(set(flat_lst_clean))
sorted_names  = pysort.Sorting().heapSort(cbip_unsorted)

# %%
# -- Second pass 
missing_drugs = []
z=0
for drug in no_match:
    out = bs.BinarySearch(sorted_names, drug)
    if out == -1:
        no_atc += 1
        missing_drugs.append(drug)
    else:
        sort_ixd = out # index
        drug = sorted_names[sort_ixd]
        z += 1
        for dic in buffer:
            atc_occ = 0
            if drug in dic.keys():
                target_idx = list(dic.values())
                # print(target_idx)
                # print(drug)
                print(len(target_idx))
                atc_occ += 1
                if atc_occ > 2:
                    print(drug)

print(z)




#### TO DO ######
# l'output de binary search = index de sorted ou se trouve le médicament en question
# mtn il faut faire le chemin inverse cad trouver l'index dans CBIP qui correspond
# à la ligne ou se trouve le médicament qu'on vient de trouver
#     * pour faire ca idéalement il faudrait stocker les index de CBIP lorsque 
#     traitre les données pour le 2e passage, cad ligne 89



# %%

print("Found " + str(atc_match) + " Janus x CBIP matches")
print("Couldn't find " + str(no_atc) + " ATC codes" )

# %%
# -- Add ATC column to basic database
df['atc'] = atc_codes

# -- Filter out rows with no ATC code
final_db = df[df['atc'] != 'no_atc']
final_db = final_db[['drug_name', 'atc', 'summary']]

# %%
# -- Export 
final_db.to_csv('./outputs/janus_webscraping.csv', index=False)
pd.DataFrame(
    missing_drugs,
    columns=['missing_drugs']
    ).to_csv(
    './outputs/missing_drugs.csv',
    index=False,
    )

print('"janus_webscraping.csv" & "missing_drugs.csv" written into ./outputs/')
# %%
