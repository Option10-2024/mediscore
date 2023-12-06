#%%
import requests
from bs4 import BeautifulSoup
import dirmaker

# import python scripts
import createListURLs

def getAllDrugsUrls(alpha_lst_URLs):
    '''
    * alpha_lst_URLs is an alphabetical-ordered list of URLs of the webpages 
        containing all the URLs starting with the lettre $i*. 
    
        alpha_lst_URLs is the output of the createListURLs function
    
    * returns a 2D list with all the URLs to all the drugs in the janusinfo
        database
    '''
    # Define the domain name
    root = 'https://janusinfo.se/'
    all_drugs_urls = []
    
    for drugs_letter_i in alpha_lst_URLs:
        # print letter being processed
        current_letter = drugs_letter_i.split('=')[1][0]
        print("Letter " + str(current_letter) + " is being processed...")
        
        # Begin URL extraction
        urls_letter_i = []
        result  = requests.get(drugs_letter_i)
        content = result.text
        soup = BeautifulSoup(content, 'lxml')
        alpha_table = soup.find('ol', class_='sv-abc-result sv-defaultlist-noleft')
        
        # Make sure the find() does not return None
        if alpha_table:
            # Extract all the URLs from the given webpage
            for href in alpha_table.find_all('a', href=True):
                link = href['href']
                full_valid_link = f"{root}{link}"
                #print(full_valid_link)
                urls_letter_i.append(full_valid_link)
                
            # Add all the links for a given letter to the main list
            all_drugs_urls.append(urls_letter_i)
            
        elif alpha_table==None :
            print("    No 'ol' element with the specified class found!")
            # Check if there is a drug starting with letter *i*
            print("    Checking if list of drugs is empty")
            warning_div = soup.find('div', class_="marker_4ba952c316aa46e49e75c8a2")
            warning_msg = warning_div.text.strip()
            print("    " + warning_msg)
            
        else:
            print("No 'ol' element with the specified class found!")
        
    return all_drugs_urls
    
# %%
if __name__ == "__main__":
    dirmaker.makeOutputDir()
    # Create a list containing all the URL of the webpages 
    # with all the links for drug starting with letter *i*
    lst_alpha_urls = createListURLs.CreateListAlphabeticalURLs()
    all_drugs_urls = getAllDrugsUrls(lst_alpha_urls)
    
    # Write the output as a txt file
    with open('./outputs/list_drugs_urls.txt','w') as file:
        for drugs_letter_i in all_drugs_urls:
            for url_drug_i in drugs_letter_i:
                file.write(url_drug_i)
                file.write('\n')

    print('URLs of all drugs correctly written!')
    
    