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
# exceltemplatespath = Path("/Users/shalevwiden/Downloads/Projects/dvwebsitecreation/sourcefiles/pythonfunctions")
# sys.path.append(str(exceltemplatespath))

from pathlib import Path
import sys

project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

from degreeview_expansion.excel.functions.make_excelfile import make_excelfile




class exceltesting():
    def __init__(self,universityname,configpath):
        self.make_excelfile=make_excelfile
        self.universityname=universityname
        self.configpath=configpath

        

        self.sampledepartmentname='Economics'
        
        self.samplerows=[[i for i in range(4)] for i in range(10)]
        print(f'Self.samplerows: \n {self.samplerows}')

        # self.savepath=os.path.join('testing',self.universityname)
       
        

        base_dir = Path(__file__).resolve().parent  # folder of the script
        self.savepath = base_dir / 'testing' / self.universityname
        self.savepath.mkdir(parents=True, exist_ok=True)  # pathlib version




        

    def make_themed_file(self):
        '''
        This is a modular way to make excel files.
        '''
        filename=f'{self.sampledepartmentname}-{self.universityname}.xlsx'
        # change this line to change the save path
        # kinda
        savepath=os.path.join(str(self.savepath),filename)
        with open(self.configpath,'r') as configjson:
            # config json has styling data like colors and fonts
            configjson=json.load(configjson)
            for key, value in configjson.items():
                if isinstance(value, str) and '#' in value:
                    configjson[key] = value.replace('#', '')
        
        config={
        "departmentname":self.sampledepartmentname,
        "universityname":self.universityname,
        "savepath":savepath,
        "rows":self.samplerows,
        }
        
        config.update(configjson)

        # this is an imported function defined it init
        self.make_excelfile(**config)


def main():
    '''

    '''

    def finish_config_path(unfinished_path):
        """
        Resolves a path relative to the directory of the running script.
        Works with partial paths, relative paths, or absolute paths.
        """

        base_dir = Path(__file__).resolve().parent.parent   # directory of ExcelTesting.py
        path = Path(unfinished_path)
          # go one level up
    
    
    
    

        if path.is_absolute():
            return path                               # already absolute → leave it alone
        
        finishedpath=(base_dir / path).resolve()
        print(f'Finished path: {finishedpath}')
        return finishedpath

    utexceltesting=exceltesting('UT Austin',finish_config_path('utcourses/uniexcelconfig.json'))
    utexceltesting.make_themed_file()
   

if __name__ == "__main__":
    main()