import os

import sys

import subprocess
import random

import csv
import time


# use this to upload stuff to google cloud
from google.cloud import storage


# use this to import stuff from other python files
import importlib.util

file_path = '/Users/shalevwiden/Downloads/Coding_Files/Python/BeautifulSoup_Library/college_course_scraping/theassetcontainment.py'

spec = importlib.util.spec_from_file_location("config", file_path)
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)

theasset=config.theasset
# you can also assign a function

# the asset is important here because it contains the name of every degree in it.


class createWebsite:
    def __init__(self,schooldata):
        # this is the assets folder

                # this is the assets folder

# update this later or make it a relative path. 
        self.degreeviewfolderpath='/Users/shalevwiden/Downloads/Projects/degreeview'

        self.schooldata=schooldata
        
        self.schoolnamekey=list(schooldata)[0]
        self.schoolname=schooldata[self.schoolnamekey]        
        self.schoolnameassetfolder=os.path.join(self.degreeviewfolderpath,self.schoolname)


        # this one is fixed 
        # this should work. If not I need to find a mystery

        # -----------New cleaned schoolname and websitefoler stuff --------------
        self.degreeviewwebsite_path='/Users/shalevwiden/Downloads/Projects/degreeviewwebsite'


        self.cleanedschoolname=self.schoolname.replace(' ','').lower()
        self.schoolpage=f'{self.cleanedschoolname}.html'
        # can I have spaces is the question

        self.websiteschoolfolder=os.path.join(self.degreeviewwebsite_path,self.cleanedschoolname)

        self.fullschoolpage=os.path.join(self.websiteschoolfolder,self.schoolpage)


        # footer so I dont have to redefine it multiple times. 

        self.footer=f'''
        <footer>
            <div class="footerleft">
            <div class="links">
                <a href="about">About</a>

                <a href="Home">Home</a>
            </div>
            <p id="statement">DegreeView 2025</p>
            </div>

            <div class="footerright">
            <img
                id="smalllogo"
                src="testingassets/minilogo.png"
                alt="smalldegreeviewlogo"
            />
            </div>
            <!--  -->
        </footer>
'''
    def upload_schoolfiles(self):


        '''
        This simply gets all the school files and uploads them to cloud. 
        '''
         
        #  if you want to only upload one legree, just change it so its i range 1 to range 


        def get_school_assetlists():
            
            '''
            Important: these lists contain the paths to the files ON THE LOCAL MACHINE. Not in cloud or on the website. 
            '''
            csvlist=[]
            excellist=[]
            pdflist=[]
            mmdlist=[]
            # os.walk recursively travels everything
            for file in os.listdir(self.schoolnameassetfolder):
                
                    
                    # we neewd the fullpath in the list since thats the way it can be uploaded to google cloud.

                full_path = os.path.join(self.schoolnameassetfolder,file)

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
                bucket = client.bucket('degreeview-ut')
                # bucket list


            #THis is what will be in the url and what the name of the object will be in google cloud storage

                cleaned_object_name=source_file_name.split('/')[-1]        


                # make it so each file has the type. 
                # define upload blob here
               
                if os.path.splitext(source_file_name)[1]=='.csv':
                    uploadblob =f'{self.cleanedschoolname}/csvs/{bucket.blob(cleaned_object_name)}'
                elif os.path.splitext(source_file_name)[1]=='.xlsx':
                    uploadblob =f'{self.cleanedschoolname}/excel-files/{bucket.blob(cleaned_object_name)}'

                elif os.path.splitext(source_file_name)[1]=='.pdf':
                    uploadblob =f'{self.cleanedschoolname}/pdfs/{bucket.blob(cleaned_object_name)}'
                elif os.path.splitext(source_file_name)[1]=='.mmd':
                    uploadblob =f'{self.cleanedschoolname}/mmds/{bucket.blob(cleaned_object_name)}'

                else:
                    uploadblob = bucket.blob(cleaned_object_name)

                # add a check to not do it many times
                if not uploadblob.exists():

                    uploadblob.upload_from_filename(source_file_name)

                    uploadblob.make_public()  # Makes it publicly accessible
                    # can also use blob.make_private()
                else:
                    print(f'{uploadblob.name} already exits, didnt upload\n')


                # use this link on the website to serve the file.
                return uploadblob.public_url

            def loop_through_assets_to_upload():
                csvlist=get_school_assetlists()[0]
                for csv in csvlist:
                    # comment these out depending on which ones I want
                    upload_to_googlecloud(csv)
                    # pass a tuple
                    
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
        for file in os.listdir(self.schoolnameassetfolder):
            
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

    
    def createschoolpages(self):
        '''
        On each school page include the school specific csv/.xlsx (listing all the degrees). Then also include another other school diagrams in the future.
        I need it to be modularized so I can do it school by school. As such, use the asset. 
        '''
        # this ensures other folders arent added
        
        degreenamelist=[]
        cleaneddegreenamelist=[]
        for i in range(1,len(self.schooldata)):
                    
                    key=list(self.schooldata)[i]
                    degreename=key
                    degreename=degreename.replace('/','-').strip()
                    degreenamelist.append(degreename)

                    # clean it for website links


                    degreenamecleaned=degreename.replace(' ','').lower().split('(')
                    degreenamecleaned=degreenamecleaned[0]+"-"+degreenamecleaned[-1]
                    degreenamecleaned=degreenamecleaned.replace(')','')

                    cleaneddegreenamelist.append(degreenamecleaned)

        print(f'\nDegreename list is {degreenamelist}\n')




        # degreename list is already cleaned
        

            
        
        # --------------------------
        schoolinfo=f'Every degree page has 2 csvs, 2 excel files, and a sample semester diagram.\n\
        More files coming in the future.' 

        headhtmlcode=f'''
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{self.schoolname}</title>

    <!-- main stylesheet -->
    <link rel="stylesheet" href="../cssfiles/schoolpage.css" />

    <!-- animation stylesheet -->
    <link rel="stylesheet" href="../cssfiles/animations.css" />
    <!-- Barlow Font -->
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
    href="https://fonts.googleapis.com/css2?family=Barlow:ital,wght@0,400;1,100;1,300;1,900&family=Roboto:ital,wght@0,100..900;1,100..900&display=swap"
    rel="stylesheet"
    />
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

            abovemainsitecode=f'''
<div class="abovemainsite">
    <div class="topnav">
        <nav class="breadcrumbs">
        <ul>
            <li><a href="\\">DegreeView UT</a></li>
            <i class="fa fa-chevron-right"></i>

            <li id="current">{self.schoolname}</li>
        </ul>
        </nav>
        <nav class="homeandabout">
        <ul>
            <li><a href="/">Home</a></li>
            <li><a href="">About</a></li>
            <li><a href="">Stats</a></li>
        </ul>
        </nav>
    </div>
    <div class="schoolnamebox">
        <h1 id="schoolnametitle">{self.schoolname}</h1>
    </div>
    </div>
'''
            return abovemainsitecode
        

        def make_degreelist_ul():
            degreelist_ul_element_content=f''''''
            for degreename, cleaneddegreename in zip(degreenamelist,cleaneddegreenamelist):
                
                displaydegreename=degreename.replace("-","/").strip().split('(')

                degreenamepage=f'{cleaneddegreename}.html\n'

                displaydegreename=displaydegreename[0]+f'({displaydegreename[-1]}'

                degreelist_ul_element_content+=f'''<li class="degreelink"><a href="{degreenamepage}">{displaydegreename}</a>
                <a href="{degreenamepage}"><img class="linksvg" src="../testingassets/Link-17.svg" alt="" /></a>
                </li>'''

            
            degreelist_ul_element=f'''
            <ul>{degreelist_ul_element_content}
            </ul>'''
            return degreelist_ul_element
        def make_mainsitecode():

            


            csv_incloudlist=self.get_school_assetcloudpaths_lists()[0]
            # get first, and only, item from the list
            schooldegreescsvlink=csv_incloudlist[0]
            print(f'School Degrees CSV is {schooldegreescsvlink}\n')

            leftcontentcode=f'''
        <div class="leftcontent">
        <div class="filescontainer" id="csvcontainer">
        <h3>CSV Files</h3>
        <ul>
            <li>
            <div class="linkbox">
                <p>Degrees CSV</p>

                <p>
                <!-- download attribute means they will download it -->
                Download:&nbsp;&nbsp;<a
                    href="{schooldegreescsvlink}"
                    download
                    ><i class="fa-solid fa-arrow-up-from-bracket"></i
                ></a>
                </p>
            </div>
            </li>
        </ul>
        </div>
    </div>
        '''
            

            degreelist_ul_element=make_degreelist_ul()


            rightcontentcode=f'''        <div class="rightcontent">
<div class="degreelistheaderbox">
        <h3 id="degreelistheader">School Name degrees</h3>
        </div>
        <!-- Contains links to every degreepage -->
        <div class="degreelistbox">{degreelist_ul_element}</div>
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

            undermainsite=f'''
            <div class="undermainsite">
            <!-- this can be empty and like 20 px tall just to take up space, and be used for something in the future
                -->
            <div class="visuals">
                <h3 id="displayeditemname">CSV Visuals here</h3>
            </div>
            </div>
'''
            bodyhtmlcode=f'''
            <div class="sitecontainer">
            {abovemainsitecode}
            {mainsitecode}
            {undermainsite}
            {self.footer}
            <!-- Hover Script -->
            <script src="../javascript_files/headingcolorchange.js"></script>


            </div>

            '''
            return bodyhtmlcode
        
        def makefullhtmlcode():

            bodyhtmlcode=makebodyhtmlcode()

            fullhtmlcode=f'''
                <!DOCTYPE html>
                <html lang="en">
                {headhtmlcode}
                <body>
                {bodyhtmlcode}\n
                </body>
                </html>'''
            
            if not os.path.exists(self.websiteschoolfolder):
                os.mkdir(self.websiteschoolfolder)

            print(f'Full school page: {self.fullschoolpage}\n')

            with open(self.fullschoolpage,'w') as htmlschoolpage:
                htmlschoolpage.write(fullhtmlcode)
        
        makefullhtmlcode()


# --------------------------------Degree pages now ----------------------------------

    def upload_degree_files(self):

        '''
        Like other functions, this does it by school.
        '''
         
        #  if you want to only upload one legree, just change it so its i range 1 to range 2
        for i in range(1,len(self.schooldata)):
            '''
            Dont need to clean the degreename, since the degreename files(csv, excel,etc) already have clean names.
'''

            key=list(self.schooldata)[i]
            degreename=key
            degreename=degreename.replace('/','-').strip()

            degreenameassetfolder=os.path.join(self.schoolnameassetfolder,degreename)


            def get_assetlists(degreenameassetfolder):
                    

                    csvlist=[]
                    excellist=[]
                    pdflist=[]
                    mmdlist=[]
                    # os.walk recursively travels everything
                    for root, dirs, files in os.walk(degreenameassetfolder):
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


            def upload_to_googlecloud(source_file_name):

                # how to manually change credentials...


                # just change project name here to change where they go.
                # In code, for multiple schools. Dope.
                client = storage.Client(project='degreeview-ut')


                # this should return the email used for google cloud. Its a service email tho

                # yeah the project is the same as the bucket name. In the future change this, as the bucketname is what user sees
                bucket = client.bucket('degreeview-ut')
                # bucket list


            #THis is what will be in the url and what the name of the object will be in google cloud storage

                cleaned_object_name=source_file_name.split('/')[-1]        


                # make it so each file has the type. 
                # define upload blob here
               
                if os.path.splitext(source_file_name)[1]=='.csv':
                    uploadblob =f'{self.cleanedschoolname}/csvs/{bucket.blob(cleaned_object_name)}'
                elif os.path.splitext(source_file_name)[1]=='.xlsx':
                    uploadblob =f'{self.cleanedschoolname}/excel-files/{bucket.blob(cleaned_object_name)}'

                elif os.path.splitext(source_file_name)[1]=='.pdf':
                    uploadblob =f'{self.cleanedschoolname}/pdfs/{bucket.blob(cleaned_object_name)}'
                elif os.path.splitext(source_file_name)[1]=='.mmd':
                    uploadblob =f'{self.cleanedschoolname}/mmds/{bucket.blob(cleaned_object_name)}'

                else:
                    uploadblob = bucket.blob(cleaned_object_name)

                # add a check to not do it many times
                if not uploadblob.exists():

                    uploadblob.upload_from_filename(source_file_name)

                    uploadblob.make_public()  # Makes it publicly accessible
                    # can also use blob.make_private()
                else:
                    print(f'{uploadblob.name} already exits, didnt upload\n')


                # use this link on the website to serve the file.
                return uploadblob.public_url

            def loop_through_assets_to_upload():
                for csv, excelfile,pdf,mmd in zip(get_assetlists(degreenameassetfolder=degreenameassetfolder)):
                    # comment these out depending on which ones I want
                    upload_to_googlecloud(csv)
                    # pass a tuple
                    if not excelfile.startswith(("~$", "$")):
                        upload_to_googlecloud(excelfile)
                    upload_to_googlecloud(pdf)
                    upload_to_googlecloud(mmd)




    def create_degree_pages(self):
        '''
        Hold on this is kinda easy
        '''
        def get_degreename_lists():
            degreenamelist=[]
            cleaneddegreenamelist=[]
            for i in range(1,len(self.schooldata)):
                        
                key=list(self.schooldata)[i]
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
        for degreename, degreenamecleaned in zip(degreenamelist,cleaneddegreenamelist):
            

            # this is the folder for it in degreeview

            degreenameassetfolder=os.path.join(self.schoolnameassetfolder,degreename)
            

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

            titlename=displaydegreename.replace("<br>","")
            
            headhtmlcode=f'''
<head>

    <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Architecture-Architectural Engineering (BArch-BSArchE) Page</title>

        <!-- main stylesheet -->
        <link rel="stylesheet" href="../cssfiles/degreepage2.css" />

        <!-- animation stylesheet -->
        <link rel="stylesheet" href="cssfiles/animations.css" />
        <!-- Barlow Font -->
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
        <link
        href="https://fonts.googleapis.com/css2?family=Barlow:ital,wght@0,600;1,100;1,700;1,900&family=Roboto:ital,wght@0,100..900;1,100..900&display=swap"
        rel="stylesheet"
        />
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
                pass

            def make_mainsitecode():
                pass
            
            def makebodyhtmlcode():
            
                return ''


            def makefullhtmlcode():

                bodyhtmlcode=makebodyhtmlcode()

                fullhtmlcode=f'''
                    <!DOCTYPE html>
                    <html lang="en">
                    {headhtmlcode}
                    <body>
                    {bodyhtmlcode}\n
                    </body>
                    </html>'''

    
                # have to run createschoolpages() first so self.websiteschool folder works
                fulldegreepage=os.path.join(self.websiteschoolfolder,f'{degreenamecleaned}.html')
                with open(fulldegreepage,'w') as htmldegreepage:
                    htmldegreepage.write(fullhtmlcode)
    

# ---------------------END of make degree pages


    def createstatspage(self):
        '''This will create the University Wide stats html page'''
        pass

# -------------END of class -----------------------




def architecure_testing():
     '''Only test here for the first stage'''
     archdata=theasset[0]

     archobject=createWebsite(schooldata=archdata)

     print(f'Full school page: \n{archobject.fullschoolpage}')
     print('\nCreating degree pages now\n\n')
     print(f'Cleaned school name:\n{archobject.cleanedschoolname}\n')
     archobject.createschoolpages()
     csvlist=archobject.get_school_assetcloudpaths_lists()[0]
     print(f'School CSV list is {csvlist}')
     archobject.create_degree_pages()

architecure_testing()


# storage testing

# with architecture teseting
def get_archfiles_lists():
    archpath='/Users/shalevwiden/Downloads/Projects/degreeview/School of Architecture'

    csvlist=[]
    excellist=[]
    pdflist=[]
    mmdlist=[]
    # os.walk recursively travels everything
    for root, dirs, files in os.walk(archpath):
        for file in files:
            
            # we neewd the fullpath in the list since thats the way it can be uploaded to google cloud.

            full_path = os.path.join(root, file)

            if os.path.splitext(file)[1]=='.csv':
                csvlist.append(file)
                # removes those dollar sign excel files. 
            elif os.path.splitext(file)[1]=='.xlsx' and not file.startswith(("~$", "$")):
                excellist.append(full_path)
            elif os.path.splitext(file)[1]=='.pdf':
                pdflist.append(file)
            elif os.path.splitext(file)[1]=='.mmd':
                mmdlist.append(file)

    return excellist

def upload_to_googlecloudtesting(source_file_name):

    # how to manually change credentials...


    # just change project name here to change where they go.
    # In code, for multiple schools. Dope.
    client = storage.Client(project='degreeview-ut')


    # this should return the email used for google cloud. Its a service email tho

    # yeah the project is the same as the bucket name
    bucket = client.bucket('degreeview-ut')
    # bucket list


#THis is what will be in the url and what the name of the object will be in google cloud storage

    cleaned_object_name=source_file_name.split('/')[-1]        


    # make it so each file has the type. 
    if os.path.splitext(source_file_name)[1]=='.csv':
        uploadblob =f'csvs/{bucket.blob(cleaned_object_name)}'
    elif os.path.splitext(source_file_name)[1]=='.xlsx':
        uploadblob =f'excel-files/{bucket.blob(cleaned_object_name)}'

    elif os.path.splitext(source_file_name)[1]=='.pdf':
        uploadblob =f'pdfs/{bucket.blob(cleaned_object_name)}'
    elif os.path.splitext(source_file_name)[1]=='.mmd':
        uploadblob =f'mmds/{bucket.blob(cleaned_object_name)}'

    else:
        uploadblob = bucket.blob(cleaned_object_name)

    # add a check to not do it many times
    if not uploadblob.exists():

        uploadblob.upload_from_filename(source_file_name)

        uploadblob.make_public()  # Makes it publicly accessible
        # can also use blob.make_private()
    else:
         print(f'{uploadblob.name} already exits, didnt upload\n')


    # use this link on the website to serve the file.
    return uploadblob.public_url

excellist=get_archfiles_lists()
print(f'Printing excel stuff now\n\n')
for excelfile in excellist:
     print(excelfile+'\n')
    #  upload_to_googlecloudtesting(source_file_name=excelfile)
     






# def unpacktheasset_into_createSchoolpages(theasset):
#     for schooldict in theasset:
#         websiteobject=createWebsite(schooldata=schooldict)