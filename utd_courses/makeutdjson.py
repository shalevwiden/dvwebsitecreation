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

cataloglink='https://catalog.utdallas.edu/2025/undergraduate/courses'

# do both graduate and undergraduate

''


def scrapecatalog():
    catalogdict={}

    catalogpage=requests.get(cataloglink)
    catalogsoup=BeautifulSoup(catalogpage.text,'html.parser')

    trs=catalogsoup.select('table#courses > tbody tr')
    for tr in trs:
        tds=tr.select('td')
        codetd=tds[0]
        codetext=codetd.get_text()
        atag=codetd.find('a')

        departmentname=tds[1].get_text()

        fulldepartmentname=f'{codetext} - {departmentname}'
        if atag:

            departmentlink=atag['href']

            departmentlink=f'https://catalog.utdallas.edu{departmentlink}'
            catalogdict[fulldepartmentname]=departmentlink
            


    return catalogdict

catalogdict=scrapecatalog()
print(catalogdict)

def createjson(catalogdict):
    finaldict=catalogdict


    with open('utdjson.json','w') as utjson:
        # the dict, the file
        json.dump(finaldict,utjson,indent=4)

createjson(catalogdict=catalogdict)