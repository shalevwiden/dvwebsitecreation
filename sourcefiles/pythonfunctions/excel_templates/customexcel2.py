
import sys
import os
import json
import pandas as pd

import csv
import random

from openpyxl import load_workbook
from openpyxl import Workbook
# use this to define the function define_start_column
from openpyxl.utils import column_index_from_string
from openpyxl.utils import get_column_letter


# this assigns cells colors
from openpyxl.styles import PatternFill

import time
import os

from openpyxl.styles import Font
from openpyxl.styles import Border, Side, Alignment

import sqlite3

'''
This is for converting data from .DTA files, csvs, and more, into workable with excelfiles
'''
def makecustom_excelfile2(heading, leftsecondary,rightsecondary,
                         
                    columnheadings,
                    rows,

                   savepath,secondarycolor,bigbordercolor,smallerbordercolor,
                   gridlinecolor,rowtextcolor,titlecolor,
                   mainbackgroundcolor,paddingbackgroundcolor,
                   subheadingbordercolor,
                    
                   datafontname="Helvetica",titlefontname='Calibri',
                   logofontname="Barlow",
                   logocolor="ffffff",
                   urlcolor='ffffff',
                   subheadingsize=22,
                   subheadingcolor='ffffff',
                   headingsfontname='Calibri',
                   headingsfontcolor='ffffff',
                   datarowheight=30,
                   headingrowheight=40,
                   columnscaler=1,                    

                   ):

    '''Rows will end up being a list of lists
    Schoolnamecolor must be a hex code without a #either

    column scaler just affects all the columns at once, doesn't change individual ones

    Important to note that the white fonts make this function start by default as a dark theme
    '''
    departmentworkbook=Workbook()
    # gets the default worksheet
    ws=departmentworkbook.active

    # override it lol for now


        
    titlefont=Font(size=33,bold=True,color=titlecolor,name=titlefontname)
    headingborder=Border(bottom=Side(style='mediumDashDot',color=smallerbordercolor))

    # this is for the row that has the department name and the universityname (latter is updated later)
    headingsfonts=Font(size=21,bold=True,color=headingsfontcolor,name=headingsfontname)

    # this is for like Coursename, Courserow, etc.
    subheadingsfont=Font(size=subheadingsize,bold=True,color=subheadingcolor)
    # lighter burnt orange
    # reuse the headingsfontname argument
    secondaryfont=Font(size=19, color=secondarycolor, name=headingsfontname, bold=True)
    # update later

    # applied to the actual semester data. 
    datafont=Font(size=15,name=datafontname,color=rowtextcolor)


    leftalign=Alignment(horizontal='left')
    centeralign=Alignment(horizontal='center')

    # plus one because of how columns work in excel
    lastcolumnletter=get_column_letter(len(columnheadings)+1)
    secondtolastletter=get_column_letter(len(columnheadings))

    lastcolumnindex=len(columnheadings)+1
    



    # total height of 40


    # first row after title that is. Start at row 3 since rows 1 and 2 were merged

    firstrow=[f'{leftsecondary}']
   

        
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

    subheadingrow=columnheadings
    ws.append(subheadingrow)
    # now apply styles
    previousrow = ws[ws.max_row]

    # print(f"previousrow was {[cell.value for cell in previousrow]}")

    for cell in ws[5]:
        cell.font=subheadingsfont
        cell.alignment=leftalign

    
    def set_headings_height():
        for row in [3,4]:
            ws.row_dimensions[row].height = headingrowheight
    set_headings_height()


    # now the meat of the file, the data
    



    # for each course
    def writecoursedata(subrows):
        '''
        This adds the rows to the excel object which later adds it with all the courses and stuff.
        Rowval is used later to add the rows on there
        '''
        excelobject=[]                        

        totalhours=0
        # this dict is simple
        lengthofrows=len(subrows)
        # can change this later to expand it
        
        rows=[]
        for row in subrows:
            rows.append(row)

        for row in rows:
            excelobject.append(row)
        
        return rows,excelobject


        # write an empty line at the end

    rows,excelobject=writecoursedata(subrows=rows)


        

    # adding to excel file
    # rowval is important for adding rows in order

    '''
    Using the length of Excel object to find out when to put the end stuff
    '''
    # starting row
    rowval=6

    def style_rows_and_cols():       
        '''
        This actually adds the rows with all the courses and stuff.
        Rowval is used later to add the rows on there
        '''
        rowindexes=len(excelobject)+rowval
        for rowentry in range(rowval, rowindexes):
            # update it here so it updates by row not column...although

            if rowentry%2==0:            
                ws.row_dimensions[rowentry].height = datarowheight  # sets height of the entire row
            else:
                ws.row_dimensions[rowentry].height = datarowheight+50  # sets height of the entire row




                    # start at column one, and then remember the padding rows are added later. 
            excelobjectrowindex=rowentry-rowval
            for col_index, value in enumerate(excelobject[excelobjectrowindex], start=1):
                # change alignnment here. 1 indexed not 0
                datacell = ws.cell(row=rowentry, column=col_index, value=value)

                datacell.font=datafont
                # alignment happens later
    style_rows_and_cols()
                
    
            


    print(f'len excel object={len(excelobject)}, ie number of datarows')
    

# -----------------------------end data stuff --------------------------------------------------------
    ws.append(blankrow)
   


    # normally put like custom excel themes here
    # put a url later
    reddituser='Digital Navigator'
    lastrow=['Animotion']
    lastrow += [''] * (len(columnheadings)  - 2)
    lastrow += ['ANM']

    


    lastrowindex=len(rows)+7

    # change the logo colors here
    for col_index, value in enumerate(lastrow, start=1):
        
        # use.font to assign the font I see
        lastrowcell=ws.cell(row=lastrowindex, column=col_index, value=value)
        # FF=full opacity 
        if col_index==lastcolumnindex-1:
            # site link cell
            # keep this the same
            lastrowcell.value='ANM'
            lastrowcell.font=Font(name='Roboto',size=19, bold=True, color=urlcolor)
            lastrowcell.alignment=Alignment(horizontal='left',vertical='bottom')

            cell = ws.cell(row=lastrowindex, column=lastcolumnindex)

            


        elif col_index==1:
            logocell=lastrowcell
            logocell.value='Animotion'
            logocell.font=Font(name=logofontname,size=26, bold=True, color=logocolor)
            logocell.alignment=Alignment(horizontal='left',vertical='center')

        # else:
        #     lastrowcell.value=''


        # one more cause now we wrote the actual last row there
        ws.row_dimensions[lastrowindex+1].height = 50



    # ---------------formatting stuff------------------
    
    # add padding
    
    
    ws.insert_rows(1)      #new row
    ws.insert_cols(1)       # new col

    # ws.columns gets columns. Each column is a tuple of cells
    # this is for dynamic widths. I want standard widths now.
    for column_cells in ws.columns:
        # max function gets the max in a list. Same for min
        # generator must be in ()
        cellwidthgenerator=(len(str(cell.value)) if cell.value else 0 for cell in column_cells)
        colwidth = max(cellwidthgenerator)

        mincolwidth=10
        if colwidth<mincolwidth:
            colwidth=mincolwidth
        

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


    def standardize_colwidths():
        '''animate this by causing it to shrink and grow.'''
        width=30
        for index in range(1, len(columnheadings) + 1):
            col_letter = get_column_letter(index)

            ws.column_dimensions[col_letter].width=width

    # standardize_colwidths()

    newcolumnindex=get_column_letter(len(columnheadings)+1)

    ws.column_dimensions['A'].width=15
    ws.column_dimensions[f'{newcolumnindex}'].width=15
    ws.row_dimensions[1].height=45
    ws.row_dimensions[lastrowindex+2].height=45


    # ------------------------------------TITLE STUFF-------------------------------------------

    # create a merged 'Degree view and departmentname header can't lie".
    ws.merge_cells(f'B2:{lastcolumnletter}3')    
    ws.row_dimensions[2].height = 30
    ws.row_dimensions[3].height = 30
    mergedrowcontent=f'{heading}'
    
    # refer to top left of merged cells
    titlecell=ws['B2']
    titlecell.value=mergedrowcontent
    titlecell.alignment = Alignment(horizontal='center', vertical='center')
    titlecell.font=titlefont

    # NOW THE UNIVERSITY CELL STUFF
    avoidletterslist=['A','B','C']
    if secondtolastletter not in avoidletterslist:    
        ws.merge_cells(f'{secondtolastletter}4:{lastcolumnletter}4')    

        print(f'Second to last letter {secondtolastletter}')
        ws[f'{secondtolastletter}4'].value = rightsecondary
        ws[f'{secondtolastletter}4'].font = secondaryfont
        ws[f'{secondtolastletter}4'].border = headingborder
        # right align
        ws[f'{secondtolastletter}4'].alignment = Alignment(horizontal='right')
    # I inserted a row, thats why +=it
    logorowindex=lastrowindex+1
    ws.merge_cells(f'B{logorowindex}:D{logorowindex}')
    ws[f'B{logorowindex}'].alignment = Alignment(horizontal='left')


# ------------------------ CONTINUE FORMATTING STUFF -----------------------------------------------------
    # apply a border around the entire file -----------------------------------------------------------------------------

    # make it responsive based on the amount of data
    # remove the +1 here to have no border
    
    rows = list(ws['B2':f'{lastcolumnletter}{lastrowindex+1}'])
    min_row = 2
    max_row = lastrowindex+1

    min_col = column_index_from_string('B')  
    secondtolastcolindex=column_index_from_string(secondtolastletter)


    maxcolindex=column_index_from_string(secondtolastletter)
    print(f'Max column index : {maxcolindex}')

    # where border code used to be
    
    # make the entire worksheet a color:
    # this is padding tho cause we override this later
    paddingcolor=PatternFill(fill_type="solid", start_color=paddingbackgroundcolor) #end_color='0000FF' fill_type="gray125" or linear later

    # have the background be like a padding. 
    # +1 because of the new column added on the right
    for row in ws.iter_rows(min_row=1, max_row=lastrowindex+2, min_col=1, max_col=lastcolumnindex+1):
        for cell in row:
            cell.fill = paddingcolor
    
    # reverse the background for cells with content:

    backgroundfill=PatternFill(fill_type="solid", start_color=mainbackgroundcolor)
    # re-add gridline borders:

    gridline_border = Border(
        # make gridline border not exactly white
        left=Side(border_style="thin", color=gridlinecolor),
        right=Side(border_style="thin", color=gridlinecolor),
        top=Side(border_style="thin", color=gridlinecolor),
        bottom=Side(border_style="thin", color=gridlinecolor)
    )

    for row in ws.iter_rows(min_row=min_row, max_row=max_row, min_col=min_col, max_col=lastcolumnindex):
        for cell in row:
            cell.fill = backgroundfill
            cell.border=gridline_border

    rowval+=1

    def style_rows_and_cols():       
        '''
        This actually adds the rows with all the courses and stuff.
        Rowval is used later to add the rows on there.

        Here you can make rows different heights and do all kinds of crazy stuff
        '''

        allcenteredalignment=Alignment(vertical='center',horizontal='center')
        leftcenter=Alignment(vertical='center',horizontal='left')

        rowindexes=len(excelobject)+rowval
        for rowentry in range(rowval, rowindexes):
            # update it here so it updates by row not column...although

            if rowentry%2==0:            
                ws.row_dimensions[rowentry].height = datarowheight  # sets height of the entire row
            else:
                ws.row_dimensions[rowentry].height = datarowheight  # sets height of the entire row




                    # start at column one, and then remember the padding rows are added later. 
            excelobjectrowindex=rowentry-rowval
            for col_index, value in enumerate(excelobject[excelobjectrowindex], start=2):
                # change alignnment here. 1 indexed not 0
                datacell = ws.cell(row=rowentry, column=col_index)

                def col_alignments():
                     
                    datacell.alignment=allcenteredalignment
                    
                col_alignments()

    # big function call
    style_rows_and_cols()
    
    
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
    right=entire_ws_border if col_index == lastcolumnindex else current.right
)

    

    # where is this one?
    # this is like the subheading border
    # keep min and max row 6 to apply the heading border
    for row in ws.iter_rows(min_row=6, max_row=6, min_col=2, max_col=secondtolastcolindex):
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
    
    
    departmentworkbook.save(savepath)
    print(f'Saved workbook at {savepath}')