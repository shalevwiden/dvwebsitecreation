import os
from google.cloud import storage

'''
July 17th

In the future, use this to count asset files in diferent schools folders. Ie for UT Austin, Harvard, etc. 
'''
degreeviewfolderpath='/Users/shalevwiden/Downloads/Projects/degreeview'

def count_files(folderpath):

    csvcount=0
    excelcount=0
    pdfcount=0
    mmdcount=0
    # os.walk recursively travels everything
    for root, dirs, files in os.walk(folderpath):
        for file in files:
            if os.path.splitext(file)[1]=='.csv':
                csvcount += 1
            elif os.path.splitext(file)[1]=='.xlsx':
                excelcount+=1
            elif os.path.splitext(file)[1]=='.pdf':
                pdfcount+=1
            elif os.path.splitext(file)[1]=='.mmd':
                mmdcount+=1

    print(f'CSV file count {csvcount}')
    print(f'Excel file count {excelcount}')
    print(f'pdf file count {pdfcount}')
    print(f'mmd file count {mmdcount}')
    print(f'\nTotal file count {mmdcount+excelcount+pdfcount+csvcount}')

count_files(degreeviewfolderpath)

def list_bucket_files():
    '''
    This uses a class A operation. Cheap, but worth knowing.

    '''
    client = storage.Client(project='degreeview-ut')

    bucket='ut-degreeview'
    filesinbucket = bucket.list_blobs()

def delete_bucketitems(filetype):
    '''
    File type is like the subfolder. 'excel-files' for example. 
    '''
    client = storage.Client(project='degreeview-ut')

    bucket='ut-degreeview'
    blobfiles= bucket.list_blobs(prefix=filetype)

    for blob in blobfiles:
        print(f"Deleting: {blob.name}")
        blob.delete()


def getserviceemail():
    client = storage.Client(project='degreeview-ut')


    # this should return the email used for google cloud. Its a service email tho
    print(client.get_service_account_email())