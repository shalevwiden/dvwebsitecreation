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

from excel_templates import make_checkerboardfile, make_excelfile



# add parent folder to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from createuniversity import createuniversity
import importlib


class CatalogData(createUniversity):
    def __init__(self, schoolfolder, universityname, cloudbucketpath, websitefolder, schoolabrv):
        super().__init__(schoolfolder, universityname, cloudbucketpath, websitefolder, schoolabrv)
        # child specific methods
        
        self.catalogfile = None
        self.course_list = []