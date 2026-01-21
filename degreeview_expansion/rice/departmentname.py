
'''
The departmentname.py for Rice.

'''

# the departmentname itself is the name of the folders.
# IMPORTANT - the name of the folders have slashes removed by default
# departmentname=departmentname.replace('/','_')


class DepartmentName:
   
    def get_sanitized_departmentname(self,departmentname):
        
        # removing slashes is important
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

        departmentname=departmentname.replace('_','/')
        # the splitpoint is important, for UT its a "-"
        
        departmentnamehalf,code=departmentname.split('(')
        code=''.join(c for c in code if c.isalpha() or c.isspace())
        departmentnamehalf=departmentnamehalf.strip()

        # so in this case I put display department name in parenthesis
        # I may remove
        displaydepartmentname=f'{code} - {departmentnamehalf}'
        return displaydepartmentname

    def get_departmentnamehalf(self, departmentname):
        
        departmentname=departmentname.replace('_','/')
        # the splitpoint is important, for UT its a "-"
        
        departmentnamehalf,code=departmentname.split('(')
        code=''.join(c for c in code if c.isalpha() or c.isspace())
        departmentnamehalf=departmentnamehalf.strip()

        # so in this case I put display department name in parenthesis
        # I may remove

        return departmentnamehalf

    def get_departmentcode(self, departmentname):
        departmentname=departmentname.replace('_','/')
        # the splitpoint is important, for UT its a "-"
        
        departmentnamehalf,code=departmentname.split('(')
        code=''.join(c for c in code if c.isalpha() or c.isspace())

        # so in this case I put display department name in parenthesis
        # I may remove

        return code

def main():
    '''
    Use this function to test when generation
    '''
    departmentname="Ancient Mediterranean Civilizations (AMCI)"

    dept = DepartmentName()

    departmentnamecleaned=dept.get_departmentnamecleaned(departmentname)
    display_departmentname=dept.get_display_departmentname(departmentname)
    departmentnamehalf=dept.get_departmentnamehalf(departmentname)
    code=dept.get_departmentcode(departmentname)

    
    print(f"departmentname:\n{departmentname}")
    print(f"departmentnamecleaned:\n{departmentnamecleaned}")
    print(f"display_departmentname:\n{display_departmentname}")
    print(f"departmentnamehalf:\n{departmentnamehalf}")
    print(f"code:\n{code}")

if __name__ == "__main__":
    main()
