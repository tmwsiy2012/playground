delimiter $$
CREATE DATABASE `onet_career_changers` /*!40100 DEFAULT CHARACTER SET utf8 */$$
  use onet_career_changers;

  CREATE TABLE `related_occupations` (
  `reloccid` int(11) NOT NULL AUTO_INCREMENT,
  `target_code` varchar(10) NOT NULL,
  `target_title` varchar(200) NOT NULL,
  `change_code` varchar(10) NOT NULL,
  `change_title` varchar(200) NOT NULL,
  `starter_code` varchar(10) NOT NULL,
  `starter_title` varchar(200) NOT NULL,
  PRIMARY KEY (`reloccid`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
