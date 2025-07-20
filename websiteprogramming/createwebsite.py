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
        self.assetschoolfolderpath=os.path.join(self.degreeviewfolderpath,self.schoolname)


        # this one is fixed 
        # this should work. If not I need to find a mystery

        # -----------New cleaned schoolname and websitefoler stuff --------------
        self.degreeviewwebsite_path='/Users/shalevwiden/Downloads/Projects/degreeviewwebsite'


        cleanedschoolname=self.schoolname.replace(' ','').lower()
        self.schoolpage=f'{cleanedschoolname}.html'
        # can I have spaces is the question

        self.websiteschoolfolder=os.path.join(self.degreeviewwebsite_path,cleanedschoolname)

        self.fullschoolpage=os.path.join(self.websiteschoolfolder,self.schoolpage)

        self.footer=''''''

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
        for degreename, cleaneddegreename in zip(degreenamelist,cleaneddegreenamelist):
            

            
            
            # --------------------------
            schoolinfo=f'Every degree page has 2 csvs, 2 excel files, and a sample semester diagram.\n\
            More files coming in the future.' 

            headhtmlcode=f'''
    <!DOCTYPE html>
    <html lang="en">
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
            def make_mainsitecode():

                displaydegreename=degreename.replace("-","/").strip().split('(')
                displaydegreename=displaydegreename[0]+'<br>'+f'({displaydegreename[-1]}'

                degreenamepage=f'{cleaneddegreename}.html\n'

                
                ul_element_content+=f'<li class="degreelink"><a href="{degreenamepage}">{displaydegreename}</a><img class="linksvg" src="testingassets/Link-17.svg" alt="" /></li>'

            ul_element=f'''
                <ul>{ul_element_content}
                </ul>'''
                mainsitecode=f''''''
                return mainsitecode
        
            def makebodyhtmlcode():
                abovemainsitecode=make_abovemainsitecode()

                bodyhtmlcode=f'''
                <div class="sitecontainer">
                {abovemainsitecode}
                </div>
    '''
            
            def makefullhtmlcode():

                fullhtmlcode=f'''
        <!DOCTYPE html>
        <html lang="en">
        {headhtmlcode}
        <body>
        {bodyhtmlcode}\n
        {self.footer}
        </body>
        </html>'''
                
                if not os.path.exists(self.websiteschoolfolder):
                    os.mkdir(self.websiteschoolfolder)

                print(f'Full school page: {self.fullschoolpage}\n')

                with open(self.fullschoolpage,'w') as htmlschoolpage:
                    htmlschoolpage.write(fullhtmlcode)


# --------------------------------Degree pages now ----------------------------------

    def upload_files(self):

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

            degreenameassetfolder=os.path.join(self.assetschoolfolderpath,degreename)


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

            degreenameassetfolder=os.path.join(self.assetschoolfolderpath,degreename)
            

            # get file types

            def get_assetcloudpaths_lists(degreenameassetfolder):
                
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
                            objectname_incloud=f'csvs/{file}'
                            googlecloudpath=f'https://storage.googleapis.com/degreeview-ut/{objectname_incloud}'

                            csv_path_list.append(googlecloudpath)
                            # removes those dollar sign excel files. 
                        elif os.path.splitext(file)[1]=='.xlsx' and not file.startswith(("~$", "$")):

                            objectname_incloud=f'excel-files/{file}'
                            googlecloudpath=f'https://storage.googleapis.com/degreeview-ut/{objectname_incloud}'
                        
                            excel_path_list.append(googlecloudpath)
                        elif os.path.splitext(file)[1]=='.pdf':
                        
                            objectname_incloud=f'pdfs/{file}'
                            googlecloudpath=f'https://storage.googleapis.com/degreeview-ut/{objectname_incloud}'
                        
                            pdf_path_list.append(googlecloudpath)
                        elif os.path.splitext(file)[1]=='.mmd':
                        
                            objectname_incloud=f'mmds/{file}'
                            googlecloudpath=f'https://storage.googleapis.com/degreeview-ut/{objectname_incloud}'
                            mmd_path_list.append(googlecloudpath)

                return [csv_path_list,excel_path_list,pdf_path_list,mmd_path_list]
            
            # finish the rest of them when its time to upload.
            csvlist=get_assetcloudpaths_lists(degreenameassetfolder=degreenameassetfolder)[0]
            print(f'\nCSV LIst is {csvlist}')

                    
            
                              
                         
            
            # then I'll do upload to cloud, excel list, csv list, mermaid list, etc
            
            

            def make_degreewebsite_page():

                displaydegreename=degreename.replace("-","/").strip().split('(')
                displaydegreename=displaydegreename[0]+'<br>'+f'({displaydegreename[-1]}'

                titlename=displaydegreename.replace("<br>","")

                bodyhtmlcode=f'''
                <h1 id="degreenametitle">{displaydegreename}</h1>\n
    '''

                
                fullhtmlcode=f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>{titlename} Page</title>
    </head>
    <body>{bodyhtmlcode}  \n
    {self.footer}
    </body>
    </html>
    '''         
                # have to run createschoolpages() first so self.websiteschool folder works
                fulldegreepage=os.path.join(self.websiteschoolfolder,f'{degreenamecleaned}.html')
                with open(fulldegreepage,'w') as htmldegreepage:
                    htmldegreepage.write(fullhtmlcode)
        
            make_degreewebsite_page()

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
     archobject.createschoolpages()
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
print(f'Excel list: {excellist}')
for excelfile in excellist:
     print(excelfile+'\n')
    #  upload_to_googlecloudtesting(source_file_name=excelfile)
     






# def unpacktheasset_into_createSchoolpages(theasset):
#     for schooldict in theasset:
#         websiteobject=createWebsite(schooldata=schooldict)