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

from scrapecoursedata import scrapeutdcourses

class catalogData:
    def __init__(self):
        self.jsondatapath='/Users/shalevwiden/Downloads/Coding_Files/Python/BeautifulSoup_Library/degreeview_expansion/utd_courses/utdjson.json'
        self.utdcoursesfolder='/Users/shalevwiden/Downloads/Projects/otherdvschools/texas/UTD_courses'

        with open(self.jsondatapath,'r') as utsajson:

            self.jsondata=json.load(utsajson)


    def createdatabase(self):
        pass
    
    def createcsvs(self):

        for departmentname in self.jsondata:
            departmentlink=self.jsondata[departmentname]
            print(f'Starting process for {departmentname}')


            departmentnamecleaned=departmentname.replace(' ','').lower()
            departmentnamecleaned=departmentnamecleaned.replace('/','-')

            departmentname=departmentnamecleaned
            departmentfolder=departmentname
            departmentfolderpath=os.path.join(self.utdcoursesfolder,departmentfolder)

            if not os.path.exists(departmentfolderpath):
                os.mkdir(departmentfolderpath)

            
            

            departmentcourses_csv=os.path.join(departmentfolderpath,f'{departmentname}courses-csv.csv')

            with open(departmentcourses_csv,'w') as departmentcourses_csv:

                departmentdict=scrapeutdcourses(departmenturl=departmentlink)

                # expirementing with quoting cause why not
                writer=csv.writer(departmentcourses_csv,quotechar='"', delimiter=',')
                headings=['Coursename','Coursecode','Hours', 'Classification']
                writer.writerow(headings)

                writelist=[]
                totalhours=0
                for coursename in departmentdict:
                    coursecode,coursehours,status=departmentdict[coursename]
                    values=[coursename,coursecode,coursehours,status]  
                    writelist.append(values)
                    try:
                        if '-' in coursehours:
                            coursehourcount = 3
                            totalhours+=int(coursehourcount)
                            print('adding\n\n')

                        else:
                            coursehourcount = coursehours.strip()[-1]
                            totalhours+=int(coursehourcount)

                    except Exception as e:
                        print(f"Faulty coursehours: {coursehours}, Error: {e}")
                    
                
                writer.writerows(writelist)
                writer.writerow(['','',f'Total Hours: {totalhours}'])
                writer.writerow(['DegreeView'])







    def analyzedata(self):
        pass


def runcatalogDataclass():
    catalogobj=catalogData()

    catalogobj.createcsvs()

runcatalogDataclass()
