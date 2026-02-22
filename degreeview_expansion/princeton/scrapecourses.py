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

    coursepage=requests.get(departmenturl, verify=False)
    coursesoup=BeautifulSoup(coursepage.text,'html.parser')

    courseblocks=coursesoup.select('div.bordered.area-of-study > div.row.views-row > div.columns.small-12.medium-6.start')
    # print(courseblocks)

    

    for block in courseblocks:
        title=block.select_one('h2')
        print(title)

        # description=block.select_one('p.courseblockdesc')
       

        coursecode =block.select_one('div.course_id').get_text(strip=True).replace('\xa0', ' ').split('.')[0]
        print(coursecode)

        coursename = title.get_text(strip=True).replace('\xa0', ' ')
        
        # Determine course level from the number
        
        def get_coursehours():
            hours=block.select_one('span.credits')
            if hours:
                coursehours=int(hours.get_text().strip()[0])

            coursehours=''
            return coursehours


        def get_status(coursecode):
            '''
            source: https://registrar.brown.edu/students/course-enrollment/courses
            '''
            identifynumber=coursecode.split(' ')[-1][0]
            try:
                if identifynumber:
                    identifynumber=int(identifynumber)

                    if identifynumber >= 5:
                        status = 'Graduate'
                    elif identifynumber >= 3:
                        status = "Upper Division"
                    else:
                        # 1 and 2
                        status = "Lower Division"
                        
                    # override here
                    
                    return status
            except Exception as e:
                print(f"Error {e}: Identity Number conversion failed: {identifynumber}\nCoursecode: {coursecode}")
                return f"Couldnt get status: {identifynumber}"


            
        
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
    testurl = 'https://www.princeton.edu/academics/area-of-study/linguistics'
    departmentdata = scrapecourses(departmenturl=testurl)
    if departmentdata:
        print(departmentdata)

