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
import importlib.util

from createuniversity import createUniversity
from utdegreeplans import createWebsite

# sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from degreeview_expansion.newcatalogdata import catalogData

class createPages:
    def __init__(self):
        # havent used this yet
        self.websitepath='/Users/shalevwiden/Downloads/Projects/degreeviewwebsite'

        BASE_DIR = Path(__file__).resolve().parent
        print(f'BASE_DIR {BASE_DIR}')
        self.universityuldatapath= BASE_DIR.parent / 'websiteprogramming' / "json"/ "universityuldata.json"

        self.imagesjsonpath= BASE_DIR.parent / 'websiteprogramming' / "json"/ "images.json"
        self.excelimagesjsonpath= BASE_DIR.parent / 'websiteprogramming' / "json"/ "excelimages.json"

        self.footertemplatepath=BASE_DIR.parent / "sourcefiles" / "html_components" / "dvfooter.html"
        self.headtagpath=BASE_DIR.parent / "sourcefiles" / "googleanalytics_tags" / "headtag.html"



        with open(self.imagesjsonpath) as imagejson:
            self.images = json.load(imagejson)

        with open(self.excelimagesjsonpath) as excelimagejson:
            self.excelimages = json.load(excelimagejson)
        
        
        with open(self.headtagpath) as headtag:
            self.headtag=headtag.read()


       




        env = Environment(loader=FileSystemLoader("templating/templates"))

        # define all the templates to be used
        self.indextemplate = env.get_template("main_templates/indextemplate.html")
        self.mainstatstemplate=env.get_template("main_templates/mainstatspage.html")
        self.abouttemplate=env.get_template("main_templates/abouttemplate.html")
        self.exceltemplate_template=env.get_template("main_templates/exceltemplates-template.html")


        
        self.footertemplate=env.get_template('components/dvfooter.html')

        aboutpath = "about.html"
        indexpath = "index.html"
        exceltemplatespath = "exceltemplates.html"
        statspath = "degreeviewstats.html"

        footerdata = {
            "aboutpath": aboutpath,
            "indexpath": indexpath,
            "exceltemplatespath": exceltemplatespath,
            "statspath": statspath,
            "minilogo":self.images.get('minilogo')
        }

        self.rendered_footer=self.footertemplate.render(footerdata)

        # use these when making big changes

        self.data=True
        self.web=True

        self.totalcourses=0
        self.excelfilecount=0

        # just update this manuallyfor now lmao
        self.universitycount=7
        

    def buildspecs(self,schoolfolder,universityname,websitefolder, schoolabrv):

        '''
        change this to change the arguments that are passed into a class
        I think here I can do defaults like _ if _ else _
        Just put the defaults at the top of this function like placeholder='default'
        '''
        # website folder has to match schoolabrv
        return {"schoolfolder":schoolfolder,
    "universityname": universityname,
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
                    "The University of Texas at Austin",
                    os.path.join(self.websitepath,'ut'),
                    "UT")
            

                def data_methods():
                    utcatalogobj=catalogData(**ut_specs)
                    print(f'Configs folder: {utcatalogobj.configsfolder}')
                    
                    utcatalogobj.makestatsjson()


                    # utcatalogobj.make_excel_files()
                    utcatalogobj.create_univeristy_files()
                    utcatalogobj.make_sorteddepartment_json()
                    utcatalogobj.make_university_statsjson()

                    # utcatalogobj.upload_department_files()

                if self.data:    
                    print('making data for UT')
                    # data_methods()

                def web_methods():
                    utobj=createUniversity(**ut_specs)
                    # do this for UT but not all others
                    utobj.create_department_pages()
                    

                    utobj.createletterpages()
                    utobj.create_sorteddepartments_page()
                    utobj.create_departmentpagelinks_json()

                    # instead of calling all of the functions 
                    # utobj.createletterpages()

                    '''
                    These two functions are actually not called for UT because UT is special
                    UT is the original DV
                    
                    Update Feb 13: Nah UT is standardized now they are called lol
                    '''

                    utobj.createstatspage()
                    utobj.create_uni_homepage()
                    # this one is tho I think...
                    '''
                    Now UT degree plans stuff

                    This actually shouldn't really be done
                    '''
                    
                    def original_ut_stuff():
                        BASE_DIR = Path(__file__).resolve().parent
                        asset_path = BASE_DIR / "json" / "theasset.json"

                        with open(asset_path) as assetjson:
                            theasset = json.load(assetjson)

                        def unpacktheasset_into_createSchoolpages(theasset):
                            for schooldict in theasset[0:]:
                                print(schooldict[list(schooldict)[0]])
                                utdegreeplans=createWebsite(schooldata=schooldict,websitepath='/Users/shalevwiden/Downloads/Projects/degreeviewwebsite/ut/degreeplans')
                                
                                utdegreeplans.createschoolpages()
                                utdegreeplans.create_degree_pages()
                                utdegreeplans.create_renderedcsv_pages()
                                

                        unpacktheasset_into_createSchoolpages(theasset=theasset)

                    # original_ut_stuff()
                    
                if self.web:
                    web_methods()

            def rice():
                # update all of this with rice data
                rice_specs=self.buildspecs(
                    "degreeview_expansion/rice",
                    "Rice University",

                    # so I can probably make a function to finish this path for whereever I actually host the website
                    os.path.join(self.websitepath,'rice'),schoolabrv="Rice")
                
            
                # instead of calling all of the functions 

                def data_methods():
                    ricecatalogobj=catalogData(**rice_specs)
                    # ricecatalogobj.upload_to_database()
                    ricecatalogobj.makestatsjson()
                    # ricecatalogobj.make_excel_files()
                    ricecatalogobj.create_univeristy_files()
                    ricecatalogobj.make_sorteddepartment_json()
                    ricecatalogobj.make_university_statsjson()
                    # ricecatalogobj.upload_department_files()

                if self.data:   
                    print(f'Doing data for rice if self.data true lol')
                    data_methods()

                def web_methods():
                    riceobj=createUniversity(**rice_specs)

                    # riceobj.createletterpages()

                    # riceobj.upload_department_files()
                    riceobj.create_department_pages()
                    riceobj.create_departmentpagelinks_json()

                    riceobj.createstatspage()
                    riceobj.create_sorteddepartments_page()
                    riceobj.create_uni_homepage()
                    
                if self.web:
                    web_methods()
            # call all the school functions here
            def utsa():
                # update all of this with utsa data
                utsa_specs=self.buildspecs(
                    "degreeview_expansion/utsa",
                    "University of Texas at San Antonio"
                    ,"https://storage.googleapis.com/utsacourses",

                    # so I can probably make a function to finish this path for whereever I actually host the website
                    os.path.join(self.websitepath,'utsa'),schoolabrv="utsa")
                
            
                # instead of calling all of the functions 

                def data_methods():
                    utsacatalogobj=catalogData(**utsa_specs)

                    utsacatalogobj.upload_to_database()
                    utsacatalogobj.makestatsjson()
                    # utsacatalogobj.make_excel_files()
                    utsacatalogobj.create_univeristy_files()
                    utsacatalogobj.make_sorteddepartment_json()
                    utsacatalogobj.make_university_statsjson()

                if self.data:   
                    # data_methods()
                    print('doing data methods for utsa')

                def web_methods():
                    utsaobj=createUniversity(**utsa_specs)

                    # utsaobj.createletterpages()

                    # utsaobj.upload_department_files()
                    utsaobj.create_department_pages()
                    utsaobj.create_departmentpagelinks_json()

                    utsaobj.createstatspage()
                    utsaobj.create_sorteddepartments_page()
                    utsaobj.create_uni_homepage()
                    
                if self.web:
                    web_methods()
            # call all the school functions here
            
            def txstate():
                # update all of this with rice data
                txstate_specs=self.buildspecs(
                "degreeview_expansion/tx_state",
                "Texas State University",

                # so I can probably make a function to finish this path for whereever I actually host the website

                # ok the website path is different than the school abrv
                os.path.join(self.websitepath,'tx_state'),schoolabrv="TX_State")
                
            
                # instead of calling all of the functions 

                def data_methods():
                    txstatecatalogobj=catalogData(**txstate_specs)
                    # txstatecatalogobj.upload_to_database()
                    txstatecatalogobj.makestatsjson()
                    # txstatecatalogobj.make_excel_files()
                    txstatecatalogobj.create_univeristy_files()
                    txstatecatalogobj.make_sorteddepartment_json()
                    txstatecatalogobj.make_university_statsjson()
                    
                # data_methods()

                def web_methods():
                    txstateobj=createUniversity(**txstate_specs)

                    # txstateobj.createletterpages()

                    # txstateobj.upload_department_files()
                    txstateobj.create_department_pages()
                    txstateobj.create_departmentpagelinks_json()
                    txstateobj.createstatspage()
                    txstateobj.create_sorteddepartments_page()
                    txstateobj.create_uni_homepage()
                    
                if self.web:

                    web_methods()
            
            ut()
            rice()
            txstate()
            
        def california():
            def stanford():
                 
                #  we'll do bucket stuff later

                stanford_specs=self.buildspecs(
                    "degreeview_expansion/stanford",
                    "Stanford University"
                    ,
                    os.path.join(self.websitepath,'stanford'),
                    "Stanford")
                
                def data_methods():
                    stanfordcatalogobj=catalogData(**stanford_specs)
                    print(f'Configs folder: {stanfordcatalogobj.configsfolder}')
                    
                    # stanfordcatalogobj.upload_to_database()
                    
                    stanfordcatalogobj.makestatsjson()
                    # stanfordcatalogobj.make_excel_files()
                  # stanfordcatalogobj.create_univeristy_files()
                    # stanfordcatalogobj.make_sorteddepartment_json()
                    # stanfordcatalogobj.make_university_statsjson()

                data_methods()

                def web_methods():
                    stanfordobj=createUniversity(**stanford_specs)

                    # stanfordobj.createletterpages()

                    # stanfordobj.upload_department_files()
                    stanfordobj.create_department_pages()
                    stanfordobj.create_departmentpagelinks_json()

                    stanfordobj.createstatspage()
                    stanfordobj.create_sorteddepartments_page()
                    stanfordobj.create_uni_homepage()
                    
                if self.web:

                    web_methods()
            def ucberkeley():
                 
                #  we'll do bucket stuff later

                ucberkeley_specs=self.buildspecs(
                    "degreeview_expansion/ucberkeley",
                     "University of California Berkeley"
                    ,
                    os.path.join(self.websitepath,'uc_berkeley'),
                    "UC_Berkeley")
                
                def data_methods():
                    ucberkeleycatalogobj=catalogData(**ucberkeley_specs)
                    print(f'Configs folder: {ucberkeleycatalogobj.configsfolder}')
                    
                    # ucberkeleycatalogobj.upload_to_database()
                    # ucberkeleycatalogobj.upload_stragglers_todb()
                    
                    ucberkeleycatalogobj.makestatsjson()
                    # ucberkeleycatalogobj.make_excel_files()
                    ucberkeleycatalogobj.create_univeristy_files()
                    ucberkeleycatalogobj.make_sorteddepartment_json()
                    ucberkeleycatalogobj.make_university_statsjson()

                data_methods()

                def web_methods():
                    ucberkeleyobj=createUniversity(**ucberkeley_specs)

                    # ucberkeleyobj.createletterpages()

                    # ucberkeleyobj.upload_department_files()
                    ucberkeleyobj.create_department_pages()
                    ucberkeleyobj.create_departmentpagelinks_json()

                    ucberkeleyobj.createstatspage()
                    ucberkeleyobj.create_sorteddepartments_page()
                    ucberkeleyobj.create_uni_homepage()
                    
                if self.web:
                    web_methods()


            def ucsb():
                 
                #  we'll do bucket stuff later

                ucsb_specs=self.buildspecs(
                    "degreeview_expansion/ucsb",
                     "University of California Santa Barbara",
                    os.path.join(self.websitepath,'ucsb'),
                    "ucsb")
                
                def data_methods():
                    ucsbcatalogobj=catalogData(**ucsb_specs)
                    print(f'Configs folder: {ucsbcatalogobj.configsfolder}')
                    
                    # ucsbcatalogobj.upload_to_database()
                    # ucsbcatalogobj.upload_stragglers_todb()
                    
                    ucsbcatalogobj.makestatsjson()
                    # ucsbcatalogobj.make_excel_files()
                    ucsbcatalogobj.create_univeristy_files()
                    ucsbcatalogobj.make_sorteddepartment_json()
                    ucsbcatalogobj.make_university_statsjson()

                data_methods()

                def web_methods():
                    ucsbobj=createUniversity(**ucsb_specs)

                    # ucsbobj.createletterpages()

                    # ucsbobj.upload_department_files()
                    ucsbobj.create_department_pages()
                    ucsbobj.create_departmentpagelinks_json()

                    ucsbobj.createstatspage()
                    ucsbobj.create_sorteddepartments_page()
                    ucsbobj.create_uni_homepage()
                    
                if self.web:
                    web_methods()


            ucberkeley()
            stanford()
            ucsb()


        def newyork():
            def cornell():
                 
                #  we'll do bucket stuff later

                cornell_specs=self.buildspecs(
                    "degreeview_expansion/cornell",
                     "Cornell University",
                    os.path.join(self.websitepath,'cornell'),
                    "Cornell")
                
                def data_methods():
                    cornellcatalogobj=catalogData(**cornell_specs)
                    print(f'Configs folder: {cornellcatalogobj.configsfolder}')
                    
                    # cornellcatalogobj.upload_to_database()
                    # cornellcatalogobj.upload_stragglers_todb()
                    
                    cornellcatalogobj.makestatsjson()
                    # cornellcatalogobj.make_excel_files()
                    cornellcatalogobj.create_univeristy_files()
                    cornellcatalogobj.make_sorteddepartment_json()
                    cornellcatalogobj.make_university_statsjson()

                data_methods()

                def web_methods():
                    cornellobj=createUniversity(**cornell_specs)

                    # cornellobj.createletterpages()

                    # cornellobj.upload_department_files()
                    cornellobj.create_department_pages()
                    cornellobj.create_departmentpagelinks_json()

                    cornellobj.createstatspage()
                    cornellobj.create_sorteddepartments_page()
                    cornellobj.create_uni_homepage()
                    
                if self.web:
                    web_methods()
            cornell()
        def rhodeisland():
            def brown():
                 
                #  we'll do bucket stuff later

                brown_specs=self.buildspecs(
                    "degreeview_expansion/brown",
                     "Brown University",
                    os.path.join(self.websitepath,'brown'),
                    "Brown")
                
                def data_methods():
                    browncatalogobj=catalogData(**brown_specs)
                    print(f'Configs folder: {browncatalogobj.configsfolder}')
                    
                    # browncatalogobj.upload_to_database()
                    # browncatalogobj.upload_stragglers_todb()
                    
                    browncatalogobj.makestatsjson()
                    # browncatalogobj.make_excel_files()
                    browncatalogobj.create_univeristy_files()
                    browncatalogobj.make_sorteddepartment_json()
                    browncatalogobj.make_university_statsjson()

                data_methods()

                def web_methods():
                    brownobj=createUniversity(**brown_specs)

                    # brownobj.createletterpages()

                    # brownobj.upload_department_files()
                    brownobj.create_department_pages()
                    brownobj.create_departmentpagelinks_json()

                    brownobj.createstatspage()
                    brownobj.create_sorteddepartments_page()
                    brownobj.create_uni_homepage()
                    
                if self.web:
                    web_methods()
            brown()
        
        # texas()
        # california()
        newyork()
        rhodeisland()

    
    def create_main_statspage(self):
        '''
        Uses the main stats page template to create the HTML file for the main stats 
        of DegreeView (# schools, longest coursename so far, etc)

        Opens degreeview expansion folder because thats where all the assets are
        '''

        totalcourses=0
        totaldepartments=0

        excelfilecount=0
        BASE_DIR = Path(__file__).resolve().parent
        print(f'BASE_DIR {BASE_DIR}')
        base_path = BASE_DIR.parent / "degreeview_expansion"


        for folder in os.listdir(base_path):
            folder_path = os.path.join(base_path, folder)

            # Make sure it's actually a directory
            if os.path.isdir(folder_path): 
                assets_path = os.path.join(folder_path, "assets") 

                if os.path.isdir(assets_path): 
                    print("Found assets folder:", assets_path,'\n')

                    # getting the excel file count now
                    for root, dirs, files in os.walk(assets_path):
                        for file in files:
                            # Excel files: .xlsx or .xls
                            # Exclude temp files starting with $
                            if (
                                (file.endswith(".xlsx") or file.endswith(".xls"))
                                and not file.startswith("$") and "original" in file
                            ):
                                excelfilecount += 1

                    universitywidefolder=os.path.join(base_path,folder,'assets','universitywidefolder')

                    unistatsjson=os.path.join(universitywidefolder,'universitystatsjson.json')

                    with open(unistatsjson) as statsjson:
                        universitystatsdict=json.load(statsjson)
                        coursecount=universitystatsdict.get('coursecount')
                        departmentcount=universitystatsdict.get('departmentcount')
                        totalcourses+=coursecount
                        totaldepartments+=departmentcount
                    # next open the sorted departments, get the top dept, and compare those

        def get_excel_file_in_bucket_count():
            '''
            
            This uses a command to get the Excel file count but it takes forever so probably not the move

            '''

            result = subprocess.run(
            ["gsutil", "ls", "-r","gs://degreeviewsite"],
            capture_output=True,
            text=True,
            shell=False
            )

            if result.returncode != 0:
                print("Error:", result.stderr)
                return 0

            file_count = len(result.stdout.strip().splitlines())
            return file_count
        
        
        print(f'Total courses: {totalcourses}')
        print(f'Total departments: {totaldepartments}')

        # do this to call an operation on the bucket
        # excelfilecount=get_excel_file_in_bucket_count()

        excelfilecount*=2
        self.totalcourses = f"{totalcourses:,}"
        self.excelfilecount=f"{excelfilecount:,}"

        




        template_data={
            "headtag": self.headtag,

            "universities":self.universitycount,
            "totalcourses":self.totalcourses,
            "totaldepartments":totaldepartments,
            "biggestdepartments":[],
            "excelfilecount": self.excelfilecount,
            "footer":self.rendered_footer
                }

        template_data.update(self.images)

        mainstatspath=os.path.join(self.websitepath,'degreeviewstats.html')

        mainstatspagerendered=self.mainstatstemplate.render(template_data)

        with open(mainstatspath,'w') as mainstats:
            mainstats.write(mainstatspagerendered)
    def createindex(self):
        '''
        Creates the MAIN home page index
        '''
        # the key is what will be dislayed on the index, as in the school name the user will read.
        '''
        Technicalities to be aware of here:
        The box color will actually be set in scss.
        This is because with different colors I'll also have to adjust the TEXT color of the box.
        Therefore doing it in scss is the best approach
        '''

        with open(self.universityuldatapath,'r') as universityuldatajson:
            universityuldata=json.load(universityuldatajson)


        template_data={
            "headtag": self.headtag,
            "universityuldata":universityuldata,
            "universitycount":self.universitycount,
            "totalcourses": self.totalcourses,
            "biggestdepartments":[],
            "excelfilecount": self.excelfilecount,
            "footer":self.rendered_footer,     
        }
        
        template_data.update(self.images)

        mainindexrendered=self.indextemplate.render(template_data)

        mainindexpath=os.path.join(self.websitepath,'index.html')

        with open(mainindexpath,'w') as mainindex:
            mainindex.write(mainindexrendered)

    def createabout(self):
        '''
        Creates the aboutpage
        '''
        # the key is what will be dislayed on the index, as in the school name the user will read.
        '''
        Technicalities to be aware of here:
        The box color will actually be set in scss.
        This is because with different colors I'll also have to adjust the TEXT color of the box.
        Therefore doing it in scss is the best approach
        '''



        template_data={
            "headtag": self.headtag,
            "footer":self.rendered_footer
          
                       }
        template_data.update(self.images)

        
        aboutrendered=self.abouttemplate.render(template_data)

        aboutpath=os.path.join(self.websitepath,'about.html')

        with open(aboutpath,'w') as about:
            about.write(aboutrendered)

    def create_exceltemplates_template(self):
        '''
        Creates the aboutpage
        '''
        # the key is what will be dislayed on the index, as in the school name the user will read.
        '''
        Technicalities to be aware of here:
        The box color will actually be set in scss.
        This is because with different colors I'll also have to adjust the TEXT color of the box.
        Therefore doing it in scss is the best approach
        '''



        template_data={
            "headtag": self.headtag,
            "footer":self.rendered_footer
          
                       }
        template_data.update(self.images)
        template_data.update(self.excelimages)


        
        etrendered=self.exceltemplate_template.render(template_data)

        etpath=os.path.join(self.websitepath,'exceltemplates.html')

        with open(etpath,'w') as etfile:
            etfile.write(etrendered)

    def create_unilinks(self):
        '''
        this function needs to create unilinks.json

        Unilinks.json is what supports the random university button.
        '''
        pass

def main():
    # print(os.getcwd())

    createpagesobj=createPages()

    createpagesobj.schoolcontainingfunc()
    createpagesobj.create_main_statspage()
    createpagesobj.createindex()
    createpagesobj.createabout()
    createpagesobj.create_exceltemplates_template()

if __name__=="__main__":
    main()