import requests
import bs4
from bs4 import BeautifulSoup

import sys
import os
import json

import csv

# good to check everythings working with the venv:
if __name__=='__main__':
    print(f'the version of beautiful soup is\n {(bs4.__version__)}')
    print(f'the version of requests is\n {(requests.__version__)}')
    print(f'\nthe python version being used is: {sys.executable}\n')

accurl='https://ga.rice.edu/programs-study/courses/econ/'

with open('/Users/shalevwiden/Downloads/Projects/dvwebsitecreation/sourcefiles/avoidwords/avoidwords.json','r') as avoidfile:
    avoidwords=json.load(avoidfile)


print(f'Avoidwords:\n {avoidwords}\n')
def scrapericecourses(departmenturl):
    departmentdata={}

    coursepage=requests.get(departmenturl)
    coursesoup=BeautifulSoup(coursepage.text,'html.parser')

    courseblocks=coursesoup.select('div#textcontainer div.courseblock')

    for block in courseblocks:
        coursetitle=block.select('p.courseblocktitle')[0].get_text()

        coursecode=coursetitle.split('-')[0].strip()

        # this checks if a word is all I or not
        def is_all_i(word: str) -> bool:
            return all(ch.lower() == "i" for ch in word) and word != ""

        def makecapitalized(coursetitle):
            coursetitle=coursetitle.split('-')[1:]
            coursetitle='-'.join(coursetitle).strip()
            
            coursename=[]
            coursetitle=coursetitle.split(' ')
            for coursepart in coursetitle:
                if is_all_i(coursepart):
                    coursename.append(coursepart.upper())

                elif coursepart.lower() not in avoidwords:
                    coursename.append(coursepart.capitalize())
                
                else:
                    coursename.append(coursepart.lower())
            coursename=' '.join(coursename)
            return coursename
        
        coursename=makecapitalized(coursetitle=coursetitle)
        



        courseblockextras=block.select('p.courseblockextra')
        for courseblockextra in courseblockextras:
            if courseblockextra.select('span'):
                spantext=courseblockextra.select('span.credits')[0].get_text()
                coursehours=spantext.split(':')[-1].strip()
            else:
                if "course level" in courseblockextra.get_text().lower():
                    classification=courseblockextra.get_text()
                    classification=classification.split(':')[-1].strip()

            
            



        # plans for up to THREE repeated coursenames bro
        if coursename not in departmentdata:

            departmentdata[coursename]=[coursecode,coursehours,classification]
        elif coursename in departmentdata:
            coursename+="SECOND"
            departmentdata[coursename]=[coursecode,coursehours,classification]
        elif f"{coursename}SECOND" in departmentdata:
            coursename += "THIRD"
            departmentdata[coursename] = [coursecode, coursehours, classification]




    return departmentdata

def analyze_departmentdata(departmentdata):
    

        totalhours=0
        namelengthlist=[]
        for key in departmentdata:

            coursecode,coursehours,category=departmentdata[key]

            
            coursename=key
            namelengthlist.append([coursename,len(coursename)])


        namelengthlist=sorted(namelengthlist, key=lambda x:x[1],reverse=True)
        print(namelengthlist)
        print(f'\nLongest name {namelengthlist[0]}\n')
        print(f'Shortest name {namelengthlist[-1]}')

if __name__=='__main__':
        
    departmentdata=scrapericecourses(departmenturl=accurl)
    print(departmentdata)

