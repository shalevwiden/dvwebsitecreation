from pathlib import Path
import os

import sys
if __name__=='__main__':
    print(f'\nthe python version being used is:{sys.executable}\n')

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


import subprocess
import random

import csv
import time
import json
import sqlite3

# use this to render template
from jinja2 import Environment, FileSystemLoader



# use this to upload stuff to google cloud
from google.cloud import storage


# use this to import stuff from other python files
import importlib.util

# you can also assign a function

# the asset is important here because it contains the name of every degree in it.


'''
Ok so this needs to be redesigned to take in a json file.

We might modify the JSON file in python using dictionary methods if needed.

I need to add 

'''
class createUniversity:
    def __init__(self,schoolfolder, universityname, cloudbucketpath,websitefolder,schoolabrv):
        
        '''
        
        website folder is where the website files like html will be created

        I should NOT include departments in it because in this class Im creating many university wide files
        These files will go on the root level of the website
        like 
        
        dv/texas/ut/stats.html
        '''

        
        # where assets like excel files and csvs are
        self.asset_folder_path=os.path.join(schoolfolder,'assets')

        # now based on that asset_folder_path get the university stats
        self.universitywidefolder=os.path.join(self.asset_folder_path,"universitywidefolder")


        if not os.path.exists(self.universitywidefolder):
            os.makedirs(self.universitywidefolder, exist_ok=True)

        # just keep the variable names the same as the filenames
        self.sorted_departments_json=os.path.join(self.universitywidefolder,"sorted_departments_json.json")
        self.universitystatsjson=os.path.join(self.universitywidefolder,"universitystatsjson.json")
        # I actually dont think Ill use this one
        self.universitywidedatabase=os.path.join(self.universitywidefolder,"universitywidedatabase.db")



        # this is the JSON for all of the department names and department links
        self.jsondatapath=os.path.join(schoolfolder,'unijson.json')
        with open(self.jsondatapath,'r') as universityjson:
            self.jsondata=json.load(universityjson)

        # random dept stuff

       

        # university name like 'The University of Texas at Austin'
        self.universityname=universityname
        #university abbreviation like UT - for some schools there is no abbreviation.
        # well maybe, Yale could be the abbreviation for Yale University
        self.schoolabrv = schoolabrv


        

        # path like 'https://storage.googleapis.com/utcourses'
        # the bucket should be the schoolabrv
        self.cloudbucketpath=cloudbucketpath

        self.schoolfolder = schoolfolder

        # I guess these are the only ones I really need from each school folder
        
        

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

        # this one is fixed 
        # this should work. If not I need to find a mystery

      


        # can I have spaces is the question
        
        # this one is important
        # is the location of the department folder for now
        self.websitefolder=websitefolder
        if not os.path.exists(self.websitefolder):
            os.makedirs(self.websitefolder, exist_ok=True)   

        # this is where all the department pages are kept
        self.deparmentsfolder=os.path.join(self.websitefolder,"departments")
        if not os.path.exists(self.deparmentsfolder):
            os.makedirs(self.deparmentsfolder, exist_ok=True)   
        
        # now lets define the names of the uni wide files
        # change their url behavior (somewhat easily here)
        lowered=self.schoolabrv.lower()

        self.sorted_departments_page=os.path.join(self.websitefolder,f"sorted-departments.html")
        self.statspage=os.path.join(self.websitefolder,f"{lowered}stats.html")
        self.homepage=os.path.join(self.websitefolder,f"{lowered}-home.html")
        self.randompagejspath=os.path.join(self.websitefolder,f"randompage.js")
        # this json contains a list of all departmentpage names to be able to do random page functionality
        self.departmentpagelinks=os.path.join(self.websitefolder,f"departmentpagelinks.json")

        env = Environment(loader=FileSystemLoader("templating/templates"))

        # define all the templates to be used
        self.lettertemplate = env.get_template("letterpage.html")
        self.departmentpagetemplate=env.get_template("department_templates/departmentpage.html")
        self.sorted_departments_template=env.get_template("sorted_departments_page.html")
        self.statspage_template=env.get_template("statspage_template.html")
        
        self.homepage_template=env.get_template("homepage.html")


        
        # this will include code specific to that school, which right now is only getting the departmentnamehalf and displaydepartmentname
        # self.helperfunctionsfolder=helperfunctionsfolder



        self.images={
            
            "linkicon":"https://storage.googleapis.com/degreeview/degreeviewimages/linkicon.svg",
            "logo5":"https://storage.googleapis.com/degreeview/degreeviewimages/logo5.png",

            "minilogo":"https://storage.googleapis.com/degreeview/degreeviewimages/minilogo.png",
            "site_favicon":"https://storage.googleapis.com/degreeview/degreeviewimages/site_favicon.png"
        }
        
        with open('/Users/shalevwiden/Downloads/Projects/dvwebsitecreation/sourcefiles/html_components/degreeviewfooter.html','r') as footerfile:
            self.footer=footerfile.read()
        with open('/Users/shalevwiden/Downloads/Projects/dvwebsitecreation/sourcefiles/html_components/headlinks.html','r') as headfile:
            # we we actually do use this
            self.headlinks=headfile.read()


        self.outputspath='/Users/shalevwiden/Downloads/Projects/dvwebsitecreation/templating/outputs'
        with open('/Users/shalevwiden/Downloads/Projects/dvwebsitecreation/sourcefiles/googleanalytics_tags/degreeviewtag/headtag.html','r') as headtag:
            self.headtag=headtag.read()
        with open('/Users/shalevwiden/Downloads/Projects/dvwebsitecreation/sourcefiles/googleanalytics_tags/degreeviewtag/bodytag.html','r') as bodytag:
            self.bodytag=bodytag.read()
        
        # call this
        self._init_stuff()

        # footer so I dont have to redefine it multiple times. 

    def _init_stuff(self):
        '''
        Just dividing this up more
        moved excelstuff to catalogdata class

        '''

        def schoolfolder_stuff():
            schoolfolder_module=self.schoolfolder.replace('/','.')
            self.scrape_module = importlib.import_module(
                f"{schoolfolder_module}.scrapecourses"
            )
            self.dept_module = importlib.import_module(
                f"{schoolfolder_module}.departmentname"
            )

            self.scrapecourses = self.scrape_module.scrapecourses
            self.DepartmentName = self.dept_module.DepartmentName
        schoolfolder_stuff()

    def get_tablename(self):
        '''
        This gets the tablename in the department databases
        '''
        tablename=f'coursestable'
        return tablename

    def get_departmentnames(self, departmentname):
        dept=self.DepartmentName()

        departmentname=dept.get_sanitized_departmentname(departmentname)

        departmentnamecleaned=dept.get_departmentnamecleaned(departmentname)
        displaydepartmentname=dept.get_display_departmentname(departmentname)
        departmentnamehalf=dept.get_departmentnamehalf(departmentname)
        departmentcode=dept.get_departmentcode(departmentname)

        return (
            departmentname,
            departmentnamecleaned,
            displaydepartmentname,
            departmentnamehalf,
            departmentcode,
        )


    def upload_schoolfiles(self):


        '''
        This simply gets all the school files and uploads them to cloud. 
        '''
         
        #  if you want to only upload one legree, just change it so its i range 1 to range 

        print(f'\n\nBeginning Cloud Upload for {startingletter} school specific files\n\n') 

        def get_school_assetlists():
            
            '''
            Important: these lists contain the paths to the files ON THE LOCAL MACHINE. Not in cloud or on the website. 
            '''
            csvlist=[]
            excellist=[]
            pdflist=[]
            mmdlist=[]
            # os.walk recursively travels everything
            for file in os.listdir(self.schoolfolderpath):
                
                    
                    # we neewd the fullpath in the list since thats the way it can be uploaded to google cloud.

                full_path = os.path.join(self.schoolfolderpath,file)

                if os.path.splitext(file)[1]=='.csv':
                    csvlist.append(full_path)
                    # removes those dollar sign excel files. 
                elif os.path.splitext(file)[1]=='.xlsx' and not file.startswith(("~$", "$")):
                    excellist.append(full_path)
                elif os.path.splitext(file)[1]=='.pdf':
                    pdflist.append(full_path)
                elif os.path.splitext(file)[1]=='.mmd':
                    mmdlist.append(full_path)

            # these lists have the full paths since they'll be used to upload stuff. 
            # currently for school all other lists will be empty
            return [csvlist,excellist,pdflist,mmdlist]


        def upload_to_googlecloud(source_file_name):

                # how to manually change credentials...


                # just change project name here to change where they go.
                # In code, for multiple schools. Dope.
                client = storage.Client(project='degreeview-ut')


                # this should return the email used for google cloud. Its a service email tho

                # yeah the project is the same as the bucket name. In the future change this, as the bucketname is what user sees
                bucket = client.bucket('degreeview-utd-plans')
                # bucket list


            #THis is what will be in the url and what the name of the object will be in google cloud storage

                cleaned_object_name=source_file_name.split('/')[-1]        


                # make it so each file has the type. 
                # define upload blob here
               
                if os.path.splitext(source_file_name)[1]=='.csv':
                    uploadblob =f'{self.cleanedschoolname}/csvs/{cleaned_object_name}'
                    uploadblob=bucket.blob(uploadblob)
                elif os.path.splitext(source_file_name)[1]=='.xlsx':
                    uploadblob =f'{self.cleanedschoolname}/excel-files/{cleaned_object_name}'
                    uploadblob=bucket.blob(uploadblob)


                elif os.path.splitext(source_file_name)[1]=='.pdf':
                    uploadblob =f'{self.cleanedschoolname}/pdfs/{cleaned_object_name}'
                    uploadblob=bucket.blob(uploadblob)

                elif os.path.splitext(source_file_name)[1]=='.mmd':
                    uploadblob =f'{self.cleanedschoolname}/mmds/{cleaned_object_name}'
                    uploadblob=bucket.blob(uploadblob)


                else:
                    uploadblob = cleaned_object_name
                    uploadblob=bucket.blob(uploadblob)


                # add a check to not do it many times
                dontavoidreplace=True
                if dontavoidreplace:

                    uploadblob.upload_from_filename(source_file_name)

                    uploadblob.make_public()  # Makes it publicly accessible
                    # can also use blob.make_private()
                else:
                    print(f'{uploadblob.name} already exits, didnt upload\n')


                # use this link on the website to serve the file.
                return uploadblob.public_url

        # this one right here uploads the school specific assets

        def loop_through_assets_to_upload():
            csvlist=get_school_assetlists()[0]
            for csvfile in csvlist:
                # comment these out depending on which ones I want
                upload_to_googlecloud(csvfile)
                print(f'Uploaded {csvfile} to cloud\n')
                # pass a tuple
        loop_through_assets_to_upload()

        print(f'\n\nEnding Cloud Upload for {startingletter} school specific files\n\n') 

        return 0  
    

                      
    def get_school_assetcloudpaths_lists(self):
        '''
        Reconstruct the asset names manually like this:

        https://storage.googleapis.com/[BUCKET_NAME]/[OBJECT_NAME]

        Unlike other functions, this is by degree not school.
        As such this will not contain any school specific csv or excel files. 
        Those have to be obtained with another function. 
        This function returns the links that will be added to the website. That way I can get the links without a class A operation

        '''
        csv_path_list=[]
        excel_path_list=[]
        pdf_path_list=[]
        mmd_path_list=[]
        # os.walk recursively travels everything
        for file in os.listdir(self.schoolfolderpath):
            
            # we neewd the fullpath in the list since thats the way it can be uploaded to google cloud.

            googlecloudpath=f'https://storage.googleapis.com/degreeview-ut/'

            if os.path.splitext(file)[1]=='.csv':
                objectname_incloud=f'{self.cleanedschoolname}/csvs/{file}'
                googlecloudpath=f'https://storage.googleapis.com/degreeview-ut/{objectname_incloud}'

                csv_path_list.append(googlecloudpath)
                # removes those dollar sign excel files. 
            elif os.path.splitext(file)[1]=='.xlsx' and not file.startswith(("~$", "$")):

                objectname_incloud=f'{self.cleanedschoolname}/excel-files/{file}'
                googlecloudpath=f'https://storage.googleapis.com/degreeview-ut/{objectname_incloud}'
            
                excel_path_list.append(googlecloudpath)
            elif os.path.splitext(file)[1]=='.pdf':
            
                objectname_incloud=f'{self.cleanedschoolname}/pdfs/{file}'
                googlecloudpath=f'https://storage.googleapis.com/degreeview-ut/{objectname_incloud}'
            
                pdf_path_list.append(googlecloudpath)
            elif os.path.splitext(file)[1]=='.mmd':
            
                objectname_incloud=f'{self.cleanedschoolname}/mmds/{file}'
                googlecloudpath=f'https://storage.googleapis.com/degreeview-ut/{objectname_incloud}'
                mmd_path_list.append(googlecloudpath)

        # currently only csv path is updated. 
        return [csv_path_list,excel_path_list,pdf_path_list,mmd_path_list]

    
    def createletterpages(self):
        '''
        On each school page include the school specific csv/.xlsx (listing all the degrees). Then also include another other school diagrams in the future.
        I need it to be modularized so I can do it school by school. As such, use the asset. 

        This actually does create letter pages.
        '''
        # this ensures other folders arent added
        
        for startingletter in self.alphabetizeddict:

            letterfolder=os.path.join(self.asset_folder_path,startingletter)
           
            
            
                # its already cleaned
        
        # --------------------------
            schoolinfo=f'Every degree page has 2 csvs, 2 excel files, and a sample semester diagram.\n\
            More files coming in the future.' 

            def make_departmentlist_ul():
                # keep this probs
                departmentlist_ul_element_content=f''''''
                letterdict=self.alphabetizeddict[startingletter]
                for departmentname in letterdict:
                    departmenturl=letterdict[departmentname]

                    departmentname=departmentname.replace('/','_')
                    departmentfolderpath=os.path.join(letterfolder,departmentname)


                
                
                    departmentnamecleaned=departmentname.replace(' ','').lower()
                    departmentnamecleaned=departmentnamecleaned.replace(',','-').lower()

                    departmentnamecleaned=departmentnamecleaned.replace('/','_')

            
                
                    # print(f'Starting for {departmentname}')
                
                    

                    
                    
                    departmentnamepage=f'{departmentnamecleaned}.html\n'


                    displaydepartmentname=departmentname.replace('_','/')
                    displaydepartmentname=departmentname.strip().split('-')
                    code=displaydepartmentname[0].strip()
                    departmentnamehalf=displaydepartmentname[-1].strip()
                    displaydepartmentname=f'({code}) - {departmentnamehalf}'

                    departmentlist_ul_element_content+=f'''<li class="departmentlink"><a href="{departmentnamepage}">{displaydepartmentname}</a>
                    <a href="{departmentnamepage}">
                    
                    
                    </a>
                    </li>'''

                
                departmentlist_ul_element=f'''

                <ul>{departmentlist_ul_element_content}
                </ul>'''
                return departmentlist_ul_element
            
            #now build the data dict  
            letterpagedata = {
                "headtag": self.headtag,
                "startingletter": startingletter,
                "site_favicon": self.images.get("site_favicon"),
                "departmentlist_ul_element": make_departmentlist_ul(),
                "linkicon": self.images.get("linkicon"),
                "bodytag": self.bodytag,
                "footer": self.footer
            }

              
            
            def makefullhtmlcode(startingletter):

               
                startingletter=startingletter.lower()
                print(f'Starting letter {startingletter}')
                letterwebsitefolder=os.path.join(self.deparmentsfolder,startingletter)
                
                letterwebsitepage=f'{startingletter}-departments.html'

                if not os.path.exists(letterwebsitefolder):
                    os.mkdir(letterwebsitefolder)
                
                fullpagepath=os.path.join(letterwebsitefolder,letterwebsitepage)
                letterpagerendered=self.lettertemplate.render(letterpagedata)

                with open(fullpagepath,'w') as fullpage:
                    fullpage.write(letterpagerendered)
            
            makefullhtmlcode(startingletter=startingletter)
        # now its done
        return 0
# --------------------------------Degree pages now ----------------------------------

    def upload_department_files(self):

        '''


        '''

        for startingletter in self.alphabetizeddict:

            letterfolder=os.path.join(self.asset_folder_path,startingletter)
            
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
    
                # print(f'Starting for {departmentname}')

                # its already cleaned
                print(f'Department name cleaned {departmentnamecleaned}')


                def get_asset_lists(departmentfolder):
                    csvlist=[]
                    excellist=[]
                    pdflist=[]
                    mmdlist=[]
                    # os.walk recursively travels everything
                    for root, dirs, files in os.walk(departmentfolder):
                        for file in files:
                            
                            # we neewd the fullpath in the list since thats the way it can be uploaded to google cloud.

                            full_path = os.path.join(root, file)

                            if os.path.splitext(file)[1]=='.csv':
                                csvlist.append(full_path)
                                # removes those dollar sign excel files. 
                            elif os.path.splitext(file)[1]=='.xlsx' and not file.startswith(("~$", "$")):
                                excellist.append(full_path)
                            elif os.path.splitext(file)[1]=='.pdf':
                                pdflist.append(full_path)
                            elif os.path.splitext(file)[1]=='.mmd':
                                mmdlist.append(full_path)

                    # these lists have the full paths since they'll be used to upload stuff. 
                    return [csvlist,excellist,pdflist,mmdlist]

                
                def upload_to_googlecloud(source_file_name,departmentnamecleaned):
                    print(f'Beginning upload for {source_file_name}')

                    # how to manually change credentials...


                    # just change project name here to change where they go.
                    # In code, for multiple schools. Dope.
                    # this project stays the same
                    client = storage.Client(project='degreeview-ut')


                    # this should return the email used for google cloud. Its a service email tho

                    # yeah the project is the same as the bucket name. In the future change this, as the bucketname is what user sees
                    bucket = client.bucket('utcourses')
                    # bucket list


                    #This is what will be in the url and what the name of the object will be in google cloud storage

                    cleaned_object_name=source_file_name.split('/')[-1]        


                    # make it so each file has the type. 
                    # define upload blob here
                
                    if os.path.splitext(source_file_name)[1]=='.csv':
                        uploadblob =f'{departmentnamecleaned}/csvs/{cleaned_object_name}'
                        uploadblob=bucket.blob(uploadblob)
                    elif os.path.splitext(source_file_name)[1]=='.xlsx':
                        uploadblob =f'{departmentnamecleaned}/excel-files/{cleaned_object_name}'
                        uploadblob=bucket.blob(uploadblob)


                    elif os.path.splitext(source_file_name)[1]=='.pdf':
                        uploadblob =f'{departmentnamecleaned}/pdfs/{cleaned_object_name}'
                        uploadblob=bucket.blob(uploadblob)

                    elif os.path.splitext(source_file_name)[1]=='.mmd':
                        uploadblob =f'{departmentnamecleaned}/mmds/{cleaned_object_name}'
                        uploadblob=bucket.blob(uploadblob)


                    else:
                        uploadblob = cleaned_object_name
                        uploadblob=bucket.blob(uploadblob)

                    # add a check to not do it many times
                    
                    
                    if not uploadblob.exists():
                        uploadblob.upload_from_filename(source_file_name)

                        uploadblob.make_public()  # Makes it publicly accessible
                        # can also use blob.make_private()
                    # else:
                        # print(f'{uploadblob.name} already exits, didnt upload\n')


                    # use this link on the website to serve the file.
                    return uploadblob.public_url

                def loop_through_assets_to_upload():
                    '''
                    This function uses the get_assetlists functions above to get all the paths to the asset files, in each degree folder.
                    Then it uses upload_degree_files() to upload each one one by one.

                    IMPORTANT: Here is where you can change if replacing csv files, excel files, or more pdfs. 

                    I never upload the mermaids either, which is fair.

                    '''
                    csvlist=get_asset_lists(departmentfolder=departmentfolderpath)[0]
                    excellist=get_asset_lists(departmentfolder=departmentfolderpath)[1]
                    pdflist=get_asset_lists(departmentfolder=departmentfolderpath)[2]

                    coursescsv=[csv for csv in csvlist if "courses" in csv][0]

                    # mmds currently not needing to be uplaoded.
                    
                    currentonlyupload=['redtheme','cursivetheme']
                    limited_excel_list = [
                        file for file in excellist 
                        if any(substring in file for substring in currentonlyupload)
                    ]
            
                    
                    # only one csv in there rn anyway
                    for csvfile in csvlist:
                        # comment these out depending on which ones I want
                        upload_to_googlecloud(csvfile,departmentnamecleaned)
                        print(f'Uploaded {csvfile} to cloud\n')

                    for excelfile in limited_excel_list:
                        if not excelfile.startswith(("~$", "$")):
                            upload_to_googlecloud(excelfile,departmentnamecleaned)
                            print(f'Uploaded {excelfile} to cloud\n')

                # this one actually uploads everything
                loop_through_assets_to_upload()

            print(f'\n\nEnding Cloud Upload for {startingletter} degreefiles \n\n\n\n')
    
                

    def create_department_pages(self):
        '''
     this is hard af
        '''
        for startingletter in self.alphabetizeddict:

            letterfolder=os.path.join(self.asset_folder_path,startingletter)
            
            letterdict=self.alphabetizeddict[startingletter]

            for departmentname in letterdict:
                '''
                This is the for loop everything has to be done in
                '''
                
                    

                departmenturl=letterdict[departmentname]
                # just use all of this

                (
                departmentname,
                departmentnamecleaned,
                displaydepartmentname,
                departmentnamehalf,
                departmentcode,
                ) = self.get_departmentnames(departmentname)

                departmentfolderpath=os.path.join(letterfolder,departmentname)

                


            
        
            
                # print(f'Starting for {departmentname}')
            
        

                # its already cleaned
                print(f'Department name cleaned {departmentnamecleaned}')

                startingletter=startingletter.lower()
                letterwebsitepage=f'{startingletter}-departments.html'
                letterpagereferencepath=f'../{startingletter}/{letterwebsitepage}'

                scripts=f'''

                    <script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>



                    <!-- Hover Script -->

                    <script src="../../static/js/headingcolorchange.js"></script>
                    <!-- copy script -->
                    <script src="../../static/js/copytable.js"></script>

                    <!-- animate table script -->
                    <script src="../../static/js/animatetable.js"></script>
    '''
                # now I need to pass in all values from statsdict
               

            #    all statsdict values are referenced in the template

            # get file types

           
            # finish the rest of them when its time to upload.

                def readfromjson():
                    statsjsonpath=os.path.join(departmentfolderpath,f'{departmentnamecleaned}-statsjson.json')

                    with open(statsjsonpath) as statsfile:
                        statsdict=json.load(statsfile)

                    return statsdict
                
                
                
                
                def make_course_rows():
                    '''
                    This will open up the departments database and make courserows
                    Then pass it into the Jinja template.
                    
                    '''


                    databasepath=os.path.join(departmentfolderpath,f'{departmentnamecleaned}-database.db')
                    tablename=self.get_tablename(departmentnamecleaned)


                    def getdatabaserows():
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

                    rows=getdatabaserows()

                    
                    courserows=f'''

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
                        courserows+=tr
                    return courserows
                                
                def get_degree_assetcloudpaths_lists(departmentfolder,departmentnamecleaned):
                    '''
                    Reconstruct the asset names manually like this:

                    https://storage.googleapis.com/[BUCKET_NAME]/[OBJECT_NAME]

                    Unlike other functions, this is by degree not school.
                    As such this will not contain any school specific csv or excel files. 
                    Those have to be obtained with another function. 
                    This function returns the links that will be added to the website. That way I can get the links without a class A operation

                    '''

                    

                    csv_path_list=[]
                    excel_path_list=[]
                    pdf_path_list=[]
                    mmd_path_list=[]
                    # os.walk recursively travels everything

                    prefix=f'{departmentnamecleaned}'
                    for root, dirs, files in os.walk(departmentfolder): 
                        for file in files:
                            # we neewd the fullpath in the list since thats the way it can be uploaded to google cloud.


                            if os.path.splitext(file)[1]=='.csv':
                                objectname_incloud=f'{prefix}/csvs/{file}'
                                googlecloudpath=f'{self.cloudbucketpath}/{objectname_incloud}'

                                csv_path_list.append(googlecloudpath)
                                # removes those dollar sign excel files. 
                            elif os.path.splitext(file)[1]=='.xlsx' and not file.startswith(("~$", "$")):

                                objectname_incloud=f'{prefix}/excel-files/{file}'
                                googlecloudpath=f'{self.cloudbucketpath}/{objectname_incloud}'                            
                                excel_path_list.append(googlecloudpath)
                            elif os.path.splitext(file)[1]=='.pdf':
                            
                                objectname_incloud=f'{prefix}/pdfs/{file}'
                                googlecloudpath=f'{self.cloudbucketpath}/{objectname_incloud}'                            
                            
                                pdf_path_list.append(googlecloudpath)
                            elif os.path.splitext(file)[1]=='.mmd':
                            
                                objectname_incloud=f'{prefix}/mmds/{file}'
                                googlecloudpath=f'{self.cloudbucketpath}/{objectname_incloud}'                            
                                mmd_path_list.append(googlecloudpath)

                    return [csv_path_list,excel_path_list,pdf_path_list,mmd_path_list]
                
                csvlist=get_degree_assetcloudpaths_lists(departmentfolder=departmentfolderpath,departmentnamecleaned=departmentnamecleaned)[0]
                
                # now use these lists in the website creation. 
                # well this sample link stuff is working. Now I just have to upload them is the thing...
                print(f'\n CSV LIST:{departmentname} cloud links for csvs is\n: {csvlist}\n')

                # then I'll do upload to cloud, excel list, csv list, mermaid list, etc
                
                renderedcsvurl=f'{departmentnamecleaned}-rendered-csv.html'

               

                if len(displaydepartmentname)>60:
                    displaydepartmentname=displaydepartmentname.split(')')
                    displaydepartmentname=f'{displaydepartmentname[0]}<br>{displaydepartmentname[-1]}'

                print(f'Display department name= {displaydepartmentname}')
                # readd any that had slashes

                def make_excel_ul():
                    '''
                    This makes an excel ul element which gets passed into the Jinja template.
                    '''
                    excellist=get_degree_assetcloudpaths_lists(departmentfolder=departmentfolderpath,departmentnamecleaned=departmentnamecleaned)[1]
                    if excellist:
                        originaltheme_excel=[file for file in excellist if "originaltheme" in file][0]
                    else:
                        originaltheme_excel="placeholder, some schools dont have excel files generated yet."
                    
                    # make a custom college excel theme
                    # only two of em, original and college one.
                    # get rid of CSV's

                    # this should be an excelul list
                    '''
                    This is a list of lists.
                    The first element in each list is the name of the theme, and its also the id of the 
                    label.
                    The second is the path to the google cloud hosted file
                    '''
                    excel_ul=[
                        ["original",originaltheme_excel],
                    ]

                    return excel_ul
                
                excel_ul=make_excel_ul()

                courserows=make_course_rows()

                statsdict=readfromjson()

                '''
                I need to get departmentnamehalf and displaydepartmentname standardized across schools
                '''
                departmentpagedata = {
                    "universityname":self.universityname,
                    "headlinks": self.headlinks,
                    "headtag": self.headtag,
                    "departmentnamehalf": departmentnamehalf,
                    "sitefavicon": self.images.get("site_favicon"),
                    "displaydepartmentname": displaydepartmentname,
                    "startingletter":startingletter,
                    "letterpagereferencepath":letterpagereferencepath,
                    "courserows":courserows,
                     "bodytag": self.bodytag,
                    "footer": self.footer,
                    "statsdict":statsdict,
                    "excelul":excel_ul,
                    "departmentpagelinks_jsonpath":f'{os.path.join(self.schoolabrv,'departmentpagelinks.json')}',
                    "scripts":scripts,
                    
                }
     
                def makefullhtmlcode(startingletter):
                    # have to run createschoolpages() first so self.websiteschool folder works

                    startingletter=startingletter.lower()
                    print(f'Starting letter {startingletter}')
                    # departments folder passed in
                    letterwebsitefolder=os.path.join(self.deparmentsfolder,startingletter)
                   
                    fulldepartmentpage=os.path.join(letterwebsitefolder,f'{departmentnamecleaned}.html')
                    departmentpagerendered=self.departmentpagetemplate.render(departmentpagedata)
                    
                    # w mode overrides it
                    with open(fulldepartmentpage,'w') as htmldepartmentpage:
                        htmldepartmentpage.write(departmentpagerendered)

                    print(f'\n Made {fulldepartmentpage} as part of rendering department {departmentnamecleaned}\n')

                makefullhtmlcode(startingletter=startingletter)

        return 0

# ---------------------END of make rendered degree pages


    def create_departmentpagelinks_json(self):
        '''
        This file should essentially simply build all the departmentlinks, then build the full functional file.

        This allows for the functionality of the "random page button".

        How it works is there is a json file with all of the links
        And then the js reads it
        '''


        departmentpagelinks=[]

        for departmentname in self.jsondata:

    

            (
            departmentname,
            departmentnamecleaned,
            displaydepartmentname,
            departmentnamehalf,
            departmentcode,
                ) = self.get_departmentnames(departmentname)
        
         
    
        
            print(f'Department: {departmentname}')
        


            departmentpagelink=os.path.join('departments',f'{departmentnamecleaned}.html')

            departmentpagelinks.append(departmentpagelink)


        # the only thing thats dynamic is the json by school
        # so thats the only thing we have to make
        # in a better website 
        with open(self.departmentpagelinks,'w') as departmentpagelinks_json:
            json.dump(departmentpagelinks,departmentpagelinks_json,indent=4)
        
            
    def createstatspage(self):
        '''This will create the University wide stats html page'''

        with open(self.universitystatsjson,'r') as sdjson:
            universitystatsdict=json.load(sdjson)

        print(f'universitystatsdict: {universitystatsdict}')
        template_data={
        "schoolabrv":self.schoolabrv,
        "universityname":self.universityname
        }
        
        template_data.update(universitystatsdict)
        # Jinja must take name=value pairs
        statspage_rendered=self.statspage_template.render(template_data)


        with open(self.statspage,'w') as fullpage:
            fullpage.write(statspage_rendered)
        

    def create_sorteddepartments_page(self):
        '''
        This function will use sorted_departments_json.json and make a page for it for 
        every instance of this class (every University)

        '''

        with open(self.sorted_departments_json,'r') as sdjson:
            sorted_departments=json.load(sdjson)

        
        template_data={
        "schoolabrv":self.schoolabrv,
        "sorted_departments":sorted_departments,
        "universityname":self.universityname
        }
        # Jinja must take name=value pairs
        sorteddepartments_page_rendered=self.sorted_departments_template.render(template_data)


        with open(self.sorted_departments_page,'w') as fullpage:
            fullpage.write(sorteddepartments_page_rendered)

    def create_uni_homepage(self):
        '''
        Uses a Jinja template to create each schools homepage.
        Has to read some variables from the init.


        '''
        '''This will create the University wide stats html page'''

        def make_departmentlinks_dict():
            departmentlinks_dict={}

            for startingletter in self.alphabetizeddict:

                letterfolder=os.path.join(self.asset_folder_path,startingletter)
                
                letterdict=self.alphabetizeddict[startingletter]

                if startingletter not in departmentlinks_dict:
                    departmentlinks_dict[startingletter]={}



                for departmentname in letterdict:
                    '''
                    This is the for loop everything has to be done in
                    '''
                    
                        

                    departmenturl=letterdict[departmentname]
                    # just use all of this
                    
                    (
                    departmentname,
                    departmentnamecleaned,
                    displaydepartmentname,
                    departmentnamehalf,
                    departmentcode,
                        ) = self.get_departmentnames(departmentname)
                    departmentpagelink=os.path.join('departments',startingletter.lower(),f'{departmentnamecleaned}.html')

                    # adding to the dict logic
                    # we do the og department name cause it looks best
                    departmentlinks_dict[startingletter][departmentname]=departmentpagelink
            return departmentlinks_dict
        
        departmentlinks_dict=make_departmentlinks_dict()

        # uncomment to show departmentlinksdict.
        # print(f'Departmentlinks_dict for homepage: \n{departmentlinks_dict}')


        template_data={
        "schoolabrv":self.schoolabrv,
        "universityname":self.universityname,
        "departmentlinks_dict":departmentlinks_dict,
        }
        
        
        # Jinja must take name=value pairs
        homepage_rendered=self.homepage_template.render(template_data)


        with open(self.homepage,'w') as fullpage:
            fullpage.write(homepage_rendered)
        
        def create_homepage_ul():
            '''
            This returns the ul that will go on the homepage.

            This needs to be moved to the create_school_homepage function
            '''

            lis=f'''

                '''
            for startingletter in self.alphabetizeddict:
                startingletter=startingletter.lower()
                
                letterwebsitepage=f'{startingletter}-departments.html'

                
                fullpagepath=os.path.join("departments",startingletter,letterwebsitepage)

            
                li=f'''
                <li class="homepage-column">
                <a href="{fullpagepath}"
                ><div class="contentdiv">{startingletter.upper()} Departments</div></a
                >
            </li>
    '''
                lis+=li
                
                
            homepageul=f'''
            <ul class="homepage-ul">
            {lis}
            </ul>
            '''
            print(homepageul)

        departmentcontainerdata={
            "A":[{"departmentname":"","departmenturl":""},{"departmentname":"","departmenturl":""}]
        }
        
        
        # with open a template...write to it with variables, boom.

# -------------END of class -----------------------

    


# architecure_testing()
  
        

# storage te
     



# deprecated

def main():

   
    ut_specs=[
                    "degreeview_expansion/utcourses",
                    "The University of Texas at Austin"
                    ,"https://storage.googleapis.com/utcourses",
                    "/Users/shalevwiden/Downloads/Projects/testsite/ut",
                    "UT"]
    websiteobject=createUniversity(*ut_specs)
    print(f'School folder :\n {websiteobject.schoolfolder}')
    # print(websiteobject.alphabetizeddict)
    # websiteobject.createstatspage()
    websiteobject.create_uni_homepage()

    # websiteobject.create_department_pages()
    # websiteobject.createletterpages()


    
print(f'\nthe python version being used is:{sys.executable}\n')

if __name__=="__main__":
    main()