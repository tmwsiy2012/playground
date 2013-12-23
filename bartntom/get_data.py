__author__ = 'tmwsiy'
import mysql.connector
from conf.config import db_config
import pprint

class MySQLCursorDict(mysql.connector.cursor.MySQLCursorBuffered):
    def _row_to_python(self, rowdata, desc=None):
        row = super(MySQLCursorDict, self)._row_to_python(rowdata, desc)
        if row:
            return dict(zip(self.column_names, row))
        return None

def get_knowledge():
    return_value=[]
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(cursor_class=MySQLCursorDict)
    cursor.execute('''
    SELECT
        od.bls_code,
        od.title,
		cmr.element_name,
		sr.scale_name,
		k.data_value,
		cmr.description,
        k.*,
        cmr.*
    FROM
        onet.occupation_data od
        INNER join knowledge k on od.onetsoc_code=k.onetsoc_code
        INNER JOIN content_model_reference cmr on cmr.element_id=k.element_id
		INNER JOIN scales_reference sr ON k.scale_id=sr.scale_id

    WHERE
    od.onetsoc_code like '%.00'
    AND k.onetsoc_code like '%.00'
	AND recommend_suppress='N'
	AND od.bls_code IN (SELECT distinct s.occupation_code
                        FROM
                            bls_oe.series s
                        WHERE
                            s.area_code='2800000'
                            AND s.occupation_code!='000000')
    ORDER by od.onetsoc_code,k.element_id
    ''')
    rows = cursor.fetchall()
    for row in rows:
        return_value.append(row)
    return return_value
pp = pprint.PrettyPrinter(indent=3)
pp.pprint(get_knowledge())