

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
from jinja2 import Environment, FileSystemLoader



# use this to upload stuff to google cloud
from google.cloud import storage


# use this to import stuff from other python files
import importlib.util

file_path = '/Users/shalevwiden/Downloads/Coding_Files/Python/BeautifulSoup_Library/college_course_scraping/theassetcontainment.py'

# but be something else besides config for the name
spec = importlib.util.spec_from_file_location("config", file_path)
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)

theasset=config.theasset
# you can also assign a function

# the asset is important here because it contains the name of every degree in it.


class createWebsite:
    def __init__(self):

        self.assetspath='/Users/shalevwiden/Downloads/Projects/dvassets/texas/UT_courses'

        self.jsondatapath ='/Users/shalevwiden/Downloads/Coding_Files/Python/BeautifulSoup_Library/degreeview_expansion/ut_courses/utjson.json'

        self.universityname='The University of Texas at Austin'

        self.randompagehspath="/Users/shalevwiden/Downloads/Projects/dvschoolsites/texas/utcoursessite/static/js/randompage.js"
        self.cloudbucketpath='https://storage.googleapis.com/utcourses'



        with open(self.jsondatapath,'r') as universityjson:

            self.jsondata=json.load(universityjson)

        self.alphabetizeddict={}

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

        # -----------New cleaned schoolname and websitefoler stuff --------------

        # self.departmentfolders= [os.path.join(self.assetspath,folder) for folder in os.listdir(self.assetspath) 
        #    if os.path.isdir(os.path.join(self.assetspath, folder))]
        # self.departmentfolders.sort()


        # can I have spaces is the question

        self.websitepath='/Users/shalevwiden/Downloads/Projects/degreeviewwebsite/texas/utcoursessite/departments'

        self.images={
            
            "linkicon":"https://storage.googleapis.com/degreeview/degreeviewimages/linkicon.svg",
            "logo5":"https://storage.googleapis.com/degreeview/degreeviewimages/logo5.png",

            "minilogo":"https://storage.googleapis.com/degreeview/degreeviewimages/minilogo.png",
            "site_favicon":"https://storage.googleapis.com/degreeview/degreeviewimages/site_favicon.png"
        }
        
        with open('/Users/shalevwiden/Downloads/Projects/dvwebsitecreation/sourcefiles/html_components/degreeviewfooter.html','r') as footerfile:
            self.footer=footerfile.read()
        with open('/Users/shalevwiden/Downloads/Projects/dvwebsitecreation/sourcefiles/html_components/departmentpage.html','r') as headfile:
            self.headlinks=headfile.read()


        self.outputspath='/Users/shalevwiden/Downloads/Projects/dvwebsitecreation/templating/outputs'
        with open('/Users/shalevwiden/Downloads/Projects/dvwebsitecreation/sourcefiles/googleanalytics_tags/degreeviewtag/headtag.html','r') as headtag:
            self.headtag=headtag.read()
        with open('/Users/shalevwiden/Downloads/Projects/dvwebsitecreation/sourcefiles/googleanalytics_tags/degreeviewtag/bodytag.html','r') as bodytag:
            self.bodytag=bodytag.read()

        # footer so I dont have to redefine it multiple times. 

        

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
        '''
        # this ensures other folders arent added
        
        for startingletter in self.alphabetizeddict:

            letterfolder=os.path.join(self.assetspath,startingletter)
           
            
            
                # its already cleaned
        
        # --------------------------
            schoolinfo=f'Every degree page has 2 csvs, 2 excel files, and a sample semester diagram.\n\
            More files coming in the future.' 

            headhtmlcode=f'''
<head>
{self.headtag}
    <meta
        name="description"
        content="{startingletter} Degrees and Data"
        />

     <meta
      name="keywords"
      content="degree, major, UT Austin, degreeview, course diagrams, course excel files, degree stats, {startingletter}"
    />

    <meta name="author" content="DegreeView" />
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

     <!-- favicon icon -->
    <link rel="icon" href="../metaassets/site_favicon.png" type="image/png" />
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-S06MYR1FV6"></script>
    <script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', 'G-S06MYR1FV6');
</script>
<!-- to track the new update -->
    <script>
      if (window.location.pathname === "/utcoursesindex") {{
        gtag("event", "courses_index_view");
      }}
    </script>

    <title>{startingletter} Page - DegreeView</title>

    <!-- main stylesheet -->
    <link rel="stylesheet" href="../../static/css/letterpage.css" />

    <!-- animation stylesheet -->
    <link rel="stylesheet" href="../../static/css/animations.css" />

    <!-- Barlow Font -->
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600;700;900&display=swap" rel="stylesheet">

    <!-- Roboto Font -->
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
    href="https://fonts.googleapis.com/css2?family=Barlow:ital,wght@0,400;1,100;1,300;1,900&family=Roboto:ital,wght@0,100..900;1,100..900&display=swap"
    rel="stylesheet"
    />
    <!-- Icons ( download icon and many file icons from here is used) -->
    <link
    rel="stylesheet"
    href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css"
    />
</head>
'''
            def make_abovemainsitecode():
                # for the "home" box that needs to go direct to DegreeView home

                abovemainsitecode=f'''
    <div class="abovemainsite">
        <div class="topnav">
            <nav class="breadcrumbs">
            <ul>
                <li><a href="../../utcoursesindex.html">DegreeView UT</a></li>
                <i class="fa fa-chevron-right"></i>

                <li id="current">{startingletter} Departments</li>
            </ul>
            </nav>
            <nav class="homeandabout">
            <ul>
                
                <li><a href="../../../index.html">Home</a></li>
                <li><a href="../../../about.html">About</a></li>
                <li><a href="../ut-stats.html">Stats</a></li>
            </ul>
            </nav>
        </div>
        <div class="schoolnamebox">
            <h1 id="schoolnametitle">{startingletter} Departments</h1>
        </div>
        </div>
    '''
                return abovemainsitecode
            

            def make_departmentlist_ul():
                departmentlist_ul_element_content=f''''''
                letterdict=self.alphabetizeddict[startingletter]
                for departmentname in letterdict:
                    departmenturl=letterdict[departmentname]

                    departmentname=departmentname.replace('/','_')
                    departmentfolderpath=os.path.join(letterfolder,departmentname)


                
                
                    departmentnamecleaned=departmentname.replace(' ','').lower()
                    departmentnamecleaned=departmentnamecleaned.replace(',','-').lower()

                    departmentnamecleaned=departmentnamecleaned.replace('/','_')

            
                
                    print(f'Starting for {departmentname}')
                
                    

                    
                    
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
            
            def make_mainsitecode():

                
                '''This gets the asset cloud list. Since theres only 1 csv currently, we good.'''

                
                # get first, and only, item from the list
                test='test'
                print(f'School departments CSV is {test}\n')

                leftcontentcode=f'''
            <div class="leftcontent">
            <p id="futuremessage">
            There will be stuff here in a future update, coming soon.
          </p>
            </div>
            '''
                

                departmentlist_ul_element=make_departmentlist_ul()


                rightcontentcode=f'''        <div class="rightcontent">
    <div class="departmentlistheaderbox">
            <h3 id="departmentlistheader">{startingletter} Departments       <img class="linksvg" src="{self.images.get("linkicon","not found")}" alt=""
                /></h3>
            </div>
            <!-- Contains links to every departmentpage -->
            <div class="departmentlistbox">{departmentlist_ul_element}</div>
            </div>
                
                '''


                mainsitecode=f'''      
                <div class="mainsite">

                {leftcontentcode}
                {rightcontentcode}
    </div>
    '''
                return mainsitecode
        
            def makebodyhtmlcode():
                abovemainsitecode=make_abovemainsitecode()
                mainsitecode=make_mainsitecode()

                undermainsitecode=f'''
                <div class="undermainsite">
                <!-- this can be empty and like 20 px tall just to take up space, and be used for something in the future
                    -->
                
                </div>
    '''
                bodyhtmlcode=f'''
                <body>
                {self.bodytag}
                <div class="sitecontainer">
                {abovemainsitecode}
                {mainsitecode}
                {undermainsitecode}
                {self.footer}
                <!-- Hover Script -->
                <script src="../../static/js/headingcolorchange.js"></script>


                </div>
                </body>

                '''
                return bodyhtmlcode
            
            def makefullhtmlcode(startingletter):

                bodyhtmlcode=makebodyhtmlcode()

                fullhtmlcode=f'''
                    <!DOCTYPE html>
                    <html lang="en">
                    {headhtmlcode}
                    {bodyhtmlcode}\n
                
                    </html>'''
                startingletter=startingletter.lower()
                print(f'Starting letter {startingletter}')
                letterwebsitefolder=os.path.join(self.websitepath,startingletter)
                
                letterwebsitepage=f'{startingletter}-departments.html'

                if not os.path.exists(letterwebsitefolder):
                    os.mkdir(letterwebsitefolder)
                
                fullpagepath=os.path.join(letterwebsitefolder,letterwebsitepage)

                with open(fullpagepath,'w') as fullpage:
                    fullpage.write(fullhtmlcode)
            
            makefullhtmlcode(startingletter=startingletter)

        return 0


# --------------------------------Degree pages now ----------------------------------

    def upload_department_files(self):

        '''


        '''

        for startingletter in self.alphabetizeddict:

            letterfolder=os.path.join(self.assetspath,startingletter)
            
            letterdict=self.alphabetizeddict[startingletter]
            for departmentname in letterdict:
                departmenturl=letterdict[departmentname]

                departmentname=departmentname.replace('/','_')
                departmentfolderpath=os.path.join(letterfolder,departmentname)


            
            
                departmentnamecleaned=departmentname.replace(' ','').lower()
                departmentnamecleaned=departmentnamecleaned.replace('/','-')
        
            
                print(f'Starting for {departmentname}')
            
                departmentname=departmentname.replace('/','-').strip()

                departmentnamecleaned=departmentname.replace(',',"-")
                departmentnamecleaned=departmentnamecleaned.replace(" ", "").lower()

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
                    
                    currentonlyupload='redtheme'
                    limited_excel_list=[file for file in excellist if currentonlyupload in file]

            
                    
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

            letterfolder=os.path.join(self.assetspath,startingletter)
            
            letterdict=self.alphabetizeddict[startingletter]
            for departmentname in letterdict:
                departmenturl=letterdict[departmentname]

                departmentname=departmentname.replace('/','_')
                departmentfolderpath=os.path.join(letterfolder,departmentname)


            
            
                departmentnamecleaned=departmentname.replace(' ','').lower()
                departmentnamecleaned=departmentnamecleaned.replace('/','-')
        
            
                print(f'Starting for {departmentname}')
            
                departmentname=departmentname.replace('/','-').strip()

                departmentnamecleaned=departmentname.replace(',',"-")
                departmentnamecleaned=departmentnamecleaned.replace(" ", "").lower()

                # its already cleaned
                print(f'Department name cleaned {departmentnamecleaned}')



            

            # get file types

           
            # finish the rest of them when its time to upload.

                def readfromjson():
                    statsjsonpath=os.path.join(departmentfolderpath,f'{departmentnamecleaned}-statsjson.json')

                    with open(statsjsonpath) as statsfile:
                        statsdict=json.load(statsfile)

                    return statsdict
                
                def readhtmltable():
                    htmltablepath=os.path.join(departmentfolderpath,f'{departmentnamecleaned}-htmltable.html')

                    with open(htmltablepath) as htmltable:
                        tablecode=htmltable.read()

                    return tablecode


                
                def get_degree_assetcloudpaths_lists(departmentfolder,departmentnamecleaned):
                    '''
                    Reconstruct the asset names manually like this:

                    https://storage.googleapis.com/[BUCKET_NAME]/[OBJECT_NAME]

                    Unlike other functions, this is by degree not school.
                    As such this will not contain any school specific csv or excel files. 
                    Those have to be obtained with another function. 
                    This function returns the links that will be added to the website. That way I can get the links without a class A operation

                    '''

                    if '-' in departmentnamecleaned:
                        departmentnamecleaned=departmentnamecleaned.split('-')
                        departmentnamecleaned='-'.join(departmentnamecleaned[1:])
                    csv_path_list=[]
                    excel_path_list=[]
                    pdf_path_list=[]
                    mmd_path_list=[]
                    # os.walk recursively travels everything

                    prefix=f'{startingletter.lower()}/{departmentnamecleaned}'
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
                print(f'\n {departmentname} cloud links for csvs is\n: {csvlist}\n')

                # then I'll do upload to cloud, excel list, csv list, mermaid list, etc
                
                renderedcsvurl=f'{departmentnamecleaned}-rendered-csv.html'

                displaydepartmentname=departmentname.replace('_','/')
                displaydepartmentname=departmentname.strip().split('-')
                code=displaydepartmentname[0].strip()
                departmentnamehalf=displaydepartmentname[-1].strip()
                displaydepartmentname=f'({code}) - {departmentnamehalf}'

                if len(displaydepartmentname)>60:
                    displaydepartmentname=displaydepartmentname.split(')')
                    displaydepartmentname=f'{displaydepartmentname[0]}<br>{displaydepartmentname[-1]}'

                print(f'Display department name= {displaydepartmentname}')
                # readd any that had slashes

            
                headhtmlcode=f'''
    <head>
    {self.headtag}
    <meta
        name="description"
        content="Visualize {departmentnamehalf} at UT Austin through diagrams and tabular data."
        />

        <meta
        name="keywords"
        content="degree, major, UT Austin, degreeview, course diagrams, course excel files, degree stats, {displaydepartmentname}"
        />

        <meta name="author" content="DegreeView" />

        <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />

            <!-- favicon icon -->
            <link rel="icon" href="{self.images.get('site_favicon')}" type="image/png" />
            <!-- Google tag (gtag.js) -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-S06MYR1FV6"></script>
        <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());

    gtag('config', 'G-S06MYR1FV6');
    </script>
   
            <title>{departmentnamehalf} UT Page - DegreeView</title>

            
        <!-- main stylesheet -->
        <link rel="stylesheet" href="../../static/css/coursepage.css" />


        {self.headlinks}

            </head>

    '''
                def make_abovemainsitecode(startingletter):

                    startingletter=startingletter.lower()
                    letterwebsitepage=f'{startingletter}-departments.html'
                    letterpagereferencepath=f'../{startingletter}/{letterwebsitepage}'




                    abovemainsitecode=f'''

        <div class="abovemainsite">
            <div class="topnav">
            <nav class="breadcrumbs">
                <ul>
                <li><a href="../../utcoursesindex.html">DegreeView UT</a></li>
                <i class="fa fa-chevron-right"></i>

                <li><a href="{letterpagereferencepath}">{startingletter.upper()} Departments</a></li>
                <i class="fa fa-chevron-right"></i>

                <li id="current">
                    {displaydepartmentname}
                </li>
                </ul>
            </nav>
            <nav class="homeandabout">
                <ul>
                
                <li><a href="../../../index.html">Home</a></li>
                <li><a href="../../../about.html">About</a></li>
                <li><a href="../ut-stats.html">Stats</a></li>
                </ul>
            </nav>
            </div>
            <div class="degreenamebox">
            <h1 id="degreenametitle">
            {displaydepartmentname}
            </h1>
            </div>
        </div>
    '''
                    return abovemainsitecode

                
                def make_mainsitecode():
                    '''
                    This is simply a function that generates leftcontentcode and rightcontentcode, then puts it together in main content code. 
                    '''
                    
                    # get csv links
                    csvlist=get_degree_assetcloudpaths_lists(departmentfolder=departmentfolderpath,departmentnamecleaned=departmentnamecleaned)[0]
                    print(f'CSV list: {csvlist}')
                    # this is accurate
                    coursescsv=[csv for csv in csvlist if "coursescsv" in csv][0]

                    # get excel links
                    excellist=get_degree_assetcloudpaths_lists(departmentfolder=departmentfolderpath,departmentnamecleaned=departmentnamecleaned)[1]


                    blacktheme_excel=[file for file in excellist if "blacktheme" in file][0]

                    originaltheme_excel=[file for file in excellist if "originaltheme" in file][0]
                    
                    
                    
                    darktheme_excel=[file for file in excellist if "darktheme" in file][0]
                    
                    green_excel=[file for file in excellist if "greentheme" in file][0]

                    desert_excel=[file for file in excellist if "deserttheme" in file][0]

                    grey_excel=[file for file in excellist if "grey" in file][0]

                    ocean_excel=[file for file in excellist if "ocean" in file][0]
                    pastel_excel=[file for file in excellist if "pastel" in file][0]

                    primarycolors_excel=[file for file in excellist if "primarycolors" in file][0]
                    neon_excel=[file for file in excellist if "neon" in file][0]


                
                    def makeleftcontentcode():
                        '''Using the links just received above, now link them in the left content code in the website'''


                        env = Environment(loader=FileSystemLoader("/Users/shalevwiden/Downloads/Projects/dvwebsitecreation/templating/templates"))
        

                        # Pick template
                        template = env.get_template("leftcontentcode_departments.html")

                        # in jinja, reference the keys
                        variables={
                            "departmentnamehalf":departmentnamehalf,

                            "coursescsv":coursescsv,
                            "blacktheme_excel": blacktheme_excel,
                            "originaltheme_excel":originaltheme_excel,
                            "darktheme_excel":darktheme_excel,
                            "green_excel":green_excel,
                            "desert_excel":desert_excel,
                            "grey_excel":grey_excel,
                            "ocean_excel":ocean_excel,
                            "pastel_excel":pastel_excel,
                            "primarycolors_excel":primarycolors_excel,
                            "neon_excel":neon_excel


                        }

                        rendered_html = template.render(variables)

                        leftcontentcode=rendered_html

                        return leftcontentcode
                    def makerightcontentcode():
                        '''
                        For the right content code it has stats in it
                        '''

                        statsdict=readfromjson()
                       


                        gradcountsection=f'''
                        <section class="statsline" id="gradcount">
                        <div class="statsname">Graduate Courses Count</div>
                        <div class="statscontent">{statsdict['grad_count']}, {statsdict['grad_percent']}</div>
                        </section>
                            '''
                        departmentstats=f'''
<div class="departmentstats">
            <section class="statsline" id="coursecount">
              <div class="statsname">Department Course Count</div>
              <div class="statscontent">{statsdict['course_count']}</div>
            </section>
            <section class="statsline" id="longestname">
              <div class="statsname">Longest Course Name</div>
              <div class="statscontent">{statsdict['longest_course_name']}</div>
            </section>
            <section class="statsline" id="shortestname">
              <div class="statsname">Shortest Course Name</div>
              <div class="statscontent">{statsdict.get('shortest_course_name',"Not found")}</div>
            </section>
            <section class="statsline" id="lowercount">
              <div class="statsname">Lower Division Course Count</div>
              <div class="statscontent">{statsdict.get('lower_count',"Not found")}, {statsdict.get('lower_percent',"Not found")}</div>
            </section>
            <section class="statsline" id="uppercount">
              <div class="statsname">Upper Division Course Count</div>
              <div class="statscontent">{statsdict.get('upper_count',"Not found")}, {statsdict.get('upper_percent',"Not found")}</div>
            </section>
            {gradcountsection}

            <section class="statsline" id="samenamecount">
              <div class="statsname">Number of {departmentnamehalf} Courses with "{departmentnamehalf}" in their name</div>
              <div class="statscontent">{statsdict.get('samenamelen',"Not found")}, {statsdict.get('samenamepercent',"Not found")}</div>
            </section>
          </div>
'''
                        rightcontentcode=f'''
                        <div class="rightcontent">
                        <div class="displaynamebox">
                <h3 id="displayname">{displaydepartmentname} Statistics &nbsp; &nbsp;<span class="material-symbols-outlined" id="charticon">
                bar_chart_4_bars
              </span> </h3>
                
                
            </div>
            {departmentstats}
                    </div>



                    

            
    '''
                        return rightcontentcode
                    # end makerightcontentcodefunction()
                    
                    leftcontentcode=makeleftcontentcode()
                    rightcontentcode=makerightcontentcode()

                    mainsitecode=f'''<div class="mainsite">
                    {leftcontentcode}
                    {rightcontentcode}
                    </div>
                    '''
                    return mainsitecode 
                
                def make_undermainsite_code():


                    htmltable=readhtmltable()


                    displaydepartmentname=departmentname.replace('_','/')
                    displaydepartmentname=departmentname.strip().split('-')
                    code=displaydepartmentname[0].strip()
                    departmentnamehalf=displaydepartmentname[-1].strip()
                    displaydepartmentname=f'({code}) - {departmentnamehalf}'
                    
                    undermainsitecode=f'''
                <div class="undermainsite">
                <h3 id="departmenttableheading"> {departmentnamehalf} Department Courses Table</h3>

                <div class="copyanddownload">
                    <div class="animatetable">
                    <button id="animatebutton">Animate</button>
                    </div>

                    <i class="fa-regular fa-copy" id="copyicon" title="Copy Table"></i>
                    <!-- contains the rendered csv -->
                
                </div>

                {htmltable}
                </div>

                '''
                    return undermainsitecode
                def makebodyhtmlcode():
                    abovemainsitecode=make_abovemainsitecode(startingletter=startingletter)
                    mainsitecode=make_mainsitecode()
                    undermainsitecode=make_undermainsite_code()


                    csvlist=get_degree_assetcloudpaths_lists(departmentfolder=departmentfolderpath,departmentnamecleaned=departmentnamecleaned)[0]


                    scripts=f'''

                    <script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>



                    <!-- Hover Script -->

                    <script src="../../static/js/headingcolorchange.js"></script>
                    <!-- copy script -->
                    <script src="../../static/js/copytable.js"></script>

                    <!-- animate table script -->
                    <script src="../../static/js/animatetable.js"></script>
    '''

                    bodyhtmlcode=f'''                    
                    <body>
                    {self.bodytag}       
                    <div class="sitecontainer">
                    {abovemainsitecode}
                    {mainsitecode}
                    {undermainsitecode}

                    {self.footer}
                    </div>
                    {scripts}
                    </body>

    '''
                    return bodyhtmlcode


                def makefullhtmlcode(startingletter):

                    bodyhtmlcode=makebodyhtmlcode()

                    fullhtmlcode=f'''
                        <!DOCTYPE html>
                        <html lang="en">
                        {headhtmlcode}\n
                        {bodyhtmlcode}\n
                        
                        </html>'''

        
                    # have to run createschoolpages() first so self.websiteschool folder works

                    startingletter=startingletter.lower()
                    print(f'Starting letter {startingletter}')
                    letterwebsitefolder=os.path.join(self.websitepath,startingletter)
                   

                    fulldepartmentpage=os.path.join(letterwebsitefolder,f'{departmentnamecleaned}.html')

                    with open(fulldepartmentpage,'w') as htmldepartmentpage:
                        htmldepartmentpage.write(fullhtmlcode)
                    print(f'\n Made {fulldepartmentpage} as part of making departmentpages\n')

                makefullhtmlcode(startingletter=startingletter)

        return 0

# ---------------------END of make rendered degree pages

    def create_renderedcsv_pages(self):
        '''
        These are the rendered csvs in a diferent HTML page
        '''
        def get_degreename_lists():
            degreenamelist=[]
            cleaneddegreenamelist=[]
            for i in range(1,len(self.startingletter)):
                        
                key=list(self.startingletter)[i]
                degreename=key
                degreename=degreename.replace('/','-').strip()
                degreenamelist.append(degreename)

                # clean it for website links


                degreenamecleaned=degreename.replace(' ','').lower().split('(')
                degreenamecleaned=degreenamecleaned[0]+"-"+degreenamecleaned[-1]
                degreenamecleaned=degreenamecleaned.replace(')','')

                cleaneddegreenamelist.append(degreenamecleaned)
            return degreenamelist,cleaneddegreenamelist
        
        degreenamelist, cleaneddegreenamelist=get_degreename_lists()
            
        # big for loop--------------------------------------------------------------------
        for degreefolder in self.degreefolders:
            print(f'Degree folder: \n{degreefolder}\n')
            degreefolderpath=Path(degreefolder)


            degreename=degreefolderpath.name

            
            # this thing here always happens regardless of the 
            degreename=degreename.replace('/','-').strip()

            
            degreenamecleaned=degreename.replace(' ','').lower().split('(')
            degreenamecleaned=degreenamecleaned[0]+"-"+degreenamecleaned[-1]
            degreenamecleaned=degreenamecleaned.replace(')','')
            

            # this is the folder for it in degreeview

            degreenameassetfolder=os.path.join(self.schoolfolderpath,degreename)
            print(f'degreenameassetfolder:{degreenameassetfolder}')
            

            # this is the folder for it in degreeview

            degreenameassetfolder=os.path.join(self.schoolfolderpath,degreename)
            

            # get file types

           
            # finish the rest of them when its time to upload.
            def get_degree_assetcloudpaths_lists(degreenameassetfolder):
                
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
                for root, dirs, files in os.walk(degreenameassetfolder):
                    for file in files:
                        
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

                return [csv_path_list,excel_path_list,pdf_path_list,mmd_path_list]
            
            csvlist=get_degree_assetcloudpaths_lists(degreenameassetfolder=degreenameassetfolder)[0]
            # now use these lists in the website creation. 
            # well this sample link stuff is working. Now I just have to upload them is the thing...
            print(f'\n {degreename} cloud links for csvs is\n: {csvlist}\n')

                    
            
                              
                         
            
            # then I'll do upload to cloud, excel list, csv list, mermaid list, etc
            

            displaydegreename=degreename.replace("-","/").strip().split('(')
            displaydegreename=displaydegreename[0]+'<br>'+f'({displaydegreename[-1]}'

            displaydegreename_nobr=displaydegreename.replace("<br>","")
            
            headhtmlcode=f'''
<head>
 <meta
      name="description"
      content="Visualize {displaydegreename_nobr} at UT Austin through diagrams and tabular data."
    />

     <meta
      name="keywords"
      content="degree, major, UT Austin, degreeview, course diagrams, course excel files, degree stats, {displaydegreename_nobr}"
    />

    <meta name="author" content="DegreeView" />

    <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />

         <!-- favicon icon -->
         <link rel="icon" href="../metaassets/site_favicon.png" type="image/png" />
         <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-S06MYR1FV6"></script>
    <script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', 'G-S06MYR1FV6');
</script>
        <title>{displaydegreename_nobr} Rendered CSV Page - DegreeView</title>

            
        <!-- main stylesheet -->
        <link rel="stylesheet" href="../static/css/utddegreepage.css" />

        <!-- animation stylesheet -->
        <link rel="stylesheet" href="../static/css/animations.css" />

        <!-- table styling -->
        <link rel="stylesheet" href="../static/css/tablestyling.css" />

        <!-- Rendered CSV css -->

        <link rel="stylesheet" href="../static/css/renderedcsv.css" />

        <!-- Barlow Font -->
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
        <link href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600;700;900&display=swap" rel="stylesheet">

        <!-- Roboto Font -->
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
        <link
        href="https://fonts.googleapis.com/css2?family=Barlow:ital,wght@0,400;1,100;1,300;1,900&family=Roboto:ital,wght@0,100..900;1,100..900&display=swap"
        rel="stylesheet"
        />
        <!-- Icons ( download icon and file icons from here is used) -->
        <link
        rel="stylesheet"
        href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css"
        />
        </head>

'''
            def make_abovemainsitecode():
                abovemainsitecode=f'''

      <div class="abovemainsite">
        <div class="topnav">
          <nav class="breadcrumbs">
            <ul>
              <li><a href="../index.html">DegreeView UTD</a></li>
              <i class="fa fa-chevron-right"></i>

              <li><a href="{self.schoolpage}">{startingletter}</a></li>
              <i class="fa fa-chevron-right"></i>

              <li>
                <a href="{degreenamecleaned}.html">{displaydegreename_nobr}</a>
              </li>

              <i class="fa fa-chevron-right"></i>

              <li id="current">Semester Table</li>
            </ul>
          </nav>
          <nav class="homeandabout">
            <ul>
              
              <li><a href="../index.html">Home</a></li>
              <li><a href="../aboutpage.html">About</a></li>
              <li><a href="../ut-stats.html">Stats</a></li>
            </ul>
          </nav>
        </div>
        <div class="degreenamebox">
          <h1 id="degreenametitle">
           {displaydegreename_nobr} Semester Table
          </h1>
        </div>
      </div>
'''
                return abovemainsitecode

            
              
            def makebodyhtmlcode():
                '''
                This is a little different from the makedegreepages one. Here I get the asset cloud lists and then refer to them.
                '''
                abovemainsitecode=make_abovemainsitecode()

                csvlist=get_degree_assetcloudpaths_lists(degreenameassetfolder=degreenameassetfolder)[0]

                semesterlayoutcsv=[csv for csv in csvlist if "semester" in csv][0]

                undermainsitecode=f'''
 
      <div class="undermainsite">
        <!-- contains the rendered csv -->
        <div class="renderedcsvdiv">

          <div class="copyanddownload">
            <div class="animatetable"> <button id="animatebutton">Animate</button></div>

            <i class="fa-regular fa-copy" id="copyicon" title="Copy Table"></i>
                    <!-- contains the rendered csv -->
                <a href="{semesterlayoutcsv}"
                id="downloadcsv"

            >
                        <!-- use this id to get the href to place into the javascript script to render with sheet js  -->

            <i class="fa-solid fa-arrow-up-from-bracket" title="downloadcsv"></i
            ></a>
          </div>

          <div id="semester-csvtablecontainer"></div>
        </div>
    </div>


            '''

                bodyhtmlcode=f'''                    
                <body>       
                <div class="sitecontainer">
                {abovemainsitecode}
                {undermainsitecode}
                {self.footer}

                        
                <!-- new js -->
                <!-- Sheet JS Script -->
                <script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>

                <!-- Hover Script -->

                <script src="../static/js/utdheadingcolorchange.js"></script>
                <!-- copy script -->
                <script src="../static/js/copytable.js"></script>

                <!-- animate table script -->
                <script src="../static/js/animatetable.js"></script>
                </div>
                </body>

'''
                return bodyhtmlcode


            def makefullrenderedcsvpage():

                bodyhtmlcode=makebodyhtmlcode()

                fullhtmlcode=f'''
                    <!DOCTYPE html>
                    <html lang="en">
                    {headhtmlcode}\n
                    {bodyhtmlcode}\n
                    
                    </html>'''

    
                # have to run createschoolpages() first so self.websiteschool folder works
                renderedcsvpage=os.path.join(self.websiteschoolfolder,f'{degreenamecleaned}-rendered-csv.html')
                with open(renderedcsvpage,'w') as htmlcsvpage:
                    htmlcsvpage.write(fullhtmlcode)
                print(f'\n Made {renderedcsvpage} as part of making degreepages\n')

            makefullrenderedcsvpage()

        return 0
# ---------------------END of make rendered CSV pages
 
    def create_homepage_ul(self):
        '''
        This returns the ul that will go on the homepage.
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

    def create_randompage_js(self):
        '''
        This file should essentially simply build all the departmentlinks, then build the full functional file
        '''

        randompagejspath=self.randompagejspath

        departmentpagelinks=[]


        
        for startingletter in self.alphabetizeddict:

            letterfolder=os.path.join(self.assetspath,startingletter)
            
            letterdict=self.alphabetizeddict[startingletter]
            for departmentname in letterdict:
                departmenturl=letterdict[departmentname]

                departmentname=departmentname.replace('/','_')
                departmentfolderpath=os.path.join(letterfolder,departmentname)


            
            
                departmentnamecleaned=departmentname.replace(' ','').lower()
                departmentnamecleaned=departmentnamecleaned.replace('/','-')
        
            
                print(f'Starting for {departmentname}')
            
                departmentname=departmentname.replace('/','-').strip()

                departmentnamecleaned=departmentname.replace(',',"-")
                departmentnamecleaned=departmentnamecleaned.replace(" ", "").lower()


                startingletter=startingletter.lower()

                fulldepartmentpage=os.path.join('departments',startingletter,f'{departmentnamecleaned}.html')

                departmentpagelinks.append(fulldepartmentpage)
            
        fulljscode=f'''
            const pages={departmentpagelinks}
                    
            randombutton = document.getElementById("randompagebutton");

            function gotorandompage(e) {{
            e.preventDefault(); // Prevent default link behavior

            // math.floor gets floor. Math.random returns float between 0 and 1.
            const randomIndex = Math.floor(Math.random() * pages.length);
            const randomPage = pages[randomIndex];

            // need to use window change to make the entire button clickable
            window.location.href = randomPage;
            }}

            // e means event handling
            randombutton.addEventListener("click", gotorandompage);

                '''
        
        with open(randompagejspath,'w') as randompagejs:
            randompagejs.write(fulljscode)
        

    def createstatspage(self):
        '''This will create the University Wide stats html page'''


        env = Environment(loader=FileSystemLoader("/Users/shalevwiden/Downloads/Projects/dvwebsitecreation/templating/templates"))
        

        # Pick template
        template = env.get_template("statstemplate.html")

        variables={
            "universityname":self.universityname
        }

        rendered_html = template.render(variables)

        statspageoutput=os.path.join(self.outputspath,'statspageout.html')

        with open(statspageoutput,'w') as statspage:
            statspage.write(rendered_html)

# -------------END of class -----------------------




# architecure_testing()
  
        

# storage te
     




def runcreateWebsite():
    websiteobject=createWebsite()
    websiteobject.upload_department_files()

    

    
print(f'\nthe python version being used is:{sys.executable}\n')

runcreateWebsite()