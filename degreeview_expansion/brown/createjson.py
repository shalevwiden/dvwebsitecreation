import requests
import bs4
from bs4 import BeautifulSoup

import sys
import os

import csv
import json
from pathlib import Path


# good to check everythings working with the venv:
if __name__=='__main__':
    print(f'the version of beautiful soup is\n {(bs4.__version__)}')
    print(f'the version of requests is\n {(requests.__version__)}')
    print(f'\nthe python version being used is:{sys.executable}\n')

cataloglink='https://bulletin.brown.edu/departments-centers-programs-institutes/'


def scrapecatalog():
    catalogdict={}

    catalogpage=requests.get(cataloglink)

    catalogsoup=BeautifulSoup(catalogpage.text,'html.parser')

    atozdiv=catalogsoup.select_one('div#textcontainer')
    print(atozdiv)

    uls=atozdiv.select('ul')
    for ul in uls:
        lis=ul.select('li')
        for li in lis:
            atag=li.select_one('a')

            if atag:

                departmentname=atag.get_text()
                departmentlink=atag['href']

                departmentlink=f'https://bulletin.brown.edu{departmentlink}#courseinventory'
                catalogdict[departmentname]=departmentlink


    return catalogdict



catalogdict=scrapecatalog()


def createjson(catalogdict):
    script_folder = Path(__file__).parent  

    
    json_path = script_folder / 'unijson.json'

    # Write the JSON
    with open(json_path, 'w') as unijson:
        # the dict, the file
        json.dump(catalogdict,unijson,indent=4)

createjson(catalogdict=catalogdict)