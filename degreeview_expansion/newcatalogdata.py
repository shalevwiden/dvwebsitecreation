import requests
import bs4
from bs4 import BeautifulSoup
import random


import sys
import os
import json

import csv


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

import sqlite3
import importlib.util

from pathlib import Path
# use the parent folder
exceltemplatespath = Path("/Users/shalevwiden/Downloads/Projects/dvwebsitecreation/sourcefiles/pythonfunctions")
sys.path.append(str(exceltemplatespath))

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
print(os.path.dirname(os.path.dirname(__file__)))

from sourcefiles.pythonfunctions.excel_templates import make_checkerboardfile, make_excelfile



# add parent folder to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from websiteprogramming.createuniversity import createUniversity
import importlib


class catalogData(createUniversity):
    def __init__(self, schoolfolder, universityname, cloudbucketpath, websitefolder, schoolabrv):
        super().__init__(schoolfolder, universityname, cloudbucketpath, websitefolder, schoolabrv)
        # child specific methods
        
        self.catalogfile = None
        self.course_list = []
    


def main():
    

    # good to check everythings working with the venv:
    def check():
        if __name__=='__main__':
            print(f'the version of beautiful soup is\n {(bs4.__version__)}')
            print(f'the version of requests is\n {(requests.__version__)}')
            print(f'\nthe python version being used is:{sys.executable}\n')
            catalogobj=catalogData(schoolfolder='utcourses')

    ut_specs=[
                "degreeview_expansion/utcourses",
                "The University of Texas at Austin"
                ,"https://storage.googleapis.com/utcourses",
                "/Users/shalevwiden/Downloads/Projects/testsite/ut",
                "UT"]
    
    catalogobj=catalogData(*ut_specs)
    # catalogobj.create_departmentname_json()
    # catalogobj.get_sorted_departmentlist()
    print(catalogobj.random_dept)
    # catalogobj.makestatsjson()    
    # catalogobj.make_excel_files()
    
    


if __name__=="__main__":
    main()