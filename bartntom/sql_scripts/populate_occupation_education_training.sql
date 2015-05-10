LOAD DATA INFILE 'C:/Users/tmwsiy/Downloads/occupation.txt'
	INTO TABLE education_training_assignments FIELDS TERMINATED BY '\t'
	LINES TERMINATED BY '\r\n'  IGNORE 1 LINES
	(title, soc_code, education, experience, on_the_job_training);