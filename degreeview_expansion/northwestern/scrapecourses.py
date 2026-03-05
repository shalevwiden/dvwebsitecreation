import requests
import bs4
from bs4 import BeautifulSoup

import sys
import os
import json

import csv
from pathlib import Path
import re


# good to check everythings working with the venv:
if __name__=='__main__':
    print(f'the version of beautiful soup is\n {(bs4.__version__)}')
    print(f'the version of requests is\n {(requests.__version__)}')
    print(f'\nthe python version being used is: {sys.executable}\n')



def scrapecourses(departmenturl):
    departmentdata={}

    coursepage=requests.get(departmenturl)
    coursesoup=BeautifulSoup(coursepage.text,'html.parser')

    courseblocks=coursesoup.select('div#textcontainer div.courseblock')

    coursescontainer = coursesoup.select_one('div.sc_sccoursedescs')
    if not coursescontainer:
        print(f"No container found for {departmenturl}")
        return None
    

    courseblocks = coursescontainer.select('div.courseblock')

    for block in courseblocks:
        title=block.select_one('span.courseblocktitle')

        if not title:
            title=block.select_one('span.couresblocktitle')
        if not title:
            title=block.select_one('p.couresblocktitle')
        

            
       

        coursecode = title.get_text(strip=True).replace('\xa0', ' ').split(' ',2)[:2]
        coursecode=" ".join(coursecode).strip()


        print(f'Coursecode \n{coursecode}\n')

        coursenameparts = title.get_text(strip=True).replace('\xa0', ' ').split(' ',2)[2:]
        coursename = ' '.join(coursenameparts).strip().split('(')[0].strip()

        print(f'Coursename \n{coursename}\n')
        # Determine course level from the number
        
        def get_coursehours():
            # hours=block.select_one('span.credits').get_text().strip()
            units = (
                title.get_text().lower()
                .split('(')[-1]
                .replace('\xa0', ' ')
                .replace('\n', '')
                .replace(')', '').replace(' ', '')
                .strip().replace('unit','')
            )
            # dont return it as an int
            
            return units


        def get_status(coursecode):
            '''
            source:

            https://catalogs.northwestern.edu/undergraduate/requirements-policies/courses-credit/
            '''
            identifynumber=coursecode.split(' ')[-1][0]
            print(f'Identity number \n{identifynumber}\n')
            if identifynumber:
                identifynumber=int(identifynumber)

            if identifynumber >= 5:
                status = 'Graduate'
            elif identifynumber >= 3:
                status = "Upper Division"
            else:
                # 1 and 2 can all be lower
                status = "Lower Division"
                
            # override here
            return status
        
        coursehours=get_coursehours()
        status=get_status(coursecode=coursecode)

        # Handle repeated course names
        if coursename not in departmentdata:
            departmentdata[coursename] = [coursecode, coursehours, status]
        elif f"{coursename}SECOND" not in departmentdata:
            coursename += "SECOND"
            departmentdata[coursename] = [coursecode, coursehours, status]
        else:
            coursename += "THIRD"
            departmentdata[coursename] = [coursecode, coursehours, status]

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



if __name__ == '__main__':
    testurl = 'https://catalogs.northwestern.edu/undergraduate/courses-az/econ/'
    departmentdata = scrapecourses(departmenturl=testurl)
    if departmentdata:
        print(departmentdata)

