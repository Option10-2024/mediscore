# %%
import requests
import time
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

import createListURLs
import drugsURLsGetter
import summaryGetter

lst_alpha_urls = createListURLs.CreateListAlphabeticalURLs()
print('-- Got URLs by letter -- ')
all_drugs_urls = drugsURLsGetter.getAllDrugsUrls(lst_alpha_urls)
all_summaries = summaryGetter.getSummary(all_drugs_urls)

# %%
# Create the database 
# -- Flatten 2D lists into 1D lists
drug_names = []
summary_1d = []

for i in range(len(all_drugs_urls)):
    for j in range(len(all_drugs_urls[i])):
        drug_name = all_drugs_urls[i][j].split('/')[-1].split('.')[0]
        summary_i = all_summaries[i][j]
        drug_names.append(drug_name)
        summary_1d.append(summary_i)

# -- Make first basic DataFrame 
df = pd.DataFrame(
    {'drug_name' : drug_names,
     'summary' : summary_1d}
    )
# %%