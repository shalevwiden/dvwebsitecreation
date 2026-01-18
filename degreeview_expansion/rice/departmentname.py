
'''
This is for UT Austin department names every school might be a little different.

Use this class in catalogdata.py and createuniversity.py


'''

# the departmentname itself is the name of the folders.
# IMPORTANT - the name of the folders have slashes removed by default
# departmentname=departmentname.replace('/','_')


class DepartmentName:
   
    def get_sanitized_departmentname(self,departmentname):
        return departmentname.replace('/','_')

    def get_departmentnamecleaned(self, departmentname):

        departmentnamecleaned=departmentname.replace('/','-')




        departmentnamecleaned=departmentnamecleaned.replace(' ','').lower()
        departmentnamecleaned=departmentnamecleaned.replace(',','-').lower()

        return departmentnamecleaned

    def get_display_departmentname(self, departmentname):
        '''
        This one actually doesnt use departmentname cleaned, because capitalization will be displayed
        
        
        '''

        displaydepartmentname=departmentname.replace('_','/')
        # the splitpoint is important, for UT its a "-"
        displaydepartmentname=displaydepartmentname.strip().split('-')
        code=displaydepartmentname[0].strip()
        departmentnamehalf=displaydepartmentname[-1].strip()

        # so in this case I put display department name in parenthesis
        # I may remove
        displaydepartmentname=f'({code}) - {departmentnamehalf}'
        return displaydepartmentname

    def get_departmentnamehalf(self, departmentname):
        displaydepartmentname=departmentname.replace('_','/')
        # the splitpoint is important, for UT its a "-"
        displaydepartmentname=displaydepartmentname.strip().split('-')
        
        departmentnamehalf=displaydepartmentname[-1].strip()
        return departmentnamehalf

    def get_departmentcode(self, departmentname):
        displaydepartmentname=departmentname.replace('_','/')
        # the splitpoint is important, for UT its a "-"
        displaydepartmentname=displaydepartmentname.strip().split('-')
        
        code=displaydepartmentname[0].strip()
        return code

def main():
    '''
    Use this function to test when generation
    '''
    departmentname="ACF - Actuarial Foundations"

    dept = DepartmentName()

    departmentnamecleaned=dept.get_departmentnamecleaned(departmentname)
    display_departmentname=dept.get_display_departmentname(departmentname)
    departmentnamehalf=dept.get_departmentnamehalf(departmentname)
    code=dept.get_departmentcode(departmentname)

    print(departmentname)
    print(departmentnamecleaned)
    print(display_departmentname)
    print(departmentnamehalf)
    print(code)

if __name__ == "__main__":
    main()
