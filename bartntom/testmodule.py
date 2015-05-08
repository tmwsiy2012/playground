import xlsxout
import xlrd
import mysql.connector


def isNoBrainerAnnual(suppressed_codes,area,year,industry_code):
    connection = mysql.connector.connect(host='localhost', user='root', passwd='password', db='bls_qcew')
    cursor = connection.cursor()    
    cursor.callproc("get_annual_sibling_entries",[area,industry_code,year,False])
    #results = cursor.fetchall
    for result in cursor.stored_results():
    	results=result.fetchall()
    if len(results)==0:
        return False
    for record in results:
        if record[1] in suppressed_codes:
            return False
    return True
  
def isNoBrainerAnnualSum(suppressed_codes,area,year,industry_code):
    connection = mysql.connector.connect(host='localhost', user='root', passwd='tr45sh32', db='bls_qcew')
    cursor = connection.cursor()
    sibling_sum=0
    cursor.callproc("get_annual_sibling_entries",[area,industry_code,year,False])
    #results = cursor.fetchall
    for result in cursor.stored_results():
    	results=result.fetchall()		
    for record in results:
        sibling_sum+=record[5]
        if record[1] in suppressed_codes:
            return 0
    return sibling_sum


xlsxout.writeAnnualAreaDataExcelFile('test.xlsx','37021','2012')
workbook = xlrd.open_workbook('test.xlsx')
worksheet = workbook.sheet_by_name('Sheet1')
num_rows = worksheet.nrows - 1
num_cells = worksheet.ncols - 1
curr_row = -1
suppresed_rows=0
six_digit_sup=0
five_digit_sup=0
four_digit_sup=0
three_digit_sup=0
two_digit_sup=0
super_sup=0
suppressed_codes = list()
no_brainer_codes = list()
while curr_row < num_rows:
    curr_row += 1
    row = worksheet.row(curr_row)
    if worksheet.cell_value(curr_row,5) == 0:
        # this is a suppressed code
        industry_code = worksheet.cell_value(curr_row,1)
        suppressed_codes.append(industry_code)
        suppresed_rows+=1        
        industry_code_length = len(worksheet.cell_value(curr_row,1))
        if industry_code_length == 6:
            six_digit_sup+=1
        elif industry_code_length == 5:
            five_digit_sup+=1
        elif industry_code_length == 4 and not industry_code.startswith('10'):
            four_digit_sup+=1
        elif industry_code_length == 3 and not industry_code.startswith('10'):
            three_digit_sup+=1
        elif industry_code_length == 2 or '-' in industry_code:
            two_digit_sup+=1
        elif industry_code.startswith('10'):
            super_sup+=1              
        #print ('Row:', curr_row, worksheet.cell_value(curr_row,5))
        curr_cell = -1
        while curr_cell < num_cells:
            curr_cell += 1
            # Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
            cell_type = worksheet.cell_type(curr_row, curr_cell)
            cell_value= worksheet.cell_value(curr_row, curr_cell)
            #print ('	', cell_type, ':', cell_value)



print("Total Suppressed:",suppresed_rows,"Percentage of entries:",(suppresed_rows/num_rows)*100)
print("Super Suppressed:",super_sup,"Percentage:",(super_sup/suppresed_rows)*100)
print("Two Digit Suppressed:",two_digit_sup,"Percentage of Suppressed:",(two_digit_sup/suppresed_rows)*100)
print("Three Digit Suppressed:",three_digit_sup,"Percentage of Suppressed:",(three_digit_sup/suppresed_rows)*100)
print("Four Digit Suppressed:",four_digit_sup,"Percentage of Suppressed:",(four_digit_sup/suppresed_rows)*100)
print("Five Digit Suppressed:",five_digit_sup,"Percentage of Suppressed:",(five_digit_sup/suppresed_rows)*100)
print("Six Digit Suppressed:",six_digit_sup,"Percentage of Suppressed:",(six_digit_sup/suppresed_rows)*100)

for sc in suppressed_codes:    
    if isNoBrainerAnnual(suppressed_codes,'37021','2012',sc):
        no_brainer_codes.append(sc)

print((len(no_brainer_codes)/len(suppressed_codes))*100,"% no brainer")

    




worksheet.close()







