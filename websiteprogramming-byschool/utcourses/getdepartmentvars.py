'''
This file will have code to take the departmentname and get the displaydepartmentname
and the department name half for UT Austin.
'''

def get_displaydepartmentname(departmentname):
    displaydepartmentname=departmentname.replace('_','/')
    displaydepartmentname=departmentname.strip().split('-')
    code=displaydepartmentname[0].strip()
    departmentnamehalf=displaydepartmentname[-1].strip()
    displaydepartmentname=f'({code}) - {departmentnamehalf}'

    if len(displaydepartmentname)>60:
        displaydepartmentname=displaydepartmentname.split(')')
        displaydepartmentname=f'{displaydepartmentname[0]}<br>{displaydepartmentname[-1]}'

    print(f'Display department name= {displaydepartmentname}')
    return displaydepartmentname

def get_departmentnamehalf(departmentname):
    departmentname=departmentname.replace('_','/')
    departmentname=departmentname.strip().split('-')
    
    departmentnamehalf=departmentname[-1].strip()
    return departmentnamehalf