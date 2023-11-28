# %%
def dateGetter():
    from bs4 import BeautifulSoup
    import requests
    url = 'https://janusinfo.se/beslutsstod/lakemedelochmiljo/pharmaceuticalsandenvironment/environment/lastupdated.5.7b57ecc216251fae47488396.html'

    result = requests.get(url)
    content = result.text
    goodsoup = BeautifulSoup(content, 'lxml')
    box = goodsoup.find('div', attrs={'id':'svid12_7b57ecc216251fae4748839d'})
    text = box.text
    date = text.split('New')[0][4:]

    with open('./outputs/database_date.txt', 'w') as f:
        f.write(date)
    return date
# %%
