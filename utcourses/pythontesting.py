def oldtesting():

    linetext='A I 380E. Ethics in Artificial Intelligence.'

    coursecode,coursename=linetext.split('.')[0],linetext.split('.')[1]


    coursename=coursename.strip()
    coursecode=coursecode.replace('\xa0',' ')

    if '(' in coursecode:
        cleanedcoursecode=coursecode.split('(')[0]
    else:
        cleanedcoursecode=coursecode

    coursenumber=cleanedcoursecode.split(' ')[-1]
    print(coursenumber)
    coursehours=coursenumber[-1]

    # for them coursenames with crazy hours
    print(cleanedcoursecode.split(' ')[1:])
    if len(cleanedcoursecode.split(' ')[1:])>1:
        removeletters=''
        for i in cleanedcoursecode:
            if not i.isalpha():
                removeletters+=i
        cleanedcoursecode=removeletters
        print(f'new: {cleanedcoursecode}')
        coursenumbers=cleanedcoursecode.split(',')
        print(coursenumbers)
        coursehourslist=[]

        for coursenumber in coursenumbers:
            coursehours=coursenumber.strip()[0]
            coursehourslist.append(coursehours)
        coursehours=coursehourslist
        print(coursehours)

def newtesting():
    linetext='E 348J. J. M. Coetzee.'
    print(linetext)

    coursecode=linetext.split('.')[0]
    coursename=linetext.split('.')[1:]
    coursename=[part for part in coursename if part]
    coursename='.'.join(coursename)
    # coursename=''
    print(f'Coursename:{coursename}')


    # coursename=coursename.strip()
    coursecode=coursecode.replace('\xa0',' ')
    
    if '(' in coursecode:
        cleanedcoursecode=coursecode.split('(')[0].strip()
    else:
        cleanedcoursecode=coursecode
    
    print(f'Cleancoursecode={cleanedcoursecode}')
    coursenumber=cleanedcoursecode.split(' ')[-1]
    print(f'coursenumber: {coursenumber}')

    coursehours=coursenumber[0]

    identifynumber=coursenumber
newtesting()

def scrapeutcourses(departmenturl):
    deparmentdata={}
    ...
    return departmentdata
