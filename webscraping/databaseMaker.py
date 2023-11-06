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
cbip_df = pd.read_csv('ATCDPP.csv', sep=';')
cbip_df['atcnm_e'] = cbip_df['atcnm_e'].replace(', combinaisons', '')
cbip_df['atcnm_e'] = cbip_df['atcnm_e'].replace(' (human)', '')
act_df = cbip_df[['atc', 'atcnm_e', 'atcnm_f']]

# %%
# -- Find Janus x CBIP matches
atc_codes = []
missing_drugs = []
atc_match = 0
no_atc = 0

# -- Create ATC column 
for drug in drug_names:
    array = act_df[(act_df['atcnm_e'].str.replace(' ','') == drug)
                 | (act_df['atcnm_f'].str.replace(' ','') == drug)]['atc'].values
    if len(array) == 0 :
        # print('No ATC code for ' + str(drug))
        atc_codes.append('no_atc')
        missing_drugs.append(drug)
        no_atc += 1
    else:
        atc = array[0]
        atc_codes.append(atc)
        atc_match += 1

print("Found " + str(atc_match) + " Janus x CBIP matches")
print("Couldn't find " + str(no_atc) + " ATC codes" )

# -- Add ATC column to basic database
df['atc'] = atc_codes

# -- Filter rows with no ATC code
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
