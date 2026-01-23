from pathlib import Path
import os

import sys

import subprocess
import random

import csv
import time
import json


# use this to upload stuff to google cloud
from google.cloud import storage


# use this to import stuff from other python files
import importlib.util




with open("/Users/shalevwiden/Downloads/Projects/dvwebsitecreation/degreeview_expansion/utd/utdasset.json", "r") as file:
    utdasset = json.load(file)

total=0
for i in utdasset:

    total+=len(i)
print(f'Total:\n{total}')

# you can also assign a function

# the asset is important here because it contains the name of every degree in it.


class createWebsite:
    def __init__(self,schooldata):
        # this is the assets folder

                # this is the assets folder

# update this later or make it a relative path. 
        self.degreeviewfolderpath='/Users/shalevwiden/Downloads/Projects/dvassets/texas/UTD2'

        self.schooldata=schooldata
        
        self.schoolnamekey=list(schooldata)[0]
        self.schoolname=schooldata[self.schoolnamekey]        
        self.schoolfolderpath=os.path.join(self.degreeviewfolderpath,self.schoolname)
        self.degreefolders= [os.path.join(self.schoolfolderpath,folder) for folder in os.listdir(self.schoolfolderpath) 
           if os.path.isdir(os.path.join(self.schoolfolderpath, folder))]


        # this one is fixed 
        # this should work. If not I need to find a mystery

        # -----------New cleaned schoolname and websitefoler stuff --------------
        websitepath='/Users/shalevwiden/Downloads/Projects/utdallas-site'


        self.cleanedschoolname=self.schoolname.replace(' ','').lower()
        self.schoolpage=f'{self.cleanedschoolname}.html'
        # can I have spaces is the question

        self.websiteschoolfolder=os.path.join(websitepath,self.cleanedschoolname)
        

        self.fullschoolpage=os.path.join(self.websiteschoolfolder,self.schoolpage)


        # footer so I dont have to redefine it multiple times. 

        self.footer=f'''
         <footer>
        <div class="footerleft">
          <div class="links">
            <a href="../index.html">About</a>

            <a href="../index.html">Home</a>
          </div>
          <p id="statement">DegreeView 2026</p>
        </div>

        <div class="footerright">
          <img
            id="smalllogo"
            src="../metaassets/minilogo.png"
            alt="smalldegreeviewlogo"
          />
        </div>
      </footer>

'''
        
    def upload_schoolfiles(self):


        '''
        This simply gets all the school files and uploads them to cloud. 
        '''
         
        #  if you want to only upload one legree, just change it so its i range 1 to range 

        print(f'\n\nBeginning Cloud Upload for {self.schoolname} school specific files\n\n') 

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
                bucket = client.bucket('degreeview-ut')
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

        print(f'\n\nEnding Cloud Upload for {self.schoolname} school specific files\n\n') 

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
 
    def createschoolpages(self):
        '''
        On each school page include the school specific csv/.xlsx (listing all the degrees). Then also include another other school diagrams in the future.
        I need it to be modularized so I can do it school by school. As such, use the asset. 
        '''
        # this ensures other folders arent added
        
        degreenamelist=[]
        cleaneddegreenamelist=[]
        for degreefolder in self.degreefolders:
            print(f'Degree folder: \n{degreefolder}\n')
            degreefolderpath=Path(degreefolder)


            degreename=degreefolderpath.name

            
            # this thing here always happens regardless of the 
            degreename=degreename.replace('/','-').strip()

            
            degreenamecleaned=degreename.replace(' ','').lower().split('(')
            degreenamecleaned=degreenamecleaned[0]+"-"+degreenamecleaned[-1]
            degreenamecleaned=degreenamecleaned.replace(')','')
            
 
            degreenamelist.append(degreename)
            cleaneddegreenamelist.append(degreenamecleaned)

        print(f'\nDegreename list is {degreenamelist}\n')




        # degreename list is already cleaned
        

            
        
        # --------------------------
        schoolinfo=f'Every degree page has 2 csvs, 2 excel files, and a sample semester diagram.\n\
        More files coming in the future.' 

        headhtmlcode=f'''
<head>

    <meta
        name="description"
        content="{self.schoolname} Degrees and Data"
        />

     <meta
      name="keywords"
      content="degree, major, UT Austin, degreeview, course diagrams, course excel files, degree stats, {self.schoolname}"
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

    <title>{self.schoolname} Page - DegreeView</title>

    <!-- main stylesheet -->
    <link rel="stylesheet" href="../static/css/utdschoolpage.css" />

    <!-- animation stylesheet -->
    <link rel="stylesheet" href="../static/css/animations.css" />
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

            abovemainsitecode=f'''
<div class="abovemainsite">
    <div class="topnav">
        <nav class="breadcrumbs">
        <ul>
            <li><a href="../index.html">DegreeView UTD</a></li>
            <i class="fa fa-chevron-right"></i>

            <li id="current">{self.schoolname}</li>
        </ul>
        </nav>
        <nav class="homeandabout">
        <ul>
            
              <li><a href="../index.html">Home</a></li>
              <li><a href="../about.html">About</a></li>
              <li><a href="../utd-stats.html">Stats</a></li>
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
                <a href="{degreenamepage}"><img class="linksvg" src="../metaassets/Link-17.svg" alt="" /></a>
                </li>'''

            
            degreelist_ul_element=f'''
            <ul>{degreelist_ul_element_content}
            </ul>'''
            return degreelist_ul_element
        def make_mainsitecode():

            
            '''This gets the asset cloud list. Since theres only 1 csv currently, we good.'''

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
        <h3 id="degreelistheader">{self.schoolname} Degrees</h3>
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

            undermainsitecode=f'''
            <div class="undermainsite">
            <!-- this can be empty and like 20 px tall just to take up space, and be used for something in the future
                -->
            s
            </div>
'''
            bodyhtmlcode=f'''
            <body>

            <div class="sitecontainer">
            {abovemainsitecode}
            {mainsitecode}
            {undermainsitecode}
            {self.footer}
            <!-- Hover Script -->
            <script src="../static/js/utdheadingcolorchange.js"></script>


            </div>
            </body>

            '''
            return bodyhtmlcode
        
        def makefullhtmlcode():

            bodyhtmlcode=makebodyhtmlcode()

            fullhtmlcode=f'''
                <!DOCTYPE html>
                <html lang="en">
                {headhtmlcode}
                {bodyhtmlcode}\n
              
                </html>'''
            
            if not os.path.exists(self.websiteschoolfolder):
                os.mkdir(self.websiteschoolfolder)

            print(f'Full school page: {self.fullschoolpage}\n')

            with open(self.fullschoolpage,'w') as htmlschoolpage:
                htmlschoolpage.write(fullhtmlcode)
        
        makefullhtmlcode()
        return 0
# --------------------------------Degree pages now ----------------------------------

    def upload_degree_files(self):

        '''
        Like other functions, this does it by school.


        '''

        print(f'\n\nBeginning Cloud Upload for {self.schoolname} degreefiles\n\n') 
        #  if you want to only upload one legree, just change it so its i range 1 to range 2
        for i in range(1,len(self.schooldata)):
            '''
            Dont need to clean the degreename, since the degreename files(csv, excel,etc) already have clean names.
'''

            key=list(self.schooldata)[i]
            degreename=key
            degreename=degreename.replace('/','-').strip()

            degreenameassetfolder=os.path.join(self.schoolfolderpath,degreename)


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


                #This is what will be in the url and what the name of the object will be in google cloud storage

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

                '''
                csvlist=get_assetlists(degreenameassetfolder=degreenameassetfolder)[0]
                excellist=get_assetlists(degreenameassetfolder=degreenameassetfolder)[1]
                pdflist=get_assetlists(degreenameassetfolder=degreenameassetfolder)[2]

                # majorcoursescsv=[csv for csv in csvlist if "courses" in csv][0]

                # mmds currently not needing to be uplaoded.
                

                for pdffile in pdflist:
                   
                    upload_to_googlecloud(pdffile)
                    print(f'Uploaded {pdffile} to cloud\n')

                   
                   
                   

        
                
                others=True
                if others:
                    for csvfile in csvlist:
                        # comment these out depending on which ones I want
                        upload_to_googlecloud(csvfile)
                        print(f'Uploaded {csvfile} to cloud\n')

                    for excelfile in excellist:
                        if not excelfile.startswith(("~$", "$")):
                            upload_to_googlecloud(excelfile)
                            print(f'Uploaded {excelfile} to cloud\n')

            # this one actually uploads everything
            loop_through_assets_to_upload()

        print(f'\n\nEnding Cloud Upload for {self.schoolname} degreefiles \n\n\n\n')
        return 0
                    
                   
    def create_degree_pages(self):
        '''
        this is hard af
        '''
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
            
            renderedcsvurl=f'{degreenamecleaned}-rendered-csv.html'

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
        <title>{displaydegreename_nobr} Page - DegreeView</title>

        
    <!-- main stylesheet -->
    <link rel="stylesheet" href="../static/css/utddegreepage.css" />

    <!-- animation stylesheet -->
    <link rel="stylesheet" href="../static/css/animations.css" />


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

              <li><a href="{self.schoolpage}">{self.schoolname}</a></li>
              <i class="fa fa-chevron-right"></i>

              <li id="current">
                {displaydegreename_nobr}
              </li>
            </ul>
          </nav>
          <nav class="homeandabout">
            <ul>
              
              <li><a href="../index.html">Home</a></li>
              <li><a href="../about.html">About</a></li>
              <li><a href="../utd-stats.html">Stats</a></li>
            </ul>
          </nav>
        </div>
        <div class="degreenamebox">
          <h1 id="degreenametitle">
           {displaydegreename}
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
                csvlist=get_degree_assetcloudpaths_lists(degreenameassetfolder=degreenameassetfolder)[0]
                print(f'CSV list: {csvlist}')
                semesterlayoutcsv=[csv for csv in csvlist if "semestercsvfile" in csv][0]

                # get excel links
                excellist=get_degree_assetcloudpaths_lists(degreenameassetfolder=degreenameassetfolder)[1]

                lighttheme_excel=[file for file in excellist if "dark" not in file][0]
                darktheme_excel=[file for file in excellist if "semesterfile" in file and "dark" in file][0]

                # get pdf links
                pdflist=get_degree_assetcloudpaths_lists(degreenameassetfolder=degreenameassetfolder)[2]


                semesterlayoutpdf=[pdffile for pdffile in pdflist if "semesterlayout" in pdffile and "emptynodes" not in pdffile][0]
                emptynodespdf=[pdffile for pdffile in pdflist if "emptynodes" in pdffile][0]


                
                # I  dont put mmds in the website, for now...
                mmdlist=get_degree_assetcloudpaths_lists(degreenameassetfolder=degreenameassetfolder)[3]


                def makeleftcontentcode():
                    '''Using the links just received above, now link them in the left content code in the website'''

                    

                    leftcontentcode=f'''
                    <div class="leftcontent">

                    <div class="filescontainer" id="excelcontainer">
                        <div class="filesname">
                            <h3>Excel (.xlsx) Files</h3>
                            <i class="fa-regular fa-file-excel"></i>
                        </div>

                        <ul>
                            <li>
                            <div class="linkbox">
                                <p>Sample Semester Layout Light Theme</p>
                                <p>
                                <!-- download attribute means they will download it -->
                                Download:&nbsp;&nbsp;<a
                                    href="{lighttheme_excel}"
                                    download
                                    ><i class="fa-solid fa-arrow-up-from-bracket"></i
                                ></a>
                                </p>
                            </div>
                            </li>
                            <!--  -->
                            <li>
                            <div class="linkbox">
                                <p>Sample Semester Layout Dark Theme</p>
                                <p>
                                <!-- download attribute means they will download it -->
                                Download:&nbsp;&nbsp;<a
                                    href="{darktheme_excel}"
                                    download
                                    ><i class="fa-solid fa-arrow-up-from-bracket"></i
                                ></a>
                                </p>
                            </div>
                            </li>
                            
                        </ul>
                        </div>
                        <!-- files container is per file type. linkbox is per individiual link -->
                        <div class="filescontainer" id="pdfcontainer">
                        <div class="filesname">
                            <h3>PDF Files</h3>
                            <i class="fa-regular fa-file-pdf"></i>
                        </div>

                        <ul>
                            <!-- put the linkboxes in li tags for organization and readability -->
                            <li>
                            <div class="linkbox">
                                <p>Sample Semester PDF</p>

                                <p>
                                View:&nbsp;&nbsp;
                                <a href="{semesterlayoutpdf}" target="_blank"
                                    ><i class="fa-regular fa-eye"></i
                                ></a>
                                </p>
                                <p>
                                <!-- download attribute means they will download it -->
                                Download:&nbsp;&nbsp;<a
                                    href="{semesterlayoutpdf}"
                                    download
                                    ><i class="fa-solid fa-arrow-up-from-bracket"></i
                                ></a>
                                </p>
                            </div>
                            </li>

                            <li>
                            <div class="linkbox">
                                <p>Sample Semester PDF Empty Nodes</p>
                                <p>
                                View:&nbsp;&nbsp;
                                <a href="{emptynodespdf}" target="_blank"
                                    ><i class="fa-regular fa-eye"></i
                                ></a>
                                </p>
                                <p>
                                <!-- download attribute means they will download it -->
                                Download:&nbsp;&nbsp;<a
                                    href="{emptynodespdf}"
                                    download
                                    ><i class="fa-solid fa-arrow-up-from-bracket"></i
                                ></a>
                                </p>
                            </div>
                            </li>
                            <!-- dolphin pdf -->
             
              
                        </ul>
                        </div>

                        <div class="filescontainer" id="csvcontainer">
                        <div class="filesname">
                            <h3>CSV Files</h3>
                            <i class="fa-regular fa-file"></i>
                        </div>

                        <ul>
                            

                            <li>
                            <div class="linkbox">
                                <p>Sample Semester Layout CSV</p>

                                 <p>
                    View:&nbsp;&nbsp;
                    <a
                      href="{renderedcsvurl}"
                      target="_self"
                      ><img class="linksvg" src="../metaassets/Link-17.svg" alt="" />
                    </a>
                                          <!-- link icon above--> 

                  </p>
                                <p>
                                <!-- download attribute means they will download it -->
                                Download:&nbsp;&nbsp;<a href="{semesterlayoutcsv}" download
                                    ><i class="fa-solid fa-arrow-up-from-bracket"></i
                                ></a>
                                </p>
                            </div>
                            </li>
                        </ul>
                        </div>
                        </div>
'''
                    return leftcontentcode
                    
                def makerightcontentcode():
                    '''
                    The right content displays a pdf, is the "displayedpdf" iframe. THis can be used to showcase a weekly pdf or so. 
                    '''

                    rightcontentcode=f'''
                    <div class="rightcontent">
                     <div class="displayedpdfnamebox">
            <h3 id="displayedpdfname">Sample Semester Layout PDF</h3>
          </div>
          <div class="visuals">
            <iframe
              class="displayedpdf"
              src="{semesterlayoutpdf}"
              frameborder="0"
              width="90%"
              height="1000px"
            ></iframe>
          </div></div>
'''
                    return rightcontentcode
                # end makerightcontentcodefunction()
                
                leftcontentcode=makeleftcontentcode()
                rightcontentcode=makerightcontentcode()

                mainsitecode=f'''<div class="mainsite">
                {leftcontentcode}
                {rightcontentcode}
                </div>'''
                return mainsitecode 
            
            def makebodyhtmlcode():
                abovemainsitecode=make_abovemainsitecode()
                mainsitecode=make_mainsitecode()


                csvlist=get_degree_assetcloudpaths_lists(degreenameassetfolder=degreenameassetfolder)[0]


                undermainsitecode=f'''
 <div class="undermainsite">
        
      </div>

'''

                bodyhtmlcode=f'''                    
                <body>       
                <div class="sitecontainer">
                {abovemainsitecode}
                {mainsitecode}
                {undermainsitecode}
                {self.footer}

                

                 <script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>

                 <script src="../javascript_files/degreecsvrendered_samefile.js"></script>


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


            def makefullhtmlcode():

                bodyhtmlcode=makebodyhtmlcode()

                fullhtmlcode=f'''
                    <!DOCTYPE html>
                    <html lang="en">
                    {headhtmlcode}\n
                    {bodyhtmlcode}\n
                    
                    </html>'''

    
                # have to run createschoolpages() first so self.websiteschool folder works
                fulldegreepage=os.path.join(self.websiteschoolfolder,f'{degreenamecleaned}.html')
                with open(fulldegreepage,'w') as htmldegreepage:
                    htmldegreepage.write(fullhtmlcode)
                print(f'\n Made {fulldegreepage} as part of making degreepages\n')

            makefullhtmlcode()
        return 0

# ---------------------END of make rendered degree pages

    def create_renderedcsv_pages(self):
        '''
        These are the rendered csvs in a diferent HTML page
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

              <li><a href="{self.schoolpage}">{self.schoolname}</a></li>
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
              <li><a href="../about.html">About</a></li>
              <li><a href="../utd-stats.html">Stats</a></li>
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

                      <script src="../static/js/degreecsvrendered.js"></script>

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
    def make_alldegrees_list(self):
        '''
        This function returns two lists, of degreepages, and degreedata. Its later called in make_alldegreesfile().
        This is to make alldegrees.txt. 
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

        # now that we got a list of cleaned degreenames, loop through that list

        degreepage_list=[]
        degreename_data=[]
        for degreename,degreenamecleaned in zip(degreenamelist, cleaneddegreenamelist):
            fulldegreepage=os.path.join(self.cleanedschoolname,f'{degreenamecleaned}.html')

            makerendered=True
            if makerendered:
                fulldegreepage=os.path.join(self.cleanedschoolname,f'{degreenamecleaned}-rendered-csv.html')

            degreepage_list.append(fulldegreepage)
            
            displaydegreename=degreename.replace("-","/").strip().split('(')

            displaydegreename=displaydegreename[0]+f'({displaydegreename[-1]}'
            

            # using this we can figure out longest and shortest degreename. 
            degreename_data.append(displaydegreename)
        return degreepage_list, degreename_data


# -------------END of class -----------------------


def make_alldegreesfile():

    entireschool_degreepagelist=[]

    for schooldict in theasset:
        alldegreesobject=createWebsite(schooldata=schooldict)
        alldegreesobject_degreepagelist=alldegreesobject.make_alldegrees_list()[0]

        print(f'\n{alldegreesobject.schoolname} degreepage_list:\n{alldegreesobject_degreepagelist} \n\n')
        
        for eachpage in alldegreesobject_degreepagelist:
            # do this to avoid making a list of lists. This way its just a nice, giant, list
            entireschool_degreepagelist.append(eachpage)

    with open(f"{os.path.abspath("alldegrees.txt")}",'w') as alldegreesfile:
        alldegreesfile.write(f'[')

        for degreepageindex in range(len(entireschool_degreepagelist)):
            if degreepageindex==len(entireschool_degreepagelist)-1:
                alldegreesfile.write(f'"{entireschool_degreepagelist[degreepageindex]}"')
            else:
                alldegreesfile.write(f'"{entireschool_degreepagelist[degreepageindex]}",')

        alldegreesfile.write(f']')

# make_alldegreesfile()

# architecure_testing()

def get_all_schools(theasset):
    # finish this after dinner
    '''
    This generates a schoolist based on the asset. Then will generate a list of li's to go in an index.html
    '''
    schoolist=[]
    for schooldict in theasset:
        schoolname=schooldict[list(schooldict)[0]]
        schoolist.append(schoolname)
    print('School list:')
    for schoolindex in range(len(schoolist)):
        

        schoolnamecleaned=schoolist[schoolindex].replace(' ','').lower()
        schoolpage=f'{schoolnamecleaned}.html'

        websiteschoolpagelink=os.path.join(schoolnamecleaned,schoolpage)
        
        print(f' <li class="schoolist-column"> <a href="{websiteschoolpagelink}"><div class="schoolnamediv">{schoolist[schoolindex]}</div></a></li>')
       
            
        

# storage te
     



def basstesting():
    bassdict=utdasset[0]
    bassobject=createWebsite(schooldata=bassdict)
    bassobject.createschoolpages()
    # bassobject.create_degree_pages()
    bassobject.create_renderedcsv_pages()
    
# basstesting()


def main():
    for schooldict in utdasset[0:]:
        print(schooldict[list(schooldict)[0]])
        websiteobject=createWebsite(schooldata=schooldict)
        print(f'starting for {websiteobject.schoolname}\n\n\n')
        
        # websiteobject.upload_degree_files()
        websiteobject.createschoolpages()
        websiteobject.create_degree_pages()
        websiteobject.create_renderedcsv_pages()
     
        
if __name__=="__main__":
    main()