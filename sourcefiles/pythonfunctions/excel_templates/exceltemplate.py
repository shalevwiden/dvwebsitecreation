
import sys
import os
import json

import csv


from openpyxl import load_workbook
from openpyxl import Workbook
# use this to define the function define_start_column
from openpyxl.utils import column_index_from_string

# this assigns cells colors
from openpyxl.styles import PatternFill

import time
import os

from openpyxl.styles import Font
from openpyxl.styles import Border, Side, Alignment

import sqlite3


def make_excelfile(departmentname,universityname,
                   savepath,rows,schoolnamecolor,bigbordercolor,smallerbordercolor,
                   gridlinecolor,rowtextcolor,titlecolor,
                   mainbackgroundcolor,paddingbackgroundcolor,
                   subheadingbordercolor,
                   datafontname="Helvetica",titlefontname='Calibri',
                   logofontname="Barlow",
                   logocolor="ffffff",
                   subheadingsize=17,
                   subheadingcolor='ffffff',
                   headingsfontname='Calibri',
                   headingsfontcolor='ffffff',
                   datarowheight=23,
                   headingrowheight=30,
                   columnscaler=1
                   ):

    '''Rows will end up being a list of lists
    Schoolnamecolor must be a hex code without a #either

    column scaler just affects all the columns at once, doesn't change individual ones

    Important to note that the white fonts make this function start by default as a dark theme
    '''
    departmentworkbook=Workbook()
    # gets the default worksheet
    ws=departmentworkbook.active



        
    titlefont=Font(size=33,bold=True,color=titlecolor,name=titlefontname)
    headingborder=Border(bottom=Side(style='mediumDashDot',color=smallerbordercolor))

    # this is for the row that has the department name and the universityname (latter is updated later)
    headingsfonts=Font(size=21,bold=True,color=headingsfontcolor,name=headingsfontname)

    # this is for like Coursename, Courserow, etc.
    subheadingsfont=Font(size=subheadingsize,bold=True,color=subheadingcolor)
    # lighter burnt orange
    universitynamefont=Font(size=19, color=schoolnamecolor, name='Georgia', bold=True)
    # update later

    # applied to the actual semester data. 
    datafont=Font(size=15,name=datafontname,color=rowtextcolor)


    leftalign=Alignment(horizontal='left')
    centeralign=Alignment(horizontal='center')
    



    # total height of 40


    # first row after title that is. Start at row 3 since rows 1 and 2 were merged

    firstrow=[f'{departmentname}']
   

        
    # colindex is like i            
    # start= 1 means start at the first column
    for col_index, value in enumerate(firstrow, start=1):
        # adjust row here
        headingcell=ws.cell(row=3, column=col_index, value=value)
        # use.font to assign the font I see
            
        if col_index==1:
            headingcell.font=headingsfonts
            headingcell.border=headingborder
            headingcell.alignment=centeralign
        
        
        

            # print(datacell.font.size)


    blankrow=['','','','','','']
    # appends to the next empty row. Like writer.writerow(['']) for csvs
    ws.append(blankrow)

    subheadingrow=['Course Name','Course Code','Hours','Classification']
    ws.append(subheadingrow)
    # now apply styles
    previousrow = ws[ws.max_row]

    print(f"previousrow was {[cell.value for cell in previousrow]}")
    for cell in ws[5]:
        cell.font=subheadingsfont
        cell.alignment=leftalign

    
    def set_headings_height():
        for row in [3,4,5]:
            ws.row_dimensions[row].height = headingrowheight
    set_headings_height()

    # now the meat of the file, the data
    


    excelobject=[]                        

    # for each semester
    def writecoursedata():
        totalhours=0
        # this dict is simple
    
        for row in rows:
            print(f'Row in Excel\n {row}')
            coursename,coursecode,coursehours,upperlowerstatus=row
            coursename=coursename.replace('SECOND','').replace('THIRD','')

            excelobject.append([coursename,coursecode,coursehours,upperlowerstatus])

            if ',' in coursehours:
                coursehours=coursehours.split(',')[-1]
            totalhours+=int(coursehours)

        # write an empty line at the end
        excelobject.append(['','','','',''])
        return totalhours

    totalhours=writecoursedata()
        

    # adding to excel file
    # rowval is important for adding rows in order

    '''
    Using the length of Excel object to find out when to put the end stuff
    '''
    rowval=5

    for rowentry in range(len(excelobject)):
        # update it here so it updates by row not column...although
        rowval += 1
        ws.row_dimensions[rowval].height = datarowheight  # sets height of the entire row


                # start at column one, and then remember the padding rows are added later. 
        for col_index, value in enumerate(excelobject[rowentry], start=1):
            # change alignnment here. 1 indexed not 0
            datacell = ws.cell(row=rowval, column=col_index, value=value)

            if col_index in [1,2]:
                datacell.font=datafont
                datacell.alignment=leftalign
            elif col_index==3: #hourscol
                datacell.font=datafont
                datacell.alignment=centeralign
            elif col_index in [4]:
                datacell.font=datafont
                datacell.alignment=leftalign
            
    
            


    print(f'len excel object={len(excelobject)}, ie number of datarows')
    

# -----------------------------end data stuff --------------------------------------------------------
    ws.append(blankrow)
    totalhoursrow=['','',f'Total Hours: {totalhours}','','']

    # this lastrow value is actually used for the last TWO rows
    lastrowindex=len(excelobject)+6
    for col_index, value in enumerate(totalhoursrow, start=1):
        
        # use.font to assign the font I see
        cell=ws.cell(row=lastrowindex+1, column=col_index, value=value)
        # FF=full opacity 
        cell.font=datafont


    lastrow=['DegreeView','','','degreeviewsite.com']
    lastrowindex+=2 # 6 rows before we start data stuff. Then rowcount is the amount of data. 

    # change the logo colors here
    for col_index, value in enumerate(lastrow, start=1):
        
        # use.font to assign the font I see
        lastcell=ws.cell(row=lastrowindex, column=col_index, value=value)
        # FF=full opacity 
        if col_index==4:
            # site link cell
            # keep this the same
            lastcell.font=Font(name='Roboto',size=19, bold=True, color='e7e9eb')
            lastcell.alignment=Alignment(horizontal='left',vertical='bottom')

        else:
            # logo cell - CHANGE THIS
            lastcell.font=Font(name=logofontname,size=30, bold=True, color=logocolor)
            lastcell.alignment=Alignment(horizontal='left',vertical='center')

        # one more cause now we wrote the actual last row there
        ws.row_dimensions[lastrowindex+1].height = 50



    # ---------------formatting stuff------------------
    
    # add padding
    
    
    ws.insert_rows(1)      #new row
    ws.insert_cols(1)       # new col

    # ws.columns gets columns. Each column is a tuple of cells
    for column_cells in ws.columns:
        # max function gets the max in a list. Same for min
        # generator must be in ()
        cellwidthgenerator=(len(str(cell.value)) if cell.value else 0 for cell in column_cells)
        colwidth = max(cellwidthgenerator)

        firstcell=column_cells[0]
        # every cell has a .column_letter attribute
        col_letter = firstcell.column_letter
        col_index=column_index_from_string(col_letter)
        # scale the width factor to make the columns wider
        if col_index==7:  
            # make the UT Austin column alot wider
            ws.column_dimensions[col_letter].width = int(colwidth)*2*columnscaler
        elif col_index==6:
            ws.column_dimensions[col_letter].width = int(colwidth)*1.9*columnscaler
        elif col_index==5:
            ws.column_dimensions[col_letter].width=int(colwidth)*1.9*columnscaler
        elif col_index==4:
            ws.column_dimensions[col_letter].width=int(colwidth)*1.9*columnscaler
        elif col_index==3:
            ws.column_dimensions[col_letter].width=int(colwidth)*1.5*columnscaler
        
        # the semester column
        elif col_index==2:
            ws.column_dimensions[col_letter].width=int(colwidth)*1.3*columnscaler
    

        else:
            ws.column_dimensions[col_letter].width = int(colwidth)*1.1*columnscaler
        



    # set sizes for the padding row and column. Units of default font which is usually Arial it seems

    ws.column_dimensions['A'].width=15
    ws.column_dimensions['F'].width=15
    ws.row_dimensions[1].height=45
    ws.row_dimensions[lastrowindex+2].height=45

    # ------------------------------------TITLE STUFF-------------------------------------------

    # create a merged 'Degree view and departmentname header can't lie".
    ws.merge_cells('B2:E3')    
    ws.row_dimensions[2].height = 30
    ws.row_dimensions[3].height = 30
    mergedrowcontent=f'{departmentname} Courses'
    
    # refer to top left of merged cells
    titlecell=ws['B2']
    titlecell.value=mergedrowcontent
    titlecell.alignment = Alignment(horizontal='center', vertical='center')
    titlecell.font=titlefont

    # NOW THE UNIVERSITY CELL STUFF
    ws.merge_cells('C4:E4')    

    ws['C4'].value = universityname
    ws['C4'].font = universitynamefont
    ws['C4'].border = headingborder
    # right align
    ws['C4'].alignment = Alignment(horizontal='right')

# ------------------------ CONTINUE FORMATTING STUFF -----------------------------------------------------
    # apply a border around the entire file -----------------------------------------------------------------------------

    # make it responsive based on the amount of data
    # remove the +1 here to have no border
    rows = list(ws['B2':f'E{lastrowindex+1}'])
    min_row = 2
    max_row = lastrowindex+1

    min_col = column_index_from_string('B')  
    max_col = column_index_from_string('E') 

    
    # where border code used to be
    
    # make the entire worksheet a color:
    # this is padding tho cause we override this later
    paddingcolor=PatternFill(fill_type="solid", start_color=paddingbackgroundcolor) #end_color='0000FF' fill_type="gray125" or linear later

    # have the background be like a padding. 
    for row in ws.iter_rows(min_row=1, max_row=lastrowindex+2, min_col=1, max_col=6):
        for cell in row:
            cell.fill = paddingcolor
    
    # reverse the background for cells with content:

    darkfill=PatternFill(fill_type="solid", start_color=mainbackgroundcolor)
    # re-add gridline borders:

    gridline_border = Border(
        # make gridline border not exactly white
        left=Side(border_style="thin", color=gridlinecolor),
        right=Side(border_style="thin", color=gridlinecolor),
        top=Side(border_style="thin", color=gridlinecolor),
        bottom=Side(border_style="thin", color=gridlinecolor)
    )

    for row in ws.iter_rows(min_row=min_row, max_row=max_row, min_col=min_col, max_col=max_col):
        for cell in row:
            cell.fill = darkfill
            cell.border=gridline_border
    
    # this is the border that will go around everything.
    # Use logic to only add border to the cells on the outside.

    entire_ws_border=Side(style='thick',color=bigbordercolor)
    
    for row_index, row in enumerate(rows, start=min_row):
        for col_index, cell in enumerate(row, start=min_col):
            current = cell.border

            
            # remember we defined side. and you do Border(Side=style))
            '''
            This is the final peice of the puzzle that adds borders.
            If sides if empty, then
            cell.border = Border(), which defines no borders. Normally it will be entire_ws_border border preset. 
            '''
            cell.border = Border(
    top=entire_ws_border if row_index == min_row else current.top,
    bottom=entire_ws_border if row_index == max_row else current.bottom,
    left=entire_ws_border if col_index == min_col else current.left,
    right=entire_ws_border if col_index == max_col else current.right
)

    

    # where is this one?
    # this is like the subheading border
    for row in ws.iter_rows(min_row=6, max_row=6, min_col=2, max_col=5):
        for cell in row:
            current = cell.border
            cell.border = Border(
                top=current.top,
                bottom=Side(style='medium',color=subheadingbordercolor),  # Only change bottom keep thick border around everything
                left=current.left,
                right=current.right
            )
    
    logocell=ws[f'E{lastrowindex}']
    logocell.border = Border(
        left=current.left,
        right=entire_ws_border,   # only change right
        top=current.top,
        bottom=current.bottom  # preserve existing bottom

        )   
    # It was applied the whole time just not visible
    print(f"Applied border to logocell {logocell.coordinate}, row={logocell.row}, column={logocell.column}")
    
    
    departmentworkbook.save(savepath)
    print(f'Saved workbook at {savepath}')