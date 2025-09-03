import subprocess
import os
from google.cloud import storage

'''
July 17th

In the future, use this to count asset files in diferent schools folders. Ie for UT Austin, Harvard, etc. 
'''

utcoursespath='/Users/shalevwiden/Downloads/Projects/dvassets/texas/UT_courses'
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
    totalfilecount=pdfcount+excelcount+csvcount
    print(f'\nTotal file count in {folderpath},nonmmd {excelcount+pdfcount+csvcount}\n')
    return totalfilecount
count_files(folderpath=utcoursespath)


def calculate_entire_dv_files():
    pathdict={"utassetspath":'/Users/shalevwiden/Downloads/Projects/originaldegreeview',"utcoursespath":'/Users/shalevwiden/Downloads/Projects/dvassets/texas/UT_courses',
    "utdcoursespath":'/Users/shalevwiden/Downloads/Projects/dvassets/texas/UTD_courses',
    "utsacoursespath":'/Users/shalevwiden/Downloads/Projects/dvassets/texas/UTSA',
    "utdassetspath":'/Users/shalevwiden/Downloads/Projects/dvassets/texas/UTD2'}

    megatotal=0
    for i in pathdict:
        
        totalcount=count_files(pathdict[i])
        megatotal+=totalcount
    print(megatotal)

