import requests
import bs4
from bs4 import BeautifulSoup

import sys
import os

import csv
import json

# good to check everythings working with the venv:
if __name__=='__main__':
    print(f'the version of beautiful soup is\n {(bs4.__version__)}')
    print(f'the version of requests is\n {(requests.__version__)}')
    print(f'\nthe python version being used is:{sys.executable}\n')

cataloglink='https://catalog.utsa.edu/undergraduate/coursedescriptions/'


def scrapecatalog():
    catalogdict={}

    catalogpage=requests.get(cataloglink)
    catalogsoup=BeautifulSoup(catalogpage.text,'html.parser')

    atozdiv=catalogsoup.find('div',{"id":"atozindex"})

    uls=atozdiv.find_all('ul')

    for ul in uls:
        lis=ul.find_all('li')
        for li in lis:
            atag=li.find('a')

            departmentname=atag.get_text()
            departmentlink=atag['href']

            departmentlink=f'https://catalog.utsa.edu{departmentlink}'
            catalogdict[departmentname]=departmentlink

    return catalogdict

catalogdict=scrapecatalog()
print(catalogdict)

def createjson(catalogdict):
    finaldict=catalogdict


    with open('utsajson.json','w') as utsajson:
        # the dict, the file
        json.dump(finaldict,utsajson,indent=4)

createjson(catalogdict=catalogdict)