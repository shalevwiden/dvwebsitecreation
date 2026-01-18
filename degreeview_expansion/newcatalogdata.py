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

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
print(os.path.dirname(os.path.dirname(__file__)))

from .excel.functions import make_checkerboard, make_excelfile



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
        # child specific
        self.make_excelfile=make_excelfile
        BASE_DIR = Path(__file__).resolve().parent
        CONFIGS_DIR = os.path.join(str(BASE_DIR), 'excel','configs')
            
        self.configsfolder=CONFIGS_DIR

        # pass this in as an argument to the init
        # then in the make_excel_files() function loop over this and create as many configs as is here pretty much
        self.excelconfigs_list=[]
        
        
   

    def finishconfigpath(self,endofpath):
        '''
        This is for configs and is not related to saving the file at all
        This is related to excel files
        '''
        return os.path.join(self.configsfolder,endofpath)

   

    def upload_to_database(self):
        '''
        
        Uses SQLite to upload to databases.
        We will then to quieries on said databases.

        For UTD, instead of the category column, its the notes column. 
        Its creating 3 times just because it still needs to be wiped.

        This was fucking tricky.

        Make a video e

        
        '''
        for startingletter in self.alphabetizeddict:

            '''
            More complex logic now with multiple stuff on one page.

            We will use similar logic for UTSA.

            I'll also need to create some databases for each notes ... maybe.
            For that I could just use the utcoursescraping file since just the notes will be much faster.

             


            '''

            letterfolder=os.path.join(self.asset_folder_path,startingletter)
            if not os.path.exists(letterfolder):
                os.mkdir(letterfolder)
            
            letterdict=self.alphabetizeddict[startingletter]
            for departmentname in letterdict:
                departmenturl=letterdict[departmentname]

                (
                departmentname,
                departmentnamecleaned,
                displaydepartmentname,
                departmentnamehalf,
                departmentcode,
                ) = self.get_departmentnames(departmentname)

                departmentfolderpath=os.path.join(letterfolder,departmentname)


                if not os.path.exists(departmentfolderpath):
                    os.mkdir(departmentfolderpath)
                        # now get the SQL stuff right, then just copy paste. 
                def database_logic():
                # its a little different from the database name, use underscore instead of hyphen
                    '''
                    There was a tricky problem with the seconds...thats why I used SECOND
                    '''

                    

                    databasepath=os.path.join(departmentfolderpath,f'{departmentnamecleaned}-database.db')

                    # start fresh

                    if os.path.exists(databasepath):
                        os.remove(databasepath)
                    # hyphens and commas not allowed in tablename

                    tablename=self.get_tablename()

                    def maketable():
                        '''This creates the table for course data in the db'''

                        # this line makes the db
                        with sqlite3.connect(databasepath) as conn:
                            cursor=conn.cursor()

                        # table name lowercase- since we changed from notes to category we also changed UpperDivStatus-UpperLowerStatus
                            createtablecommand=f'''CREATE TABLE IF NOT EXISTS "{tablename}" (coursename TEXT , coursecode TEXT, coursehours TEXT, classification TEXT);'''
                            cursor.execute(createtablecommand)
                            conn.commit()
                    maketable()
                        
                    with sqlite3.connect(databasepath) as conn:
                        cursor=conn.cursor()
                        departmentdata=self.scrapecourses(departmenturl=departmenturl)
                        for coursename in departmentdata:
                            coursecode,coursehours,classification=departmentdata[coursename]
                            # established second and third in scrape courses
                            coursename=coursename.replace('SECOND','').replace('THIRD','')
                            cursor.execute(f'INSERT INTO {tablename} (coursename, coursecode, coursehours, classification) values(?,?,?,?);',
                                        [coursename,coursecode,coursehours,classification])
                                    


                                
                        # commit to the database 
                        conn.commit()
                        print(f'Created {departmentnamecleaned}-database.db\n')
                database_logic()

    def makestatsjson(self):
        '''
        
        This function will make a stats JSON that will be used in the createuniversity.py.
        
        '''        

        for startingletter in self.alphabetizeddict:


            letterfolder=os.path.join(self.asset_folder_path,startingletter)
            if not os.path.exists(letterfolder):
                os.mkdir(letterfolder)
            
            letterdict=self.alphabetizeddict[startingletter]

            for departmentname in letterdict:
                departmenturl=letterdict[departmentname]

                # make the slashes underscores. This will normalize it. Then in the createwebsite.py, I've already coded ways to unnormalize it. 
                (
                departmentname,
                departmentnamecleaned,
                displaydepartmentname,
                departmentnamehalf,
                departmentcode,
                ) = self.get_departmentnames(departmentname)

                departmentfolderpath=os.path.join(letterfolder,departmentname)

                databasepath=os.path.join(departmentfolderpath,f'{departmentnamecleaned}-database.db')
                

                tablename=self.get_tablename()


                def getdatabasestats():
                    '''
                    These are all the column names: coursename, coursecode, coursehours, classification
                    '''
                    with sqlite3.connect(databasepath) as conn:
                            cursor=conn.cursor()

                    def get_department_coursecount():
                        countcoursescommand=f'''

                        SELECT coursename 
                        FROM {tablename} 
                        WHERE coursename IS NOT NULL AND coursename != ''
                        '''


                        cursor.execute(countcoursescommand)
                        courselist = cursor.fetchall()
                        courselist=[row[0] for row in courselist] 

                        return len(courselist)
                        
                    def get_longest_coursename():
                        longestnamecommand=f'''
                        SELECT coursename 
                        FROM {tablename} 
                        WHERE Coursename IS NOT NULL AND coursename != ''
                        ORDER BY LENGTH(coursename) DESC LIMIT 1;
                        
                        '''


                        cursor.execute(longestnamecommand)
                        longestresult=cursor.fetchone()[0]   

                        return longestresult                 

                                     
                    def get_shortest_coursename():


                        shortestnamecommand=f'''
                        SELECT coursename 
                        FROM {tablename} 
                        WHERE coursename IS NOT NULL AND coursename != ''
                        ORDER BY LENGTH(Coursename) ASC LIMIT 1;'''

                        cursor.execute(shortestnamecommand)

                        shortestresult=cursor.fetchone()[0]   
                        return shortestresult

                    def getaveragelength():
                        getcoursescommand=f'''

                        SELECT coursename 
                        FROM {tablename} 
                        WHERE coursename IS NOT NULL AND coursename != ''
                        '''


                        cursor.execute(getcoursescommand)

                        courselist = cursor.fetchall()
                        courselist=[row[0] for row in courselist]
                        total=0
                        for course in courselist:
                            total+=len(course)
                        averagelength=total/len(courselist)
                        return averagelength
                    
                    def get_classification_percents():
                        '''
                        This returns what percent is upper divison, lower division, and graduate, if applicable. 
                        '''
                        classificationlistcommand=f'''

                        SELECT classification 
                        FROM {tablename} 
                        WHERE classification IS NOT NULL AND classification != ''
                        '''


                        cursor.execute(classificationlistcommand)
                        classificationlist = cursor.fetchall()
                        classificationlist=[row[0].lower() for row in classificationlist] 

                        # print(f'{departmentname} classificationlist: {classificationlist}')


                        lowercount=0
                        uppercount=0
                        gradcount=0
                        total=len(classificationlist)

                        for classification in classificationlist:
                            # must do this in the database for all schools
                            if "lower" in classification:
                                lowercount+=1
                            elif "upper" in classification:
                                uppercount+=1
                            elif "grad" in classification:
                                gradcount+=1
                        lowerpercent=lowercount/total
                        upperpercent=uppercount/total
                        gradpercent=gradcount/total
                        
                        return lowercount,uppercount,gradcount,lowerpercent,upperpercent,gradpercent

                    def get_courseswithdepartmentnameinthem(departmentname):
                        countcoursescommand=f'''

                        SELECT coursename 
                        FROM {tablename} 
                        WHERE coursename IS NOT NULL AND coursename != ''
                        '''


                        cursor.execute(countcoursescommand)
                        courselist = cursor.fetchall()
                        courselist=[row[0] for row in courselist]
                        
                        departmentname=departmentname.split('-')[-1].lower()
                        print(f'departmentname {departmentname}')

                        samenamelist=[]
                        for course in courselist:
                            if departmentname in course.lower():
                                samenamelist.append(course)
                        print(samenamelist)
                        samenamepercent=len(samenamelist)/len(courselist)
                        return len(samenamelist),samenamepercent


                        
                    longestcoursename = get_longest_coursename()
                    shortestcoursename = get_shortest_coursename()
                    coursecount = get_department_coursecount()
                    lowercount, uppercount, gradcount, lowerpercent, upperpercent, gradpercent = get_classification_percents()
                    samenamelen,samenamepercent=get_courseswithdepartmentnameinthem(departmentname=departmentname)
                    averagelength=getaveragelength()


                    statsdict = {
                            "course_count": coursecount,
                            "longest_course_name": longestcoursename,
                            "shortest_course_name": shortestcoursename,
                            "average_course_length":f'{averagelength:.0f}',
                            
                                "lower_count": lowercount,
                                "upper_count": uppercount,
                                "grad_count": gradcount,
                                "lower_percent": f"{lowerpercent*100:.1f}%",
                                "upper_percent": f"{upperpercent*100:.1f}%",
                                "grad_percent": f"{gradpercent*100:.1f}%",
                                "samenamelen":samenamelen,
                                "samenamepercent": f"{samenamepercent*100:.1f}%"
                            
                            }

                    return statsdict
                
                def jsonfilemaking(departmentnamecleaned):
                    statsjsonpath=os.path.join(departmentfolderpath,f'{departmentnamecleaned}-statsjson.json')

                    statsdict=getdatabasestats()



                    with open(statsjsonpath,'w') as statsfile:
                        json.dump(statsdict,statsfile,indent=4)

                jsonfilemaking(departmentnamecleaned=departmentnamecleaned)   
               

    def createcsvs(self):
        '''
        SO RIGHT NOW
        THIS ISNT UP TO SPEED
        Because insted of scraping I read it from a database

        '''
        for startingletter in self.alphabetizeddict:

            '''
            '''

            letterfolder=os.path.join(self.asset_folder_path,startingletter)
            if not os.path.exists(letterfolder):
                os.mkdir(letterfolder)
            
            letterdict=self.alphabetizeddict[startingletter]
            for departmentname in letterdict:
                departmenturl=letterdict[departmentname]

                (
                departmentname,
                departmentnamecleaned,
                displaydepartmentname,
                departmentnamehalf,
                departmentcode,
                ) = self.get_departmentnames(departmentname)                
                departmentfolderpath=os.path.join(letterfolder,departmentname)

                if not os.path.exists(departmentfolderpath):
                    os.mkdir(departmentfolderpath)

        
            # use the fact that its an underscore to readd it later in the website creation file
            

                departmentcourses_csv=os.path.join(departmentfolderpath,f'{departmentnamecleaned}-coursescsv.csv')

                with open(departmentcourses_csv,'w') as departmentcourses_csv:

                    departmentdict=self.scrapecourses(departmenturl=departmenturl)

                    # expirementing with quoting cause why not
                    writer=csv.writer(departmentcourses_csv,quotechar='"', delimiter=',')
                    headings=['Coursename','Coursecode','Hours', 'Classification']
                    writer.writerow(headings)

                    writelist=[]
                    totalhours=0
                    for coursename in departmentdict:
                        coursecode,coursehours,status=departmentdict[coursename]
                        coursename=coursename.replace('SECOND','').replace('THIRD','')

                        values=[coursename,coursecode,coursehours,status]  
                        writelist.append(values)

                        
                        if ',' in coursehours:
                            coursehourcount=3
                        else:
                            coursehourcount=coursehours.strip()[-1]

                        
                        totalhours+=int(coursehourcount)
                    
                    writer.writerows(writelist)
                    writer.writerow(['','',f'Total Hours: {totalhours}'])
                    writer.writerow(['DegreeView'])

    def make_excel_files(self):
            
        '''
        This uses the result of the scrape semester data function to make an excel file out of it.
        For the CSV files I did them fully vertical. For these excel files, since I can control what columns and cells things are going,
        I want it to be more of a horizontal feel. 

        '''
        for startingletter in self.alphabetizeddict:
            
            letterfolder=os.path.join(self.asset_folder_path,startingletter)
            if not os.path.exists(letterfolder):
                os.mkdir(letterfolder)
            
            letterdict=self.alphabetizeddict[startingletter]
            for departmentname in letterdict:

                # single excel file logic
                if self.single_department and departmentname != self.random_dept:
                    continue
                
                departmenturl=letterdict[departmentname]

                (
                departmentname,
                departmentnamecleaned,
                displaydepartmentname,
                departmentnamehalf,
                departmentcode,
                ) = self.get_departmentnames(departmentname)   

                def make_required_folders():
                    departmentfolderpath=os.path.join(letterfolder,departmentname)

                    excelfolderpath=os.path.join(departmentfolderpath,'excelthemes')

                    if not os.path.exists(departmentfolderpath):
                        os.mkdir(departmentfolderpath)


                    if not os.path.exists(excelfolderpath):
                        os.mkdir(excelfolderpath)

                    return departmentfolderpath, excelfolderpath

                departmentfolderpath, excelfolderpath=make_required_folders()
            
            # use the fact that its an underscore to readd it later in the website creation file
              

              

                databasepath=os.path.join(departmentfolderpath,f'{departmentnamecleaned}-database.db')

                # hyphens and commas not allowed in tablename
                tablename=self.get_tablename()
                def getdatabasedata():
                    '''
                    These are all the column names: coursename, coursecode, coursehours, classification
                    '''
                    with sqlite3.connect(databasepath) as conn:
                        cursor=conn.cursor()

                        getalldata=f'''

                        SELECT *
                        FROM {tablename} 
                        WHERE coursename IS NOT NULL AND coursename != ''
                        '''


                        cursor.execute(getalldata)
                        rows = cursor.fetchall()                        
                        newrows=[]
                        for row in rows:
                            rowlist=list(row)
                            newrows.append(rowlist)
                        return newrows
                
                rows=getdatabasedata()
                # everything that follows is like the with open but for excel
                '''
                Use Font and OpenPyXL to create nicely formatted tabular data
                '''
                utconfig=self.finishconfigpath('uniconfigs/ut.json')
                originalconfig=self.finishconfigpath('originalconfig.json')
                darkthemeconfig=self.finishconfigpath('darkthemeconfig.json')
                redconfig=self.finishconfigpath('colorconfigs/redtheme.json')
                blueconfig=self.finishconfigpath('colorconfigs/bluetheme.json')
                checkerboardconfig=self.finishconfigpath('checkerboardconfigs/brownconfig.json')

                def make_themed_file(configpath,themename):
                    '''
                    This is a modular way to make excel files.
                    '''
                    filename=f'{departmentnamecleaned}-{themename.lower().replace(' ','').strip()}.xlsx'
                    # change this line to change the save path
                    # kinda
                    savepath=os.path.join(excelfolderpath,filename)
                    with open(configpath,'r') as configjson:
                        # config json has styling data like colors and fonts
                        configjson=json.load(configjson)
                    
                    config={
                    "departmentname":departmentname,
                    "universityname":self.universityname,
                    "savepath":savepath,
                    "rows":rows,
                    }
                    
                    config.update(configjson)

                    # this is an imported function defined it init
                    self.make_excelfile(**config)

                make_themed_file(utconfig,'UT-theme')
                make_themed_file(originalconfig,"original-theme")
                make_themed_file(darkthemeconfig,'darktheme')
                make_themed_file(redconfig,'red-theme')
                make_themed_file(blueconfig,'blue-theme')

        
    def create_univeristy_files(self):
        '''what this function will do is initialize the University Wide files.
        This includes the University Wide Database, and some csv files I'm thinking
        '''


    # this will rewrite it everytime I start the file. Clearing it

        def make_universidewide_csv():
            universitywidecsvpath=os.path.join(self.universitywidefolder,'universitywidecsv.csv')

            with open(universitywidecsvpath,'w') as universitywidecsv:
                writer=csv.writer(universitywidecsv)
                writer.writerow(['Courses','',"","",'The University of Texas at Austin'])


                writer.writerow(['Coursename','Coursecode','Coursehours','Classification',"Department Name"])
                writer.writerow([])


            for startingletter in self.alphabetizeddict:

                
                

                    
                

                letterfolder=os.path.join(self.asset_folder_path,startingletter)
                if not os.path.exists(letterfolder):
                    os.mkdir(letterfolder)
                
                letterdict=self.alphabetizeddict[startingletter]

                for departmentname in letterdict:
                    departmenturl=letterdict[departmentname]

                    # make the slashes underscores. This will normalize it. Then in the createwebsite.py, I've already coded ways to unnormalize it. 
                    (
                    departmentname,
                    departmentnamecleaned,
                    displaydepartmentname,
                    departmentnamehalf,
                    departmentcode,
                    ) = self.get_departmentnames(departmentname)   

                    departmentfolderpath=os.path.join(letterfolder,departmentname)

                        
                    
                    databasepath=os.path.join(departmentfolderpath,f'{departmentnamecleaned}-database.db')

                    # hyphens and commas not allowed in tablename
                    

                    tablename=self.get_tablename()


                    def getdatabasedata():
                        '''
                        These are all the column names: coursename, coursecode, coursehours, classification

                        To keep in mind, there are actually no blank rows in any database file. 
                        '''
                        
                        with sqlite3.connect(databasepath) as conn:
                            cursor=conn.cursor()

                            getalldata=f'''

                            SELECT *
                            FROM {tablename} 
                            WHERE coursename IS NOT NULL AND coursename != ''
                            '''


                            cursor.execute(getalldata)
                            rows = cursor.fetchall()                        
                            
                            return rows
                        
                    rows=getdatabasedata()
                    newrows=[]
                    for row in rows:
                        rowlist=list(row)
                        rowlist.append(displaydepartmentname)

                        newrows.append(rowlist)

                    with open(universitywidecsvpath,'a') as universitywidecsv:
                        writer=csv.writer(universitywidecsv)
                        writer.writerows(newrows)

            # now add the closing row
            with open(universitywidecsvpath,'a') as universitywidecsv:
                writer=csv.writer(universitywidecsv)
                writer.writerow([])

                writer.writerow(['DegreeView'])
        
        make_universidewide_csv()

        def make_universidewide_database():
            universitywidedatabase=os.path.join(self.universitywidefolder,'universitywidedatabase.db')

            if os.path.exists(universitywidedatabase):
                os.remove(universitywidedatabase)

            universitytablename=f'universitywidedata_table'
            def maketable():
                '''This creates the table for course data in the db'''

                # this line makes the db
                with sqlite3.connect(universitywidedatabase) as conn:
                    cursor=conn.cursor()

                # table name lowercase- since we changed from notes to category we also changed UpperDivStatus-UpperLowerStatus
                    createtablecommand=f'''CREATE TABLE IF NOT EXISTS "{universitytablename}" (coursename TEXT , coursecode TEXT, coursehours TEXT, classification TEXT, departmentname TEXT);'''
                    cursor.execute(createtablecommand)
                    conn.commit()
            maketable()



            for startingletter in self.alphabetizeddict:
                
                letterfolder=os.path.join(self.asset_folder_path,startingletter)
                if not os.path.exists(letterfolder):
                    os.mkdir(letterfolder)
                
                letterdict=self.alphabetizeddict[startingletter]

                for departmentname in letterdict:
                    departmenturl=letterdict[departmentname]

                    # make the slashes underscores. This will normalize it. Then in the createwebsite.py, I've already coded ways to unnormalize it. 
                    (
                    departmentname,
                    departmentnamecleaned,
                    displaydepartmentname,
                    departmentnamehalf,
                    departmentcode,
                    ) = self.get_departmentnames(departmentname)   

                    departmentfolderpath=os.path.join(letterfolder,departmentname)

                    databasepath=os.path.join(departmentfolderpath,f'{departmentnamecleaned}-database.db')

                    # hyphens and commas not allowed in tablename
                    

                    tablename=self.get_tablename()


                    def getdatabasedata():
                        '''
                        These are all the column names: coursename, coursecode, coursehours, classification

                        To keep in mind, there are actually no blank rows in any database file. 
                        '''
                        
                        with sqlite3.connect(databasepath) as conn:
                            cursor=conn.cursor()

                            getalldata=f'''

                            SELECT *
                            FROM {tablename} 
                            WHERE coursename IS NOT NULL AND coursename != ''
                            '''


                            cursor.execute(getalldata)
                            rows = cursor.fetchall()                        
                            
                            return rows
                        
                    rows=getdatabasedata()

                    with sqlite3.connect(universitywidedatabase) as conn:
                        cursor=conn.cursor()

                        
                        for row in rows:
                            coursename,coursecode,coursehours,classification=row
                            cursor.execute(f'INSERT INTO {universitytablename} (coursename, coursecode, coursehours, classification, departmentname) values(?,?,?,?,?);',
                                        [coursename,coursecode,coursehours,classification,displaydepartmentname])
                                    

                        conn.commit()
                                
                        # commit to the database 
                      
        make_universidewide_database()

        def makeuniversitywidehtmltable():
            universitywidedatabase=os.path.join(self.universitywidefolder,'universitywidedatabase.db')
            universitytablename=f'universitywidedata_table'


            def getdatabasedata():
                '''
                These are all the column names: coursename, coursecode, coursehours, classification
                So instead of opening each individual database...

                I just open the big universitywide one rn
                '''
                with sqlite3.connect(universitywidedatabase) as conn:
                    cursor=conn.cursor()

                    getalldata=f'''

                    SELECT *
                    FROM "{universitytablename}" 
                    WHERE coursename IS NOT NULL AND coursename != ''
                    '''


                    cursor.execute(getalldata)
                    rows = cursor.fetchall()                        
                    
                    return rows


            def univeristytablefilemaking():
                
        

                universitywidehtmltable=os.path.join(self.universitywidefolder,'universitywidetable.html')

                rows=getdatabasedata()

                
                htmlrows=f'''

                '''
                for row in rows:
                    coursename=f'<td>{row[0]}</td>'
                    coursecode=f'<td>{row[1]}</td>'
                    coursehours=f'<td>{row[2]}</td>'
                    classification=f'<td>{row[3]}</td>'
                    departmentname=f'<td>{row[4]}</td>'
                    
                    tr=f'''
                    <tr>
                    {coursename}
                    {coursecode}
                    {coursehours}
                    {classification}
                    {departmentname}
                    </tr>
                    '''
                    htmlrows+=tr
                htmlrows+=f'''
                    <tr>
                    <td>DegreeView</td>
                    <td></td>
                    <td></td>
                    <td></td>
                    </tr>
                    '''

                htmlcode=f'''
                <table id="departmentcoursestable">
                    <tr>
                    <td colspan="2">Courses</td>
                    
                    <td colspan="3" >{self.universityname}</td>
                    </tr>
                    <tr>
                    <td>Course Name</td>
                    <td>Course Code</td>
                    <td>Course Hours</td>
                    <td>Classification</td>
                    <td>Department Name</td>

                    </tr>
                    {htmlrows}
                </table>
                '''



                with open(universitywidehtmltable,'w') as htmlfile:
                    htmlfile.write(htmlcode)
                print(f'Made {universitywidehtmltable}')

            univeristytablefilemaking()

        makeuniversitywidehtmltable()

        def make_departmentcomparison_database():
            '''
            This should be a database ( and eventual CSV) that has each department, the longest course in it, the shortest course in it, and the count.
            This is easy because I already have all of this data in JSON file for each one. 
            I just need to put it in a database and csv now. 
            '''
            pass
    

    def get_sorted_departmentlist(self):
        '''
        This one is tricky, but I want an ordered list of the name of the department and how many courses each department has

        I'll then pass in the biggest and smallest department to be in the unversitystatsjson

        But the full list should be in its own file, like a json or csv.

        This file is gonna need me to open and query all departments databases, so it should probably be its own method
        '''

        departmentsize_dict={}
        for startingletter in self.alphabetizeddict:


            letterfolder=os.path.join(self.asset_folder_path,startingletter)
            if not os.path.exists(letterfolder):
                os.mkdir(letterfolder)
            
            letterdict=self.alphabetizeddict[startingletter]

            for departmentname in letterdict:
                # make the slashes underscores. This will normalize it. Then in the createwebsite.py, I've already coded ways to unnormalize it. 
                departmentname=departmentname.replace('/','_')


                departmentfolderpath=os.path.join(letterfolder,departmentname)

                    
                departmentnamecleaned=departmentname.replace(' ','').lower()


                databasepath=os.path.join(departmentfolderpath,f'{departmentnamecleaned}-database.db')

                # hyphens and commas not allowed in tablename
                # this should hopefully work across schools
                tabledepartmentname=departmentnamecleaned.replace('-','_').replace(',','_').replace('&','and').replace("'","")

                tablename=f'{tabledepartmentname}_table'


               
                with sqlite3.connect(databasepath) as conn:
                        cursor=conn.cursor()

                def get_department_coursecount():
                    countcoursescommand=f'''

                    SELECT coursename 
                    FROM {tablename} 
                    WHERE coursename IS NOT NULL AND coursename != ''
                    '''


                    cursor.execute(countcoursescommand)
                    courselist = cursor.fetchall()
                    courselist=[row[0] for row in courselist] 

                    return len(courselist)
                coursecount = get_department_coursecount()
                departmentsize_dict[departmentname]=coursecount
        
        # sort them with biggest first (descending)
        sorted_departments = dict(sorted(departmentsize_dict.items(), key=lambda x: x[1],reverse=True))
        # make the json path in the university wide folder
        
        # create a json
        with open( self.sorted_departments_json,'w') as sdjson:
            json.dump(sorted_departments,sdjson,indent=4)


    def make_university_statsjson(self):
        '''
        This is the big function containing getting the data and making the file

        The function that actually MAKES the json is makestatsjson()
        '''


        universitywidedatabase='enterpathlater'


        def getunidata():
            '''
            These are all the column names: coursename, coursecode, coursehours, classification

            It is case insensitive wow.

            This used to be named getdatabasedata() but I changed it to getunidata because we are doing some non database stuff
            '''

            # this function gets the number of departments per school
            def get_departmentcount():
                '''
                This uses the already created jsondata, under self.jsondatapath, which has the number of departments
                '''

                with open(self.jsondatapath) as unijson:
                    unidict=json.load(unijson)
                    departmentcount=len(unidict)
                return departmentcount
            
            def get_biggest_and_smallest_departments():

                with open(self.sorted_departments_json,'r') as sdjson:
                    sorted_departments=json.load(sdjson)
                
                # this makes a list of key value pairs as tuples
                # this is a good idea when you need to index into a dictionary, like below
                sorted_departments_list = list(sorted_departments.items())
                print(f'sorted_departments_list :\n{sorted_departments_list}')
                

                first_dept=sorted_departments_list[0]
                second_dept=sorted_departments_list[1]
                third_dept=sorted_departments_list[2]

                last_dept = sorted_departments_list[-1]
                second_last_dept = sorted_departments_list[-2]
                third_last_dept = sorted_departments_list[-3]

                # return them all

                # this is put together with "universitystatsdict" in getunidata

                # so the values here are tuples which become lists/ arrays in json
                biggest_and_smallest_departments = { 
                "first_dept": first_dept,
                "second_dept": second_dept,
                "third_dept": third_dept,
                "third_last_dept": third_last_dept,
                "second_last_dept": second_last_dept,
                "last_dept": last_dept,
                }
                return biggest_and_smallest_departments


            universitywidedatabase=os.path.join(self.universitywidefolder,'universitywidedatabase.db')

            universitytablename=f'universitywidedata_table'
            with sqlite3.connect(universitywidedatabase) as conn:
                cursor=conn.cursor()
                def get_course_count():

                    countquery=f'''

                    SELECT COUNT(coursename) 
                    FROM {universitytablename} 
                    WHERE coursename IS NOT NULL AND coursename != ''
                    '''


                    cursor.execute(countquery)
                    rowcount = cursor.fetchone()[0]                    
                    return rowcount
                def get_longest_andshortest_coursename():

                    longestnamecommand=f'''
                    SELECT * 
                    FROM {universitytablename} 
                    WHERE coursename IS NOT NULL AND coursename != ''
                    ORDER BY LENGTH(Coursename) DESC 
                    LIMIT 1;'''

                    cursor.execute(longestnamecommand)
                    row=cursor.fetchone()
                    longestcoursename=row[0]
                    longestcoursecode=row[1]
                    ldepartment=row[4]
                    longestlength=len(longestcoursename)


                    shortestnamecommand=f'''
                    SELECT * 
                    FROM {universitytablename} 
                    WHERE coursename IS NOT NULL AND Coursename != ''
                    ORDER BY LENGTH(Coursename) ASC 
                    LIMIT 2;
                    '''

                    cursor.execute(shortestnamecommand)
                    # for UT the real shortest coursename is
                    row=cursor.fetchall()[-1]
                    shortestcoursename=row[0]
                    shortestcoursecode=row[1]
                    sdepartment=row[4]

                    shortestlength=len(shortestcoursename)

                    results = {
                    "longestcoursename": longestcoursename,
                    "longestcoursecode": longestcoursecode,
                    "ldepartment": ldepartment,
                    "longestlength": longestlength,
                    "shortestcoursename": shortestcoursename,
                    "shortestcoursecode": shortestcoursecode,
                    "sdepartment": sdepartment,
                    "shortestlength": shortestlength
                }
                    return results


            departmentcount=get_departmentcount()
            # use get_ordered_deparmentlist to get the biggest and smallest departments and return them
            # then load it here into the univeristy statsdict
            coursecount=get_course_count()

            biggest_and_smallest_departments=get_biggest_and_smallest_departments()
            # this dict has the QUERIES
            resultsdict=get_longest_andshortest_coursename()



            universitystatsdict={
                "departmentcount":departmentcount,
                "coursecount":coursecount,
                
            }
            # merge
            universitystatsdict.update(resultsdict)
            universitystatsdict.update(biggest_and_smallest_departments)
            
            return universitystatsdict

        def makestatsjson():
            '''
            
            In this stats json, I'm going to put alot of unique stats, such as how long it would take to take all classes over the course of how many semesters.


            '''
            universityjson=os.path.join(self.universitywidefolder,'universitystatsjson.json')

            universitystatsdict=getunidata()
            print(f'universitystatsdict: {universitystatsdict}')


            with open(universityjson,'w') as statsfile:
                json.dump(universitystatsdict,statsfile,indent=4)
        
        makestatsjson()







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
    catalogobj.make_excel_files()
    
    


if __name__=="__main__":
    main()