from string import ascii_uppercase  

def CreateListAlphabeticalURLs():
    lst_urls = []
    base_url_str = 'https://janusinfo.se/beslutsstod/lakemedelochmiljo/pharmaceuticalsandenvironment.4.7b57ecc216251fae47487d9a.html?letter=A#letter/{}'
    for letter in ascii_uppercase:
        lst_urls.append(base_url_str.format(letter))
    return lst_urls

if __name__ == "__main__":
    # only write txt file if executed as a main file
    urls = CreateListAlphabeticalURLs()
    with open('list_alpha_urls.txt','w') as file:
        for url_i in urls: 
            file.write(url_i)
            file.write('\n')

    print('All URLs correctly written!')
