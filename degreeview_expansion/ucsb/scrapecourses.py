import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def scrapecourses(departmenturl):
    departmentdata = {}

    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # run in background
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(60)  # increase if needed


    try:
        driver.get(departmenturl)

        if "/courses" not in driver.current_url:
            print(f"Redirected to a non-course page: {driver.current_url}. Skipping...")
            return None
        
        time.sleep(5)  # wait for JS to render the table
        html = driver.page_source
        coursesoup = BeautifulSoup(html, 'html.parser')
    except Exception as e:
        print(f"Error loading page: {e}")
        driver.quit()
        return None
    finally:
        driver.quit()

    table = coursesoup.select_one('section#coursesTabContent table')
    if not table:
        print(f"No table found for {departmenturl}")
        return None

    tbody = table.select_one('tbody.base-table__body')
    if not tbody:
        print(f"\n\nNo tbody found for {departmenturl}")
        return None
    

    trs = tbody.select('tr')

    for tr in trs:
        code_cell = tr.select_one('th')
        if not code_cell:
            continue

        coursecode = code_cell.get_text(strip=True).replace('\xa0', ' ')

        td_cells = tr.select('td')
        coursename = td_cells[0].get_text(strip=True) if len(td_cells) > 0 else ""

        # Determine course level from the number
        
        def get_coursehours():
            coursehours=''
            return coursehours


        def get_status():
            '''
            
            source:
            https://help.professional.ucsb.edu/general-information/academic-information/course-numbers
            '''
            match = re.search(r'\d+', coursecode)
            identifynumber = int(match.group()) if match else 0

            if identifynumber >= 200:
                status = 'Graduate'
            elif identifynumber >= 100:
                status = "Upper Division"
            else:
                status = "Lower Division"
            # override here
            # status=''
            return status
        
        coursehours=get_coursehours()
        status=get_status()

        # Handle repeated course names
        if coursename not in departmentdata:
            departmentdata[coursename] = [coursecode, coursehours, status]
        elif f"{coursename}SECOND" not in departmentdata:
            coursename += "SECOND"
            departmentdata[coursename] = [coursecode, coursehours, status]
        else:
            coursename += "THIRD"
            departmentdata[coursename] = [coursecode, coursehours, status]

    return departmentdata


def analyze_departmentdata(departmentdata):
    namelengthlist = []

    for key in departmentdata:
        coursecode, coursehours, category = departmentdata[key]
        coursename = key
        namelengthlist.append([coursename, len(coursename)])

    namelengthlist = sorted(namelengthlist, key=lambda x: x[1], reverse=True)
    print("Course name lengths (descending):", namelengthlist)
    print(f'\nLongest name: {namelengthlist[0]}')
    print(f'Shortest name: {namelengthlist[-1]}')


if __name__ == '__main__':
    testurl = 'https://catalog.ucsb.edu/departments/ANTH/courses'
    departmentdata = scrapecourses(departmenturl=testurl)
    if departmentdata:
        print(departmentdata)
        # analyze_departmentdata(departmentdata)
