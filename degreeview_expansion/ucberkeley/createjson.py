import requests
import bs4
from bs4 import BeautifulSoup
from pathlib import Path


import sys
import os

import csv
import json

# good to check everythings working with the venv:
if __name__=='__main__':
    print(f'the version of beautiful soup is\n {(bs4.__version__)}')
    print(f'the version of requests is\n {(requests.__version__)}')
    print(f'\nthe python version being used is:{sys.executable}\n')

cataloglink='https://undergraduate.catalog.berkeley.edu/departments'


def scrapecatalog():
    catalogdict={}

    catalogpage=requests.get(cataloglink)
    catalogsoup=BeautifulSoup(catalogpage.text,'html.parser')

    atozdiv=catalogsoup.select_one('div#main-content')
    atozdiv = atozdiv.select_one('div.lg\\:w-3\\/4.w-full.mr-4')


    divs=atozdiv.find_all('div',recursive=False)

    for div in divs:
        atags=div.select('ul>li>a')

        for atag in atags:
            if atag:

                departmentname = atag.get_text().strip().strip('\n')
                departmentlink=atag['href'].replace('overview','courses')

                departmentlink=f'https://undergraduate.catalog.berkeley.edu{departmentlink}'
                catalogdict[departmentname]=departmentlink
         
         
    
            
            


    return catalogdict

catalogdict=scrapecatalog()
print(catalogdict)

def createjson(catalogdict):
    

    script_folder = Path(__file__).parent  

    
    json_path = script_folder / 'unijson.json'

    # Write the JSON
    with open(json_path, 'w') as unijson:
        # the dict, the file
        json.dump(catalogdict,unijson,indent=4)

createjson(catalogdict=catalogdict)