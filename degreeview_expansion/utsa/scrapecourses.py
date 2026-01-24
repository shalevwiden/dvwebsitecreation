import requests
import bs4
from bs4 import BeautifulSoup

import sys
import os
import json

import csv

import openpyxl




from openpyxl import load_workbook
from openpyxl import Workbook
# use this to define the function define_start_column
from openpyxl.utils import column_index_from_string

# this assigns cells colors
from openpyxl.styles import PatternFill

import time
import os

from openpyxl.styles import Font
from openpyxl.styles import Border, Side, Alignment



# good to check everythings working with the venv:
if __name__=='__main__':
    print(f'the version of beautiful soup is\n {(bs4.__version__)}')
    print(f'the version of requests is\n {(requests.__version__)}')
    print(f'\nthe python version being used is:{sys.executable}\n')

csurl='https://catalog.utsa.edu/undergraduate/sciences/computerscience/#courseinventory'

mecheurl='https://catalog.utsa.edu/undergraduate/coursedescriptions/me/'

def scrape_utsa_courses(url):

    coursespage=requests.get(url)
    coursessoup=BeautifulSoup(coursespage.text,'html.parser')

    # find, find_all
    coursesdiv=coursessoup.find('div',attrs={"class":"courses"})

    def get_department_name(coursesdiv):
        departmentelement=coursesdiv.find('h3',{"class":"keepwithnext"})

        departmentclass=departmentelement.get("class", [])

        departmentname=departmentelement.get_text()

        departmentname=departmentname.split(')')[0]+')'
        departmentname2=departmentelement.text


        print(f'Department name class:\n{departmentclass[0]}\n')
        print(f'print statement:\nDepartment name: {departmentname}\n')
        return departmentname
    





    departmentname=get_department_name(coursesdiv=coursesdiv)
    print(f'Department name = {departmentname}')

    def get_courses_dict(coursediv):

        departmentdict={}
        courseblocks=coursediv.find_all('div',{"class":"courseblock"})

        for courseblock in courseblocks:
            courseline=courseblock.find('p',{"class":"courseblocktitle"}).find("strong").get_text()
            
            # print(courseline)
            
            # coursename2=courseblock.find('p')[0].get_text()
            courselinelist=courseline.split('. ')

            if len(courselinelist)>3:
                coursecode=courselinelist[0]

                coursename=' '.join(courselinelist[1:-2])

                # logic to get hours
                if "hours" not in courselinelist[-1].lower():
                    coursehours=courselinelist[-2]
                else:
                    coursehours=courselinelist[-1]


            else:
                coursecode,coursename,coursehours,empty=courseline.split('.')
            

            coursename=coursename.strip()
            coursecode=coursecode.replace('\xa0',' ')

            # clean course hours
            coursehours=coursehours.lower().replace(' ','').split(')')[-1].split('credit')[0].strip()
            coursehours=int(coursehours)



            print(coursecode,coursename,coursehours)

            upperlowerstatus=''

            firstnum=coursecode.split( )[-1][0]
            firstnum=int(firstnum)
            if firstnum>2:
                upperlowerstatus="Upper Division"
            else:
                upperlowerstatus="Lower Division"

            departmentdict[coursename]=[coursecode,coursehours,upperlowerstatus]


        return departmentdict

            
    departmentdict=get_courses_dict(coursediv=coursesdiv)
    
    # main return 
    return departmentdict


def analyze_departmentdict(departmentdict):

        totalhours=0
        namelengthlist=[]
        for key in departmentdict:

            coursecode,coursehours,category=departmentdict[key]
            totalhours+=coursehours
            coursename=key
            print(coursename)
            namelengthlist.append([coursename,len(coursename)])


        namelengthlist=sorted(namelengthlist, key=lambda x:x[1],reverse=True)
        print(namelengthlist)
    






csdict=scrape_utsa_courses(url=csurl)
# print(f'CS dict:\n{csdict}\n')

mechedict=scrape_utsa_courses(url=mecheurl)

# print(mechedict)

