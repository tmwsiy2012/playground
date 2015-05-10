LOAD DATA INFILE 'C:/Users/tmwsiy/Downloads/Related_AppD.txt'
	INTO TABLE related_occupations FIELDS TERMINATED BY '\t'
	LINES TERMINATED BY '\r\n'  IGNORE 1 LINES
	(target_code, target_title, change_code, change_title, starter_code, starter_title);