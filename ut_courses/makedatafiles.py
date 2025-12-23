import requests
import bs4
from bs4 import BeautifulSoup

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







# good to check everythings working with the venv:
if __name__=='__main__':
    print(f'the version of beautiful soup is\n {(bs4.__version__)}')
    print(f'the version of requests is\n {(requests.__version__)}')
    print(f'\nthe python version being used is:{sys.executable}\n')

from scrapecoursedata import scrapeutcourses

class catalogData:
    def __init__(self):
        self.jsondatapath='/Users/shalevwiden/Downloads/Coding_Files/Python/BeautifulSoup_Library/degreeview_expansion/ut_courses/utjson.json'
        self.assetspath='/Users/shalevwiden/Downloads/Projects/dvassets/texas/UT_courses'
        self.universityname='The University of Texas at Austin'
        

            
        

        with open('excelconfiglink.txt','r') as configlink:
            self.excelconfigpath=configlink.read()


# Absolute path

        # Create spec from file
        from pathlib import Path


        # Now you can access functions from that file
       
        self.make_excelfile = make_excelfile
        # self.make_checkerboard=module.make_excelfile()



        with open(self.jsondatapath,'r') as universityjson:

            self.jsondata=json.load(universityjson)
        
        self.alphabetizeddict={}
        # this is a function to divide up the departments alphabetically
        for departmentname in self.jsondata:
            departmenturl=self.jsondata[departmentname]
            startingletter=departmentname[0]


            if startingletter not in self.alphabetizeddict:

                self.alphabetizeddict[startingletter]={}
                self.alphabetizeddict[startingletter][departmentname]=departmenturl
            else:
                self.alphabetizeddict[startingletter][departmentname]=departmenturl

        
    def get_departmentnamecleaned(self,departmentname):
        '''
        Docstring for get_departmentnamecleaned:
        This is a helper function for create_departmentname_json()
        
        :param self: Description
        :param departmentname: departmentname
        '''
        

        departmentnamecleaned=departmentname.replace('/','_')
        departmentnamecleaned=departmentname.replace(' ','').lower()
        departmentnamecleaned=departmentnamecleaned.replace('/','-')
        return departmentnamecleaned
    
    def create_departmentname_json(self):
        '''
        This will create departmentnamejson for every department which will include 4 things.
        It works well as JSON because I can get a visual on it 24/7

        departmentnamecleaned
        displaydepartmentname
        departmentnamehalf
        departmentcode

        This is tricky because all the other functions need to know how to get to this one, which means I think they all do need the minimum
        departmentnamecleaned code.

        This can serve as a function in the createuniversity class init and in this classes init
        '''

        for startingletter in self.alphabetizeddict:

            letterfolder=os.path.join(self.assetspath,startingletter)
            if not os.path.exists(letterfolder):
                os.mkdir(letterfolder)
            
            letterdict=self.alphabetizeddict[startingletter]

            for departmentname in letterdict:
                

                # make the slashes underscores. This will normalize it. Then in the createwebsite.py, I've already coded ways to unnormalize it. 


                departmentnamecleaned=self.get_departmentnamecleaned(departmentname)
                print(f'Departmentname cleaned is {departmentnamecleaned}')

                # use departmentname for the asset folder, not departmentname cleaned
                # use this line no matter where actually just to get rid of slashes, thats a necesity
                departmentname=departmentname.replace('/','_')

                departmentfolderpath=os.path.join(letterfolder,departmentname)


                departmentnamestats={
                    "departmentnamecleaned":"",
                    "displaydepartmentname":"",
                    "departmentnamehalf":"",
                    "departmentcode":"",


                }

                departmentnamejson=f'departmentnamejson.json'

                departmentnamejsonpath=os.path.join(departmentfolderpath,departmentnamejson)
                with open(departmentnamejsonpath,'w') as departmentnamejsonobj:
                        json.dump(departmentnamestats,departmentnamejsonobj,indent=4)

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

            letterfolder=os.path.join(self.assetspath,startingletter)
            if not os.path.exists(letterfolder):
                os.mkdir(letterfolder)
            
            letterdict=self.alphabetizeddict[startingletter]
            for departmentname in letterdict:
                departmenturl=letterdict[departmentname]

                departmentname=departmentname.replace('/','_')

                departmentfolderpath=os.path.join(letterfolder,departmentname)


                if not os.path.exists(departmentfolderpath):
                    os.mkdir(departmentfolderpath)

            
            
                departmentnamecleaned=departmentname.replace(' ','').lower()
                departmentnamecleaned=departmentnamecleaned.replace('/','-')



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
                    tabledepartmentname=departmentnamecleaned.replace('-','_').replace(',','_').replace('&','and').replace("'","")

                    tablename=f'{tabledepartmentname}_table'
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
                        departmentdata=scrapeutcourses(departmenturl=departmenturl)
                        for coursename in departmentdata:
                            coursecode,coursehours,classification=departmentdata[coursename]
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


            letterfolder=os.path.join(self.assetspath,startingletter)
            if not os.path.exists(letterfolder):
                os.mkdir(letterfolder)
            
            letterdict=self.alphabetizeddict[startingletter]

            for departmentname in letterdict:
                departmenturl=letterdict[departmentname]

                # make the slashes underscores. This will normalize it. Then in the createwebsite.py, I've already coded ways to unnormalize it. 
                departmentname=departmentname.replace('/','_')


                departmentfolderpath=os.path.join(letterfolder,departmentname)

                    
                departmentnamecleaned=departmentname.replace(' ','').lower()


                databasepath=os.path.join(departmentfolderpath,f'{departmentnamecleaned}-database.db')

                # hyphens and commas not allowed in tablename
                tabledepartmentname=departmentnamecleaned.replace('-','_').replace(',','_').replace('&','and').replace("'","")

                tablename=f'{tabledepartmentname}_table'


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
                    departmentnamecleaned=departmentnamecleaned.replace(',','-')


                    statsjsonpath=os.path.join(departmentfolderpath,f'{departmentnamecleaned}-statsjson.json')

                    statsdict=getdatabasestats()



                    with open(statsjsonpath,'w') as statsfile:
                        json.dump(statsdict,statsfile,indent=4)

                jsonfilemaking(departmentnamecleaned=departmentnamecleaned)   
               
    def makehtmltable(self):
        for startingletter in self.alphabetizeddict:

            letterfolder=os.path.join(self.assetspath,startingletter)
            if not os.path.exists(letterfolder):
                os.mkdir(letterfolder)
            
            letterdict=self.alphabetizeddict[startingletter]

            for departmentname in letterdict:
                departmenturl=letterdict[departmentname]

                # make the slashes underscores. This will normalize it. Then in the createwebsite.py, I've already coded ways to unnormalize it. 
                departmentname=departmentname.replace('/','_')


                departmentfolderpath=os.path.join(letterfolder,departmentname)

                    
                departmentnamecleaned=departmentname.replace(' ','').lower()


                databasepath=os.path.join(departmentfolderpath,f'{departmentnamecleaned}-database.db')

                # hyphens and commas not allowed in tablename
                tabledepartmentname=departmentnamecleaned.replace('-','_').replace(',','_').replace('&','and').replace("'","")

                tablename=f'{tabledepartmentname}_table'


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
                        
                        return rows


                def tablefilemaking(departmentname,departmentnamecleaned):
                    departmentnamecleaned=departmentnamecleaned.replace(',','-')


                    displaydepartmentname=departmentname.replace('_','/')
                    displaydepartmentname=departmentname.strip().split('-')
                    code=displaydepartmentname[0].strip()
                    departmentnamehalf=displaydepartmentname[-1].strip()
                    displaydepartmentname=f'({code}) - {departmentnamehalf}'

                    htmltablefile=os.path.join(departmentfolderpath,f'{departmentnamecleaned}-htmltable.html')

                    rows=getdatabasedata()

                    
                    htmlrows=f'''

                    '''
                    for row in rows:
                        coursename=f'<td>{row[0]}</td>'
                        coursecode=f'<td>{row[1]}</td>'
                        coursehours=f'<td>{row[2]}</td>'
                        classification=f'<td>{row[3]}</td>'
                        
                        tr=f'''
                        <tr>
                       {coursename}
                       {coursecode}
                       {coursehours}
                       {classification}
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
                        <td colspan="2">{departmentnamehalf}</td>
                       
                        <td colspan="2" >{self.universityname}</td>
                        </tr>
                        <tr>
                        <td>Course Name</td>
                        <td>Course Code</td>
                        <td>Course Hours</td>
                        <td>Classification</td>
                        </tr>
                        {htmlrows}
                    </table>
                    '''



                    with open(htmltablefile,'w') as htmlfile:
                        htmlfile.write(htmlcode)
                    print(f'Made {htmltablefile}')

                tablefilemaking(departmentname=departmentname,departmentnamecleaned=departmentnamecleaned)   

    def createcsvs(self):
        
        for startingletter in self.alphabetizeddict:

            '''
            '''

            letterfolder=os.path.join(self.assetspath,startingletter)
            if not os.path.exists(letterfolder):
                os.mkdir(letterfolder)
            
            letterdict=self.alphabetizeddict[startingletter]
            for departmentname in letterdict:
                departmenturl=letterdict[departmentname]

                departmentname=departmentname.replace('/','_')
                departmentfolderpath=os.path.join(letterfolder,departmentname)

                if not os.path.exists(departmentfolderpath):
                    os.mkdir(departmentfolderpath)

            
            
                departmentnamecleaned=departmentname.replace(' ','').lower()
                

        
            # use the fact that its an underscore to readd it later in the website creation file
            


                departmentcourses_csv=os.path.join(departmentfolderpath,f'{departmentnamecleaned}-coursescsv.csv')

                with open(departmentcourses_csv,'w') as departmentcourses_csv:

                    departmentdict=scrapeutcourses(departmenturl=departmenturl)

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
            
            letterfolder=os.path.join(self.assetspath,startingletter)
            if not os.path.exists(letterfolder):
                os.mkdir(letterfolder)
            
            letterdict=self.alphabetizeddict[startingletter]
            for departmentname in letterdict:
                departmenturl=letterdict[departmentname]

                departmentname=departmentname.replace('/','_')

                def make_required_folders():
                    departmentfolderpath=os.path.join(letterfolder,departmentname)

                    excelfolderpath=os.path.join(departmentfolderpath,'excelthemes')

                    if not os.path.exists(departmentfolderpath):
                        os.mkdir(departmentfolderpath)


                    if not os.path.exists(excelfolderpath):
                        os.mkdir(excelfolderpath)

                    return departmentfolderpath, excelfolderpath

                departmentfolderpath, excelfolderpath=make_required_folders()
            
            
                departmentnamecleaned=departmentname.replace(' ','').lower()
                departmentnamecleaned=departmentnamecleaned.replace('/','-')
                

        
            # use the fact that its an underscore to readd it later in the website creation file
            



                
                    
                departmentnamecleaned=departmentname.replace(' ','').lower()


                databasepath=os.path.join(departmentfolderpath,f'{departmentnamecleaned}-database.db')

                # hyphens and commas not allowed in tablename
                tabledepartmentname=departmentnamecleaned.replace('-','_').replace(',','_').replace('&','and').replace("'","")

                tablename=f'{tabledepartmentname}_table'


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

                def makegreentheme():
                    
                    configjsonpath='/Users/shalevwiden/Downloads/Projects/dvwebsitecreation/sourcefiles/Excelfile_configs/testconfigs/green.json'
                    savepath=os.path.join(excelfolderpath,f'{departmentnamecleaned}-coursesgreentheme.xlsx')
                    with open(configjsonpath,'r') as configjson:
                        configjson=json.load(configjson)
                    config={
                    "departmentname":departmentname,
                    "universityname":self.universityname,
                    "savepath":savepath,
                    "rows":rows,
                    }
                    config.update(configjson)
                    
                    self.make_excelfile(**config)

                # makegreentheme()
                def makeoriginaltheme():
                    configjsonpath='/Users/shalevwiden/Downloads/Projects/dvwebsitecreation/sourcefiles/Excelfile_configs/originalconfig.json'
                    savepath=os.path.join(excelfolderpath,f'{departmentnamecleaned}-courses-originaltheme.xlsx')
                    with open(configjsonpath,'r') as configjson:
                        configjson=json.load(configjson)
                    config={
                    "departmentname":departmentname,
                    "universityname":self.universityname,
                    "savepath":savepath,
                    "rows":rows,
                    }
                    config.update(configjson)
                    
                    self.make_excelfile(**config)

                # makeoriginaltheme()

                def makedarktheme():
                    configjsonpath='/Users/shalevwiden/Downloads/Projects/dvwebsitecreation/sourcefiles/Excelfile_configs/darkthemeconfig.json'
                    savepath=os.path.join(excelfolderpath,f'{departmentnamecleaned}-courses-darktheme.xlsx')
                    with open(configjsonpath,'r') as configjson:
                        configjson=json.load(configjson)
                    config={
                    "departmentname":departmentname,
                    "universityname":self.universityname,
                    "savepath":savepath,
                    "rows":rows,
                    }
                    config.update(configjson)
                    
                    self.make_excelfile(**config)

                # makedarktheme()

                def makeneon():
                    configjsonpath= '/Users/shalevwiden/Downloads/Projects/dvwebsitecreation/sourcefiles/Excelfile_configs/testconfigs/rainbow.json'
                    savepath=os.path.join(excelfolderpath,f'{departmentnamecleaned}-neontheme.xlsx')
                    with open(configjsonpath,'r') as configjson:
                        configjson=json.load(configjson)
                    config={
                    "departmentname":departmentname,
                    "universityname":self.universityname,
                    "savepath":savepath,
                    "rows":rows,
                    }
                    config.update(configjson)
                    
                    self.make_excelfile(**config)

                # makeneon() 

                def makedesert():
                    configjsonpath=  '/Users/shalevwiden/Downloads/Projects/dvwebsitecreation/sourcefiles/Excelfile_configs/newconfigs/desertnew.json'
                    savepath=os.path.join(excelfolderpath,f'{departmentnamecleaned}-deserttheme.xlsx')
                    with open(configjsonpath,'r') as configjson:
                        configjson=json.load(configjson)
                    config={
                    "departmentname":departmentname,
                    "universityname":self.universityname,
                    "savepath":savepath,
                    "rows":rows,
                    }
                    config.update(configjson)
                    
                    self.make_excelfile(**config)

                # makedesert()
                def makeocean():
                    configjsonpath='/Users/shalevwiden/Downloads/Projects/dvwebsitecreation/sourcefiles/Excelfile_configs/newconfigs/oceantheme.json'
                    savepath=os.path.join(excelfolderpath,f'{departmentnamecleaned}-oceantheme.xlsx')
                    with open(configjsonpath,'r') as configjson:
                        configjson=json.load(configjson)
                    config={
                    "departmentname":departmentname,
                    "universityname":self.universityname,
                    "savepath":savepath,
                    "rows":rows,
                    }
                    config.update(configjson)
                    
                    self.make_excelfile(**config)
                   

                # makeocean()

                def makeprimary():
                    configjsonpath= '/Users/shalevwiden/Downloads/Projects/dvwebsitecreation/sourcefiles/Excelfile_configs/newconfigs/primarycolors.json'
                    savepath=os.path.join(excelfolderpath,f'{departmentnamecleaned}-primarycolorstheme.xlsx')
                    with open(configjsonpath,'r') as configjson:
                        configjson=json.load(configjson)
                    config={
                    "departmentname":departmentname,
                    "universityname":self.universityname,
                    "savepath":savepath,
                    "rows":rows,
                    }
                    config.update(configjson)
                    
                    self.make_excelfile(**config)
                # makeprimary()

                def makegreyscale():
                    configjsonpath= '/Users/shalevwiden/Downloads/Projects/dvwebsitecreation/sourcefiles/Excelfile_configs/newconfigs/greyscale.json'
                    savepath=os.path.join(excelfolderpath,f'{departmentnamecleaned}-greyscaletheme.xlsx')
                    with open(configjsonpath,'r') as configjson:
                        configjson=json.load(configjson)
                    config={
                    "departmentname":departmentname,
                    "universityname":self.universityname,
                    "savepath":savepath,
                    "rows":rows,
                    }
                    config.update(configjson)
                    
                    self.make_excelfile(**config)

                # makegreyscale()

                def makeblack():
                    configjsonpath= '/Users/shalevwiden/Downloads/Projects/dvwebsitecreation/sourcefiles/Excelfile_configs/newconfigs/blacktheme.json'
                    savepath=os.path.join(excelfolderpath,f'{departmentnamecleaned}-blacktheme.xlsx')
                    with open(configjsonpath,'r') as configjson:
                        configjson=json.load(configjson)
                    config={
                    "departmentname":departmentname,
                    "universityname":self.universityname,
                    "savepath":savepath,
                    "rows":rows,
                    }
                    config.update(configjson)
                    
                    self.make_excelfile(**config)
                    
                # makeblack()

                def makepasteltheme():
                    configjsonpath='/Users/shalevwiden/Downloads/Projects/dvwebsitecreation/sourcefiles/Excelfile_configs/newconfigs/pastelconfig.json'
                    savepath=os.path.join(excelfolderpath,f'{departmentnamecleaned}-pasteltheme.xlsx')
                    with open(configjsonpath,'r') as configjson:
                        configjson=json.load(configjson)
                    config={
                    "departmentname":departmentname,
                    "universityname":self.universityname,
                    "savepath":savepath,
                    "rows":rows,
                    }
                    config.update(configjson)
                    
                    self.make_excelfile(**config)
                
                def testingexcel():
                    configjsonpath='/Users/shalevwiden/Downloads/Projects/dvwebsitecreation/sourcefiles/Excelfile_configs/newconfigs/pastelconfig.json'
                    savepath=os.path.join(excelfolderpath,f'{departmentnamecleaned}-testing.xlsx')
                    with open(configjsonpath,'r') as configjson:
                        configjson=json.load(configjson)
                    config={
                    "departmentname":departmentname,
                    "universityname":self.universityname,
                    "savepath":savepath,
                    "rows":rows,
                    }
                    config.update(configjson)
                    
                    self.make_excelfile(**config)

                # testingexcel()

                def checkerboardtheme():
                    configjsonpath='/Users/shalevwiden/Downloads/Projects/dvwebsitecreation/sourcefiles/Excelfile_configs/checkerboardconfigs/brownconfig.json'
                    savepath=os.path.join(excelfolderpath,f'{departmentnamecleaned}-checkerboard.xlsx')
                    with open(configjsonpath,'r') as configjson:
                        configjson=json.load(configjson)
                    config={
                    "departmentname":departmentname,
                    "universityname":self.universityname,
                    "savepath":savepath,
                    "rows":rows,
                    }
                    config.update(configjson)
                    
                    make_checkerboardfile(**config)

                # checkerboardtheme()


                def makeredtheme():
                    configjsonpath='/Users/shalevwiden/Downloads/Projects/dvwebsitecreation/sourcefiles/Excelfile_configs/colorconfigs/redtheme.json'
                    savepath=os.path.join(excelfolderpath,f'{departmentnamecleaned}-redtheme.xlsx')
                    with open(configjsonpath,'r') as configjson:
                        configjson=json.load(configjson)
                    config={
                    "departmentname":departmentname,
                    "universityname":self.universityname,
                    "savepath":savepath,
                    "rows":rows,
                    }
                    config.update(configjson)
                    
                    self.make_excelfile(**config)

                makeredtheme()



                def makebluetheme():
                    configjsonpath='/Users/shalevwiden/Downloads/Projects/dvwebsitecreation/sourcefiles/Excelfile_configs/colorconfigs/bluetheme.json'
                    savepath=os.path.join(excelfolderpath,f'{departmentnamecleaned}-bluetheme.xlsx')
                    with open(configjsonpath,'r') as configjson:
                        configjson=json.load(configjson)
                    config={
                    "departmentname":departmentname,
                    "universityname":self.universityname,
                    "savepath":savepath,
                    "rows":rows,
                    }
                    config.update(configjson)
                    
                    self.make_excelfile(**config)

                makebluetheme()

    def create_univeristy_files(self):
        '''what this function will do is initialize the University Wide files.
        This includes the University Wide Database, and some csv files I'm thinking
        '''

        universitystatsfolder=os.path.join(self.assetspath,"universitywidefolder")

        if not os.path.exists(universitystatsfolder):
            os.mkdir(universitystatsfolder)

    # this will rewrite it everytime I start the file. Clearing it

        def make_universidewide_csv():
            universitywidecsvpath=os.path.join(universitystatsfolder,'universitywidecsv.csv')

            with open(universitywidecsvpath,'w') as universitywidecsv:
                writer=csv.writer(universitywidecsv)
                writer.writerow(['Courses','',"","",'The University of Texas at Austin'])


                writer.writerow(['Coursename','Coursecode','Coursehours','Classification',"Department Name"])
                writer.writerow([])


            for startingletter in self.alphabetizeddict:

                
                

                    
                

                letterfolder=os.path.join(self.assetspath,startingletter)
                if not os.path.exists(letterfolder):
                    os.mkdir(letterfolder)
                
                letterdict=self.alphabetizeddict[startingletter]

                for departmentname in letterdict:
                    departmenturl=letterdict[departmentname]

                    # make the slashes underscores. This will normalize it. Then in the createwebsite.py, I've already coded ways to unnormalize it. 
                    departmentname=departmentname.replace('/','_')


                    departmentfolderpath=os.path.join(letterfolder,departmentname)

                        
                    departmentnamecleaned=departmentname.replace(' ','').lower()

                    displaydepartmentname=departmentname.replace('_','/')
                    displaydepartmentname=departmentname.strip().split('-')
                    code=displaydepartmentname[0].strip()
                    departmentnamehalf=displaydepartmentname[-1].strip()
                    displaydepartmentname=f'({code}) - {departmentnamehalf}'


                    databasepath=os.path.join(departmentfolderpath,f'{departmentnamecleaned}-database.db')

                    # hyphens and commas not allowed in tablename
                    tabledepartmentname=departmentnamecleaned.replace('-','_').replace(',','_').replace('&','and').replace("'","")

                    tablename=f'{tabledepartmentname}_table'


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
            universitywidedatabase=os.path.join(universitystatsfolder,'universitywidedatabase.db')

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
                
                letterfolder=os.path.join(self.assetspath,startingletter)
                if not os.path.exists(letterfolder):
                    os.mkdir(letterfolder)
                
                letterdict=self.alphabetizeddict[startingletter]

                for departmentname in letterdict:
                    departmenturl=letterdict[departmentname]

                    # make the slashes underscores. This will normalize it. Then in the createwebsite.py, I've already coded ways to unnormalize it. 
                    departmentname=departmentname.replace('/','_')


                    departmentfolderpath=os.path.join(letterfolder,departmentname)

                        
                    departmentnamecleaned=departmentname.replace(' ','').lower()


                    displaydepartmentname=departmentname.replace('_','/')
                    displaydepartmentname=departmentname.strip().split('-')
                    code=displaydepartmentname[0].strip()
                    departmentnamehalf=displaydepartmentname[-1].strip()
                    displaydepartmentname=f'({code}) - {departmentnamehalf}'


                    databasepath=os.path.join(departmentfolderpath,f'{departmentnamecleaned}-database.db')

                    # hyphens and commas not allowed in tablename
                    tabledepartmentname=departmentnamecleaned.replace('-','_').replace(',','_').replace('&','and').replace("'","")

                    tablename=f'{tabledepartmentname}_table'


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
            universitywidedatabase=os.path.join(universitystatsfolder,'universitywidedatabase.db')
            universitytablename=f'universitywidedata_table'


            def getdatabasedata():
                '''
                These are all the column names: coursename, coursecode, coursehours, classification
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
                


            

                universitywidehtmltable=os.path.join(universitystatsfolder,'universitywidetable.html')

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



    def make_university_statsjson(self):


        universitywidedatabase='enterpathlater'

        universitystatsfolder=os.path.join(self.assetspath,"universitywidefolder")

        def getdatabasedata():
            '''
            These are all the column names: coursename, coursecode, coursehours, classification

            It is case insensitive wow.
            '''

            universitywidedatabase=os.path.join(universitystatsfolder,'universitywidedatabase.db')

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



            coursecount=get_course_count()
            resultsdict=get_longest_andshortest_coursename()

            universitystatsdict={
                "coursecount":coursecount,
                
            }

            # merge
            universitystatsdict.update(resultsdict)
            
            return universitystatsdict


        def makestatsjson():
            '''
            
            In this stats json, I'm going to put alot of unique stats, such as how long it would take to take all classes over the course of how many semesters.


            '''
            universityjson=os.path.join(universitystatsfolder,'universitystatsjson.json')

            universitystatsdict=getdatabasedata()
            print(universitystatsdict)


            with open(universityjson,'w') as statsfile:
                json.dump(universitystatsdict,statsfile,indent=4)
        
        makestatsjson()







'''
Now this is a class that is truly scalable and reproducable
'''
def runcatalogDataclass():
    catalogobj=catalogData()

    
    
    catalogobj.create_departmentname_json()
    # catalogobj.makestatsjson()    
    # catalogobj.make_excel_files()
    
    

runcatalogDataclass()
