'''
This will be the main file that creates and updates all pages on the website.

From "createutcourseswebsite.py" I need to repurpose that class and then call each object when Im updating schools.

Some variables need to be the same across classes like the location of the DegreeView folder.

The data for each object should probably be held in a json file.

Updating the legacy UT part of the site needs to be in this file too.
'''


from pathlib import Path
import os

import sys
if __name__=='__main__':
    print(f'\nthe python version being used is:{sys.executable}\n')


import subprocess
import random

import csv
import time
import json

# use this to render template


# use this to upload stuff to google cloud
from google.cloud import storage


# use this to import stuff from other python files
import importlib.util

from createuniversity import createUniversity

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from degreeview_expansion.newcatalogdata import catalogData

class createPages:
    def __init__(self):
        # havent used this yet
        self.websitepath='/Users/shalevwiden/Downloads/Projects/degreeviewdeployed/utcoursessite/departments'

        self.universityuldatapath=''
    def buildspecs(self,schoolfolder,universityname,cloudbucketpath,websitefolder, schoolabrv):

        
        return {"schoolfolder":schoolfolder,
    "universityname": universityname,
    "cloudbucketpath": cloudbucketpath,
    "websitefolder": websitefolder,
    "schoolabrv":schoolabrv,}
    
    def schoolcontainingfunc(self):
        '''
        This function will call all of the school objects and their methods.
        Itll be a big one.
        Might wanna divide it up later.

        '''
        def texas():
            '''
            This contains all the schools within texas
            '''

            def ut():
                # I need need to standardize the location of all of this stuff
                ut_specs=self.buildspecs(
                    "degreeview_expansion/utcourses",
                    "The University of Texas at Austin"
                    ,"https://storage.googleapis.com/utcourses",
                    "/Users/shalevwiden/Downloads/Projects/testsite/ut",
                    "UT")
            

                def data_methods():
                    utcatalogobj=catalogData(**ut_specs)
                    print(f'Configs folder: {utcatalogobj.configsfolder}')
                    # utcatalogobj.makestatsjson()
                    utcatalogobj.make_excel_files()
                data_methods()


                def web_methods():
                    utobj=createUniversity(**ut_specs)
                    utobj.create_sorteddepartments_page()
                    utobj.create_departmentpagelinks_json()

                # instead of calling all of the functions 

                # utobj.createletterpages()

                # utobj.create_department_pages()

                '''these two functions are actually not called for UT because UT is special
                UT is the original DV'''

                # utobj.createstatspage()
                # utobj.create_uni_homepage()
                # this one is tho I think...

            def rice():
                # update all of this with rice data
                rice_specs=self.buildspecs(
                    "/Users/shalevwiden/Downloads/Coding_Files/Python/BeautifulSoup_Library/degreeview_expansion/rice",
                    "Rice University"
                    ,"https://storage.googleapis.com/ricecourses",

                    # so I can probably make a function to finish this path for whereever I actually host the website
                    "/Users/shalevwiden/Downloads/Projects/testsite/rice",schoolabrv="Rice")
            
                riceobj=createUniversity(**rice_specs)
                # instead of calling all of the functions 

                riceobj.createletterpages()


                riceobj.create_department_pages()
                riceobj.createstatspage()
                riceobj.create_uni_homepage()

            
            # call all the school functions here
            ut()
            # rice()
        texas()

    def createindex(self):
        '''
        Creates the MAIN home page index
        '''
        # the key is what will be dislayed on the index, as in the school name the user will read.
        indextemplate=''
        '''
        Technicalities to be aware of here:
        The box color will actually be set in scss.
        This is because with different colors I'll also have to adjust the TEXT color of the box.
        
        Therefore doing it in scss is the best approach

        '''
        with open(self.universityuldatapath,'r') as universityuldatajson:
            universityuldata=json.load(universityuldatajson)

    def create_main_statspage():
        '''
        Uses the main stats page template to create the HTML file for the main stats 
        of DegreeView (# schools, longest coursename so far, etc)
        '''

def main():
    createpages=createPages()

    createpages.schoolcontainingfunc()

if __name__=="__main__":
    main()