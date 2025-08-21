
import subprocess
import os
from google.cloud import storage

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

def deletebasedon_subfolder(subfoldername):

    bucket = "your-bucket"
    

    command = [
        "gsutil",
        "rm",
        f"gs://{bucket}/{subfoldername}**"
    ]

    try:
        subprocess.run(command, check=True)
        print("Delete successful.")
    except subprocess.CalledProcessError as e:
        print(f"Error deleting objects: {e}")


def getserviceemail():
    client = storage.Client(project='degreeview-ut')


    # this should return the email used for google cloud. Its a service email tho
    print(client.get_service_account_email())