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
    print(f'\nthe python version being used is:{sys.executable}\n')

englishurl='https://catalog.utexas.edu/general-information/coursesatoz/e/'

# ut courses
# but function name is the same
def scrapecourses(departmenturl):
    departmentdata={}

    coursepage=requests.get(departmenturl)
    coursesoup=BeautifulSoup(coursepage.text,'html.parser')

    courselines=coursesoup.select('div#textcontainer > h5')

    for line in courselines:
        linetext=line.get_text()
        print(linetext)

            
        coursecode=linetext.split('.')[0]
        coursename=linetext.split('.')[1:]
        # remove empty strings
        coursename=[part for part in coursename if part]
        coursename='.'.join(coursename)


        coursename=coursename.strip()
        coursecode=coursecode.replace('\xa0',' ')
        
        if '(' in coursecode:
            cleanedcoursecode=coursecode.split('(')[0].strip()
        else:
            cleanedcoursecode=coursecode
        
        print(f'Cleancoursecode={cleanedcoursecode}')
        coursenumber=cleanedcoursecode.split(' ')[-1]
        print(f'coursenumber: {coursenumber}')

        coursehours=coursenumber[0]

        identifynumber=coursenumber
        print(f'identifynumber: {identifynumber}')
        identifynumber = "".join(ch for ch in identifynumber if ch.isdigit())
        identifynumber=identifynumber[1:]

        identifynumber=int(identifynumber)



        status=''
        if identifynumber>=80:
            status='Graduate'
        elif identifynumber>=20:
            status="Upper Division"
        else:
            status="Lower Division"


        # for them coursenames with crazy hours
        if len(cleanedcoursecode.split(' ')[1:])>1:
            removeletters=''
            for i in cleanedcoursecode:
                if not i.isalpha():
                    removeletters+=i
            cleanedcoursecode=removeletters
            print(f'new: {cleanedcoursecode}')
            coursenumbers=cleanedcoursecode.split(',')
            print(coursenumbers)
            coursehourslist=[]

            for coursenumber in coursenumbers:
                coursehours=coursenumber.strip()[0]
                coursehourslist.append(coursehours)
            
            coursehours=', '.join(coursehourslist)
            

            



        # plans for up to THREE repeated coursenames bro
        if coursename not in departmentdata:

            departmentdata[coursename]=[coursecode,coursehours,status]
        elif coursename in departmentdata:
            coursename+="SECOND"
            departmentdata[coursename]=[coursecode,coursehours,status]
        elif f"{coursename}SECOND" in departmentdata:
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

if __name__=='__main__':
        
    departmentdata=scrapecourses(departmenturl=englishurl)
    print(departmentdata)

