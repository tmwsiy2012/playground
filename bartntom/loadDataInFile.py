import mysql.connector
import os

connection = mysql.connector.connect(host='localhost', user='root', passwd='tr45sh32', db='bls_qcew')
cursor = connection.cursor()
for dirname, dirnames, filenames in os.walk('C:\\Users\\tmwsiy\\Downloads\\data\\'):
    for filename in filenames:
        if "annual" in filename and filename.endswith(".csv"):
            print(filename)
            query = "LOAD DATA INFILE '" + os.path.join(dirname, filename).replace("\\", "\\\\") + "' INTO TABLE annual_data FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' LINES TERMINATED BY '\n' STARTING BY ''  IGNORE 1 LINES (area_fips,own_code,industry_code,agglvl_code,size_code,year,qtr,disclosure_code,annual_avg_estabs_count,annual_avg_emplvl,total_annual_wages,taxable_annual_wages,annual_contributions,annual_avg_weekly_rate,avg_annual_pay)"
            cursor.execute( query )            
            connection.commit()
        if "q1-" in filename and filename.endswith(".csv"):
            print(filename)
            query = "LOAD DATA INFILE '" + os.path.join(dirname, filename).replace("\\", "\\\\") + "' INTO TABLE quarterly_data FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"'  LINES TERMINATED BY '\n' STARTING BY ''  IGNORE 1 LINES (area_fips,own_code,industry_code,agglvl_code,size_code,year,qtr,disclosure_code,quarterly_estabs_count,month1_emplvl,month2_emplvl,month3_emplvl,total_qtrly_wages,taxable_qtrly_wages,qtrly_contributions,avg_wkly_wage)"
            cursor.execute( query )            
            connection.commit()
