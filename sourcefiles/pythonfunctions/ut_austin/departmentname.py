
'''
This is for UT Austin department names every school might be a little different
'''
def get_departmentnamecleaned(departmentname):

    departmentname=departmentname.replace('/','_')




    departmentnamecleaned=departmentname.replace(' ','').lower()
    departmentnamecleaned=departmentnamecleaned.replace(',','-').lower()

    departmentnamecleaned=departmentnamecleaned.replace('/','_')
    return departmentnamecleaned

def get_display_departmentname(departmentname):
    displaydepartmentname=departmentname.replace('_','/')
    displaydepartmentname=departmentname.strip().split('-')
    code=displaydepartmentname[0].strip()
    departmentnamehalf=displaydepartmentname[-1].strip()
    displaydepartmentname=f'({code}) - {departmentnamehalf}'