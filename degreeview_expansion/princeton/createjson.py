import requests
import bs4
from bs4 import BeautifulSoup
import certifi


import sys
import os

import csv
import json
from pathlib import Path
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
os.environ["SSL_CERT_FILE"] = certifi.where()

# good to check everythings working with the venv:
if __name__=='__main__':
    print(f'the version of beautiful soup is\n {(bs4.__version__)}')
    print(f'the version of requests is\n {(requests.__version__)}')
    print(f'\nthe python version being used is:{sys.executable}\n')

cataloglink='https://www.princeton.edu/academics/areas-of-study'


def scrapecatalog():
    catalogdict={}

    # catalogpage = requests.get(cataloglink, verify=certifi.where())

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
    }

    catalogpage = requests.get(
        "https://www.princeton.edu/academics/areas-of-study",
        headers=headers,
        verify=False
    )

    print(catalogpage.status_code)
    catalogsoup=BeautifulSoup(catalogpage.text,'html.parser')

    atozdiv=catalogsoup.select_one('div.item-list > ul.area-accordion')
    # print(f'atozdiv:\n {atozdiv}')

    lis=atozdiv.select('li')
    for li in lis:
        h2=li.select_one('h2')
        if h2:
            h2=h2.get_text()

        atag=li.select_one('div.accordion-content.row.small-12 > div > a.button')

        if atag:

            departmentname=h2
            departmentlink=atag['href']

            departmentlink=f'https://www.princeton.edu{departmentlink}'
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