#%% 
from string import ascii_uppercase  

def CreateListAlphabeticalURLs():
    lst_urls = []
    base_url_str = 'https://janusinfo.se/beslutsstod/lakemedelochmiljo/pharmaceuticalsandenvironment/#letter/{}'
    for letter in ascii_uppercase:
        lst_urls.append(base_url_str.format(letter))
    return lst_urls

urls = CreateListAlphabeticalURLs()

#%%

import requests
from bs4 import BeautifulSoup
from scrapy import Selector
from selenium import webdriver

driver = webdriver.Chrome()  # You can choose another browser if preferred

link = 'https://janusinfo.se/beslutsstod/lakemedelochmiljo/pharmaceuticalsandenvironment/#letter/A'
driver.get(link)

# Allow some time for the page to load (you may need to adjust this)
driver.implicitly_wait(30)

# Get the page source after it has loaded
page_source = driver.page_source

# Close the WebDriver
driver.quit()

# Now you can use BeautifulSoup to parse the page source
soup = BeautifulSoup(page_source, 'html.parser')
box = soup.find('div', attrs={'class': 'marker_4ba952c316aa46e49e75c8a2'})

# Check if the box is found
if box:
    links = [a['href'] for a in box.find_all('a', href=True)]
    print(links)
else:
    print("Box not found. Make sure the webpage structure hasn't changed.")

# %%
