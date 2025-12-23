
'''
This is for UT Austin department names every school might be a little different


'''

departmentname="ACF - Actuarial Foundations"

def get_departmentnamecleaned(departmentname):

    departmentname=departmentname.replace('/','_')




    departmentnamecleaned=departmentname.replace(' ','').lower()
    departmentnamecleaned=departmentnamecleaned.replace(',','-').lower()

    departmentnamecleaned=departmentnamecleaned.replace('/','_')
    return departmentnamecleaned

def get_display_departmentname(departmentname):
    '''
    This one actually doesnt use departmentname cleaned, because capitalization will be displayed
    
    
    '''

    displaydepartmentname=departmentname.replace('_','/')
    # the splitpoint is important, for UT its a "-"
    displaydepartmentname=departmentname.strip().split('-')
    code=displaydepartmentname[0].strip()
    departmentnamehalf=displaydepartmentname[-1].strip()

    # so in this case I put display department name in parenthesis
    # I may remove
    displaydepartmentname=f'({code}) - {departmentnamehalf}'
    return displaydepartmentname

def get_departmentnamehalf(departmentname):
    displaydepartmentname=departmentname.replace('_','/')
    # the splitpoint is important, for UT its a "-"
    displaydepartmentname=departmentname.strip().split('-')
    
    departmentnamehalf=displaydepartmentname[-1].strip()
    return departmentnamehalf

def get_departmentcode(departmentname):
    displaydepartmentname=departmentname.replace('_','/')
    # the splitpoint is important, for UT its a "-"
    displaydepartmentname=departmentname.strip().split('-')
    
    code=displaydepartmentname[0].strip()
    return code

def main():
    departmentnamecleaned=get_departmentnamecleaned(departmentname)
    display_departmentname=get_display_departmentname(departmentname)
    departmentnamehalf=get_departmentnamehalf(departmentname)
    code=get_departmentcode(departmentname)

    print(departmentname)
    print(departmentnamecleaned)
    print(display_departmentname)
    print(departmentnamehalf)
    print(code)

if __name__ == "__main__":
    main()
