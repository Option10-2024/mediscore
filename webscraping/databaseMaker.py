# %%
import pandas as pd

import createListURLs
import drugsURLsGetter
import summaryGetter

lst_alpha_urls = createListURLs.CreateListAlphabeticalURLs()
print('-- Got URLs by letter -- \n')
all_drugs_urls = drugsURLsGetter.getAllDrugsUrls(lst_alpha_urls)
print('-- Fetching all the summaries -- \n')
all_summaries = summaryGetter.getSummary(all_drugs_urls)

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
# %%
# -- Import ATC database from CBIP
cbip_df = pd.read_csv('ATCDPP.csv', sep=';')
act_df = cbip_df[['atc', 'atcnm_e']]

atc_codes = []
no_act = 0

# -- Create ATC column 
for drug in drug_names:
    array = act_df[act_df['atcnm_e'] == drug]['atc'].values
    if len(array) == 0 :
        # print('No ATC code for ' + str(drug))
        atc_codes.append('no_atc')
        no_act += 1
    else:
        atc = array[0]
        atc_codes.append(atc)
print("Couldn't find " + str(no_act) + " ATC codes" )

# -- Add ATC column to basic database
df['atc'] = atc_codes

# -- Filter rows with no ATC code
final_db = df[df['atc'] != 'no_atc']
final_db = final_db[['drug_name', 'atc', 'summary']]

# %%
# -- Export 
final_db.to_csv('./outputs/janus_webscraping.csv', index=False)
print('janus_webscraping.csv written into ./outputs/')