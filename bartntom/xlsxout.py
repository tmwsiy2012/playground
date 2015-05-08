import mysql.connector
import xlsxwriter


def writeQuarterlyAreaDataExcelFile( filename, area, year, quarter):
	# Create an new Excel file and add a worksheet.
	workbook = xlsxwriter.Workbook(filename)
	worksheet = workbook.add_worksheet()

	# Add a bold format to use to highlight field name cells.
	bold = workbook.add_format({'bold': 1})
	# Widen columns to make the text clearer.
	worksheet.set_column('A:A', 20)
	worksheet.set_column('B:B', 14)
	worksheet.set_column('C:C', 45)
	worksheet.set_column('E:E', 7)
	worksheet.set_column('F:F', 21)
	worksheet.set_column('G:I', 19)
	worksheet.set_column('J:J', 20)
	worksheet.set_column('K:K', 22)
	worksheet.set_column('L:L', 22)
	worksheet.set_column('M:M', 21)

	worksheet.write(0,0,"Area",bold)
	worksheet.write(0,1,"Industry Code",bold)
	worksheet.write(0,2,"Industry Title",bold)
	worksheet.write(0,3,"Year",bold)
	worksheet.write(0,4,"Quarter",bold)
	worksheet.write(0,5,"Quarterly Establishments Count",bold)
	worksheet.write(0,6,"Month1 Employment",bold)
	worksheet.write(0,7,"Month2 Employment",bold)
	worksheet.write(0,8,"Month3 Employment",bold)
	worksheet.write(0,9,"Total Quarterly Wages",bold)
	worksheet.write(0,10,"Taxable Quarterly Wages",bold)
	worksheet.write(0,11,"Quarterly Contributions",bold)
	worksheet.write(0,12,"Average Weekly Wage",bold)


	connection = mysql.connector.connect(host='localhost', user='root', passwd='password', db='bls_qcew')
	cursor = connection.cursor()
	cursor.callproc("get_quarterly_entries_by_area_code",[area,year,quarter])
	#results = cursor.fetchall
	for result in cursor.stored_results():
		results=result.fetchall()
		
	row=1
	col=0
	for record in results:
		for field in record:
			worksheet.write(row,col,field)
			col += 1
		row += 1
		col=0
			
	workbook.close()


def writeAnnualAreaDataExcelFile( filename, area, year):
    # Create an new Excel file and add a worksheet.
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()

    # Add a bold format to use to highlight field name cells.
    bold = workbook.add_format({'bold': 1})
    # Widen columns to make the text clearer.
    worksheet.set_column('A:A', 20)
    worksheet.set_column('B:B', 14)
    worksheet.set_column('C:C', 45)
    worksheet.set_column('E:E', 14)
    worksheet.set_column('F:L', 20)
    worksheet.set_column('J:J', 26)
    worksheet.set_column('K:K', 18)

    worksheet.write(0,0,"Area",bold)
    worksheet.write(0,1,"Industry Code",bold)
    worksheet.write(0,2,"Industry Title",bold)
    worksheet.write(0,3,"Year",bold)
    worksheet.write(0,4,"Annual Average Establishments Count",bold)
    worksheet.write(0,5,"Average Employment",bold)
    worksheet.write(0,6,"Total Annual Wages",bold)
    worksheet.write(0,7,"Taxable Annual Wages",bold)
    worksheet.write(0,8,"Annual Contributions",bold)
    worksheet.write(0,9,"Annual Average Weekly Rate",bold)
    worksheet.write(0,10,"Average Annual Pay",bold)

<<<<<<< HEAD
    connection = mysql.connector.connect(host='localhost', user='root', passwd='password', db='bls_qcew')
=======
    connection = mysql.connector.connect(host='localhost', user='root', passwd='tr45sh32', db='bls_qcew')
>>>>>>> 9ad63e5691899c8d1e8a922961c7b9375b9dffa0
    cursor = connection.cursor()
    cursor.callproc("get_annual_entries_by_area_code",[area,year])
    #results = cursor.fetchall
    for result in cursor.stored_results():
        results=result.fetchall()
    
    row=1
    col=0
    for record in results:
        for field in record:
            worksheet.write(row,col,field)
            col += 1
        row += 1
        col=0
    workbook.close()

def writeAnnualAreaDataExcelFileWithNoBrainers(values_to_update, filename, area, year):
    # Create an new Excel file and add a worksheet.
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()

    # Add a bold format to use to highlight field name cells.
    bold = workbook.add_format({'bold': 1})
    # Widen columns to make the text clearer.
    worksheet.set_column('A:A', 20)
    worksheet.set_column('B:B', 14)
    worksheet.set_column('C:C', 45)
    worksheet.set_column('E:E', 14)
    worksheet.set_column('F:L', 20)
    worksheet.set_column('J:J', 26)
    worksheet.set_column('K:K', 18)

    worksheet.write(0,0,"Area",bold)
    worksheet.write(0,1,"Industry Code",bold)
    worksheet.write(0,2,"Industry Title",bold)
    worksheet.write(0,3,"Year",bold)
    worksheet.write(0,4,"Annual Average Establishments Count",bold)
    worksheet.write(0,5,"Average Employment",bold)
    worksheet.write(0,6,"Total Annual Wages",bold)
    worksheet.write(0,7,"Taxable Annual Wages",bold)
    worksheet.write(0,8,"Annual Contributions",bold)
    worksheet.write(0,9,"Annual Average Weekly Rate",bold)
    worksheet.write(0,10,"Average Annual Pay",bold)

<<<<<<< HEAD
    connection = mysql.connector.connect(host='localhost', user='root', passwd='password', db='bls_qcew')
=======
    connection = mysql.connector.connect(host='localhost', user='root', passwd='tr45sh32', db='bls_qcew')
>>>>>>> 9ad63e5691899c8d1e8a922961c7b9375b9dffa0
    cursor = connection.cursor()
    cursor.callproc("get_annual_entries_by_area_code",[area,year])
    #results = cursor.fetchall
    for result in cursor.stored_results():
        results=result.fetchall()
    
    row=1
    col=0
    for record in results:
        for field in record:
                worksheet.write(row,col,field)
                col += 1
                row += 1
                col=0
    workbook.close()
    
#writeQuarterlyAreaDataExcelFile('C4870','2012','2')
