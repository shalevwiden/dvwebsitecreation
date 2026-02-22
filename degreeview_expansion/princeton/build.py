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
from jinja2 import Environment, FileSystemLoader


# use this to render template


# use this to upload stuff to google cloud
from google.cloud import storage


# use this to import stuff from other python files


import sys
from pathlib import Path

# 1️⃣ Get the project root
project_root = Path(__file__).resolve().parents[2]  # DV website creation

# 2️⃣ Add the "websiteprogramming" folder to sys.path once
website_programming = project_root / "websiteprogramming"
sys.path.append(str(website_programming))

# 3️⃣ Now you can import everything from that folder naturally
from createuniversity import createUniversity
# cobj=createUniversity()
# print(cobj.env)
from createpages import createPages
from utdegreeplans import createWebsite
PROJECT_ROOT = Path(__file__).resolve().parents[1]  # parents[1] = degreeview_expansion
sys.path.append(str(PROJECT_ROOT))
from degreeview_expansion.newcatalogdata import catalogData



pagesobj=createPages()
print(pagesobj.websitepath)

class singleUni():
    def __init__(self):

        self.websitepath='/Users/shalevwiden/Downloads/Projects/degreeviewwebsite'
        self.specs=pagesobj.buildspecs(
            "degreeview_expansion/princeton",
                "princeton University",
            os.path.join(self.websitepath,'princeton'),
            "princeton")
    def unidata(self):
                
            #  we'll do bucket stuff later

        
        
        
        princetoncatalogobj=catalogData(**self.specs)
        print(f'Configs folder: {princetoncatalogobj.configsfolder}')
        
        # princetoncatalogobj.upload_to_database()
        # princetoncatalogobj.upload_stragglers_todb()
        
        princetoncatalogobj.makestatsjson()
        # princetoncatalogobj.make_excel_files()
        princetoncatalogobj.create_univeristy_files()
        princetoncatalogobj.make_sorteddepartment_json()
        princetoncatalogobj.make_university_statsjson()

    
    def uniweb():
        princetonobj=createUniversity(**self.specs)

        # princetonobj.createletterpages()

        # princetonobj.upload_department_files()
        princetonobj.create_department_pages()
        princetonobj.create_departmentpagelinks_json()

        princetonobj.createstatspage()
        princetonobj.create_sorteddepartments_page()
        princetonobj.create_uni_homepage()
        
    

def main():
    # print(os.getcwd())

    princetonobj=singleUni()
    print(princetonobj.specs)
    princetonobj.unidata()
  

if __name__=="__main__":
    main()