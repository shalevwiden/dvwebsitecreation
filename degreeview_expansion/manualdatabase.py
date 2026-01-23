import sqlite3
import os
import json

jsonpath='stanford/manual.json'

with open(jsonpath) as f:
    manualjson=json.load(f)

def get_tablename():
        '''
        This gets the tablename in the department databases
        '''
        tablename=f'coursestable'
        return tablename
def database_logic():
# its a little different from the database name, use underscore instead of hyphen
    '''
    There was a tricky problem with the seconds...thats why I used SECOND
    '''

    

    databasepath='/Users/shalevwiden/Downloads/Projects/dvwebsitecreation/degreeview_expansion/stanford/assets/P/Psychiatry and Behavioral Sciences/psychiatryandbehavioralsciences-database.db'

    # start fresh

    if os.path.exists(databasepath):
        os.remove(databasepath)
    # hyphens and commas not allowed in tablename

    tablename=get_tablename()

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

        departmentdata=manualjson
        if departmentdata is None:
            print('departmentdata is none, ending')
            return
        for coursename in departmentdata:
            coursecode,coursehours,classification=departmentdata[coursename]
            # established second and third in scrape courses
            coursename=coursename.replace('SECOND','').replace('THIRD','')
            cursor.execute(f'INSERT INTO {tablename} (coursename, coursecode, coursehours, classification) values(?,?,?,?);',
                        [coursename,coursecode,coursehours,classification])
                    


                
        # commit to the database 
        conn.commit()
database_logic()
