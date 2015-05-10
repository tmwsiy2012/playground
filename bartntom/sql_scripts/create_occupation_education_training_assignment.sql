delimiter $$
CREATE DATABASE `bls_empl_project` /*!40100 DEFAULT CHARACTER SET utf8 */$$
  use bls_empl_project;

  CREATE TABLE `education_training_assignments` (
  `edutraassid` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(150) NOT NULL,
  `soc_code` varchar(7) NOT NULL,
  `education` varchar(45) NOT NULL,
  `experience` varchar(45) NOT NULL,
  `on_the_job_training` varchar(45) NOT NULL,
  PRIMARY KEY (`edutraassid`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;


