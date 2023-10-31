# %%
"""
@author: marie
"""

import createListURLs
import drugsURLsGetter
import requests
import time
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

lst_alpha_urls = createListURLs.CreateListAlphabeticalURLs()
all_drugs_urls = drugsURLsGetter.getAllDrugsUrls(lst_alpha_urls)

def getSummary(meds_urls):  
    tik = time.time()    
    all_drugs_summary= []
    for link in meds_urls:
        alph_med_sum = []
        for med_link in link:
            # Scrape summary
            result = requests.get(med_link)
            content = result.text
            soup = BeautifulSoup(content, 'lxml')    
            summary_box = soup.find('div', attrs={'class':'sv-vertical sv-layout sv-skip-spacer sv-decoration-content' })
            if summary_box is None:
                alph_med_sum.append('No recorded data')
            else:
                alph_med_sum.append(summary_box.text)
        all_drugs_summary.append(alph_med_sum)
    tak = time.time()
    tiktak = tak-tik
    print('Got all summaries in ' + str(round(tiktak/60, 2)) + ' minutes')
    return (all_drugs_summary)

# %%
# all_summaries = getSummary(all_drugs_urls)
