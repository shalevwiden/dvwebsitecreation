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

accountingurl='https://catalog.utdallas.edu/2025/undergraduate/courses/acct'
biourl='https://catalog.utdallas.edu/2025/undergraduate/courses/biol'

def scrapeutdcourses(departmenturl):
    departmentdict={}

    coursepage=requests.get(departmenturl)
    coursesoup=BeautifulSoup(coursepage.text,'html.parser')

    courselines=coursesoup.select('div#bukku-page p')


    for line in courselines:
        coursecode=line.select('span.course_address')[0].get_text()
        coursename=line.select('span.course_title')[0].get_text()
        coursehours=line.select('span.course_hours')[0].get_text()

        # formatting


        coursename=coursename.strip()
        coursecode=coursecode.replace('\xa0',' ')

        if 'individual' not in coursehours.lower():
            coursehours=coursehours.replace('(','').split(' ')[0]
        else:
            coursehours=coursehours
        



        cleanedcoursecode=coursecode
        
        print(f'Cleancoursecode={cleanedcoursecode}')
        coursenumber=cleanedcoursecode.split(' ')[-1]
        print(f'coursenumber: {coursenumber}')

        

        identifynumber=coursenumber[0]
        identifynumber=int(identifynumber)

        print(f'identifynumber: {identifynumber}')




        status=''
        
        if identifynumber>=5:
            status="Graduate"
        
        elif identifynumber>=3:
            status="Upper Division"
        else:
            status="Lower Division"






        departmentdict[coursename]=[coursecode,coursehours,status]

    return departmentdict

def analyze_departmentdict(departmentdict):
    

        totalhours=0
        namelengthlist=[]
        for key in departmentdict:

            coursecode,coursehours,category=departmentdict[key]

            
            coursename=key
            namelengthlist.append([coursename,len(coursename)])


        namelengthlist=sorted(namelengthlist, key=lambda x:x[1],reverse=True)
        print(namelengthlist)
        print(f'\nLongest name {namelengthlist[0]}\n')
        print(f'Shortest name {namelengthlist[-1]}')
# acctdict=scrapeutdcourses(departmenturl=accountingurl)

# well this fukin works lol

# analyze_departmentdict(departmentdict=acctdict)

if __name__=='__main__':
        
    departmentdict=scrapeutdcourses(departmenturl=biourl)
    print(departmentdict)

