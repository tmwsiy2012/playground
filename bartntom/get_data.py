__author__ = 'tmwsiy'
import mysql.connector
from conf.config import db_config
import pprint
import xlsxwriter

class MySQLCursorDict(mysql.connector.cursor.MySQLCursorBuffered):
    def _row_to_python(self, rowdata, desc=None):
        row = super(MySQLCursorDict, self)._row_to_python(rowdata, desc)
        if row:
            return dict(zip(self.column_names, row))
        return None

def write_xlsx_file( filename):
    # Create an new Excel file and add a worksheet.
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet('Knowledge')

    # Add a bold format to use to highlight field name cells.
    bold = workbook.add_format({'bold': 1})
    # Widen columns to make the text clearer.

    worksheet.set_column('A:A', 12)
    worksheet.set_column('B:B', 20)
    worksheet.set_column('C:C', 45)
    worksheet.set_column('D:D', 7)
    worksheet.set_column('E:E', 7)
    worksheet.set_column('F:F', 21)
    worksheet.set_column('G:I', 19)

    worksheet.write(0,0,"Onet Soc Code",bold)
    worksheet.write(0,1,"Title",bold)
    worksheet.write(0,2,"Knowledge Area",bold)
    worksheet.write(0,3,"Importance",bold)
    worksheet.write(0,4,"Level",bold)
    worksheet.write(0,5,"Description",bold)


    results = get_knowl_tmp_final()

    row=1
    for record in results:
        worksheet.write(row,0,record['onetsoc_code'])
        worksheet.write(row,1,record['title'])
        worksheet.write(row,2,record['element_name'])
        worksheet.write(row,3,record['importance_value'])
        worksheet.write(row,4,record['level_value'])
        worksheet.write(row,5,record['description'])
        row += 1

    worksheet = workbook.add_worksheet('Skills')
    results = get_skill_tmp_final()

    worksheet.set_column('A:A', 12)
    worksheet.set_column('B:B', 20)
    worksheet.set_column('C:C', 45)
    worksheet.set_column('D:D', 7)
    worksheet.set_column('E:E', 7)
    worksheet.set_column('F:F', 21)
    worksheet.set_column('G:I', 19)

    worksheet.write(0,0,"Onet Soc Code",bold)
    worksheet.write(0,1,"Title",bold)
    worksheet.write(0,2,"Skill Area",bold)
    worksheet.write(0,3,"Importance",bold)
    worksheet.write(0,4,"Level",bold)
    worksheet.write(0,5,"Description",bold)

    row=1
    for record in results:
        worksheet.write(row,0,record['onetsoc_code'])
        worksheet.write(row,1,record['title'])
        worksheet.write(row,2,record['element_name'])
        worksheet.write(row,3,record['importance_value'])
        worksheet.write(row,4,record['level_value'])
        worksheet.write(row,5,record['description'])
        row += 1

    workbook.close()

def get_knowledge_importance_values():
    return_value=[]
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(cursor_class=MySQLCursorDict)
    cursor.execute('''
        SELECT knowltmpid,data_value
        FROM knowledge_tmp
        WHERE scale_name='Importance'
    ''')
    rows = cursor.fetchall()
    for row in rows:
        return_value.append(row)
    return return_value

def get_skills_importance_values():
    return_value=[]
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(cursor_class=MySQLCursorDict)
    cursor.execute('''
        SELECT skilltmpid,data_value
        FROM skills_tmp
        WHERE scale_name='Importance'
    ''')
    rows = cursor.fetchall()
    for row in rows:
        return_value.append(row)
    return return_value

def get_knowl_tmp_final():
    return_value=[]
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(cursor_class=MySQLCursorDict)
    cursor.execute('''
    SELECT
        onetsoc_code,
        title,
		element_name,
		importance_value,
		level_value,
		description
	FROM onet.knowledge_tmp;
    ''')
    rows = cursor.fetchall()
    for row in rows:
        return_value.append(row)
    return return_value

def get_skill_tmp_final():
    return_value=[]
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(cursor_class=MySQLCursorDict)
    cursor.execute('''
    SELECT
        onetsoc_code,
        title,
		element_name,
		importance_value,
		level_value,
		description
	FROM onet.skills_tmp;
    ''')
    rows = cursor.fetchall()
    for row in rows:
        return_value.append(row)
    return return_value

def create_temp_tables():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(cursor_class=MySQLCursorDict)
    cursor.callproc("create_temp_table")
    connection.commit()
    cursor.close()
    connection.close()


def update_knowledge_tmp(importance_values):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(cursor_class=MySQLCursorDict)
    data_to_insert = ()
    update_sql = "UPDATE knowledge_tmp SET importance_value=%s WHERE knowltmpid=%s;"
    cnt = 0
    for imp_val in importance_values:
        data_to_insert =(imp_val['data_value'],imp_val['knowltmpid']+1)

        cursor.execute(update_sql, data_to_insert)
        cnt += 1
        if cnt % buf_size == 0:
            connection.commit()
    connection.commit()
    cursor.close()
    connection.close()

def update_skills_tmp(importance_values):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(cursor_class=MySQLCursorDict)
    data_to_insert = ()
    update_sql = "UPDATE skills_tmp SET importance_value=%s WHERE skilltmpid=%s;"
    cnt = 0
    for imp_val in importance_values:
        data_to_insert =(imp_val['data_value'],imp_val['skilltmpid']+1)

        cursor.execute(update_sql, data_to_insert)
        cnt += 1
        if cnt % buf_size == 0:
            connection.commit()
    connection.commit()
    cursor.close()
    connection.close()

def trim_knowledge_tmp(ids_to_delete):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(cursor_class=MySQLCursorDict)
    data_to_insert = ()
    update_sql = "DELETE FROM knowledge_tmp WHERE knowltmpid=%s;"
    cnt=0
    for imp_val in ids_to_delete:
        data_to_insert =[imp_val['knowltmpid']]

        cursor.execute(update_sql, data_to_insert)
        cnt += 1
        if cnt % buf_size == 0:
            connection.commit()
    connection.commit()
    cursor.close()
    connection.close()

def trim_skills_tmp(ids_to_delete):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(cursor_class=MySQLCursorDict)
    data_to_insert = ()
    update_sql = "DELETE FROM skills_tmp WHERE skilltmpid=%s;"
    cnt=0
    for imp_val in ids_to_delete:
        data_to_insert =[imp_val['skilltmpid']]

        cursor.execute(update_sql, data_to_insert)
        cnt += 1
        if cnt % buf_size == 0:
            connection.commit()
    connection.commit()
    cursor.close()
    connection.close()

pp = pprint.PrettyPrinter(indent=3)
buf_size = 500

'''
create_temp_tables()
imp_vals = get_knowledge_importance_values()
update_knowledge_tmp(imp_vals)
trim_knowledge_tmp(imp_vals)
imp_vals = get_skills_importance_values()
update_skills_tmp(imp_vals)
trim_skills_tmp(imp_vals)
'''
write_xlsx_file('file.xlsx')