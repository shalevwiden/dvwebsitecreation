
import requests
import bs4
from bs4 import BeautifulSoup
import sys

import csv


#  good to check everythings working with the venv:
if __name__=='__main__':
    print(f'the version of beautiful soup is\n {(bs4.__version__)}')
    print(f'the version of requests is\n {(requests.__version__)}')
    print(f'\nthe python version being used is:{sys.executable}\n')

link='https://projecteuler.net/archives'

def scrape(link):
    eulerpage=requests.get(link)

    eulersoup=BeautifulSoup(eulerpage.text,'html.parser')

    heading=eulersoup.select_one('h2')
    # print(heading.get_text())

    table=eulersoup.select('table')[0]
    # print(table)

    trs=table.select('tr')

    biglist=[]
    for tr in trs:
        tds=tr.select('td')

        tdlist=[]

        for td in tds:
            tdtext=td.get_text()
            # print(tdtext+'\n')
            tdlist.append(tdtext)
        biglist.append(tdlist)
    return biglist

biglistpageone=scrape(link=link)
# print(f'biglist:{biglist}')


def analyzedata(biglist):
    biglist2=[]
    for group in biglist:
            if group:
                biglist2.append(group)
    sorteddata=sorted(biglist2,key=lambda x:int(x[2]))

    print(sorteddata[0])
# analyzedata(biglist=biglistpageone)

baseurl='https://projecteuler.net/archives;page='

biglist=[]
for i in range(1,20):
    
    currentlink=f'{baseurl}{i}'
    biglist+=scrape(link=currentlink)

analyzedata(biglist=biglist)


def makecsv(biglist):
    # evan making a csv from data you can do very fast fr
    with open('eulerscsv.csv','w') as ecsv:
        writer=csv.writer(ecsv)
        writer.writerow(['Project Eulers CSV','','Sep 20, 2025'])

        for group in biglist:
            if group:
                writer.writerow(group)
makecsv(biglist=biglist)


