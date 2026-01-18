# call the catalogData class
# for all schools

class createData:
    def __init__(self):
        # this is the main folder where all the Assets will go
        self.assetspath='/Users/shalevwiden/Downloads/Projects/dvassets'

        self.universityuldatapath=''
    def buildspecs(self, asset_folder_path,jsondatapath,universityname,cloudbucketpath,websitefolder, schoolabrv):

        
        return {"asset_folder_path": asset_folder_path,
    "jsondatapath": jsondatapath,
    "universityname": universityname,
    "cloudbucketpath": cloudbucketpath,
    "websitefolder": websitefolder,
    "schoolabrv":schoolabrv}

    def schoolcontainingfunc(self):
        '''
        This function will call all of the school objects and their methods.
        Itll be a big one.
        Might wanna divide it up later.

        '''
        def texas():
            '''
            This contains all the schools within texas
            '''
            def ut():
                # I need need to standardize the location of all of this stuff
                ut_specs=self.buildspecs("/Users/shalevwiden/Downloads/Projects/dvassets/texas/UT_courses",
                    "/Users/shalevwiden/Downloads/Coding_Files/Python/BeautifulSoup_Library/degreeview_expansion/ut_courses/utjson.json",
                    "The University of Texas at Austin"
                    ,"https://storage.googleapis.com/utcourses",
                    "/Users/shalevwiden/Downloads/Projects/testsite/ut",
                    "UT")
            def rice():
                rice_specs=self.buildspecs("/Users/shalevwiden/Downloads/Projects/dvassets/texas/UT_courses",
                    "/Users/shalevwiden/Downloads/Coding_Files/Python/BeautifulSoup_Library/degreeview_expansion/ut_courses/utjson.json",
                    "The University of Texas at Austin"
                    ,"https://storage.googleapis.com/utcourses",
                    "/Users/shalevwiden/Downloads/Projects/testsite/ut",
                    "UT")

def main():
    createdata=createData()

    createdata.schoolcontainingfunc()

if __name__=="__main__":
    main()