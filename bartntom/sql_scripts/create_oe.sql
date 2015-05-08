CREATE DATABASE `bls_oe` /*!40100 DEFAULT CHARACTER SET utf8 */$$

delimiter $$

  use bls_oe;

CREATE TABLE `alldata` (
  `idalldata` int(11) NOT NULL AUTO_INCREMENT,
  `series_id` varchar(30) NOT NULL,
  `year` varchar(4) NOT NULL,
  `period` varchar(3) NOT NULL,
  `value` varchar(12) NOT NULL,
  `footnote_codes` varchar(10) NOT NULL,
  PRIMARY KEY (`idalldata`),
  KEY `seriesid` (`series_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5846041 DEFAULT CHARSET=utf8$$

delimiter $$

CREATE TABLE `area` (
  `idarea` int(11) NOT NULL AUTO_INCREMENT,
  `area_code` varchar(7) NOT NULL,
  `areatype_code` varchar(1) NOT NULL,
  `area_name` varchar(100) NOT NULL,
  PRIMARY KEY (`idarea`),
  KEY `area_code` (`area_code`)
) ENGINE=InnoDB AUTO_INCREMENT=642 DEFAULT CHARSET=utf8$$

delimiter $$

CREATE TABLE `areatype` (
  `idareatype` int(11) NOT NULL AUTO_INCREMENT,
  `areatype_code` varchar(1) NOT NULL,
  `areatype_name` varchar(100) NOT NULL,
  PRIMARY KEY (`idareatype`),
  KEY `areatype_code` (`areatype_code`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8$$

delimiter $$

CREATE TABLE `datatype` (
  `iddatatype` int(11) NOT NULL AUTO_INCREMENT,
  `datatype_code` varchar(2) NOT NULL,
  `datatype_name` varchar(100) NOT NULL,
  `footnote_code` varchar(1) NOT NULL,
  PRIMARY KEY (`iddatatype`),
  KEY `datatype_code` (`datatype_code`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8$$

delimiter $$

CREATE TABLE `footnote` (
  `idfootnote` int(11) NOT NULL AUTO_INCREMENT,
  `footnote_code` varchar(1) NOT NULL,
  `footnote_text` varchar(250) NOT NULL,
  PRIMARY KEY (`idfootnote`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8$$

delimiter $$

CREATE TABLE `industry` (
  `idindustry` int(11) NOT NULL AUTO_INCREMENT,
  `industry_code` varchar(6) NOT NULL,
  `industry_name` varchar(100) NOT NULL,
  `display_level` varchar(2) NOT NULL,
  `selectable` varchar(1) NOT NULL,
  `sort_sequence` varchar(5) NOT NULL,
  PRIMARY KEY (`idindustry`),
  KEY `industry_code` (`industry_code`)
) ENGINE=InnoDB AUTO_INCREMENT=491 DEFAULT CHARSET=utf8$$

delimiter $$

CREATE TABLE `occugroup` (
  `idoccugroup` int(11) NOT NULL AUTO_INCREMENT,
  `occugroup_code` varchar(6) NOT NULL,
  `occugroup_name` varchar(100) NOT NULL,
  PRIMARY KEY (`idoccugroup`),
  KEY `occugroup_code` (`occugroup_code`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8$$

delimiter $$

CREATE TABLE `occupation` (
  `idoccupation` int(11) NOT NULL AUTO_INCREMENT,
  `occupation_code` varchar(6) NOT NULL,
  `occupation_name` varchar(100) NOT NULL,
  `display_level` varchar(1) NOT NULL,
  `selectable` varchar(1) NOT NULL,
  `sort_sequence` varchar(5) NOT NULL,
  PRIMARY KEY (`idoccupation`),
  KEY `occupation_code` (`occupation_code`)
) ENGINE=InnoDB AUTO_INCREMENT=1090 DEFAULT CHARSET=utf8$$

delimiter $$

CREATE TABLE `oe_release` (
  `idrelease` int(11) NOT NULL AUTO_INCREMENT,
  `release_date` varchar(7) NOT NULL,
  `description` varchar(50) NOT NULL,
  PRIMARY KEY (`idrelease`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8$$

delimiter $$

CREATE TABLE `seasonal` (
  `idseasonal` int(11) NOT NULL AUTO_INCREMENT,
  `seasonal` varchar(1) NOT NULL,
  `seasonal_text` varchar(30) NOT NULL,
  PRIMARY KEY (`idseasonal`),
  KEY `seasonal` (`seasonal`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8$$

delimiter $$

CREATE TABLE `sector` (
  `idsector` int(11) NOT NULL AUTO_INCREMENT,
  `sector_code` varchar(6) NOT NULL,
  `sector_name` varchar(100) NOT NULL,
  PRIMARY KEY (`idsector`),
  KEY `sector_code` (`sector_code`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8$$

delimiter $$

CREATE TABLE `series` (
  `idseries` int(11) NOT NULL AUTO_INCREMENT,
  `series_id` varchar(30) NOT NULL,
  `seasonal` varchar(1) NOT NULL,
  `areatype_code` varchar(1) NOT NULL,
  `area_code` varchar(7) NOT NULL,
  `industry_code` varchar(6) NOT NULL,
  `occupation_code` varchar(6) NOT NULL,
  `datatype_code` varchar(6) NOT NULL,
  `footnote_codes` varchar(2) NOT NULL,
  `begin_year` varchar(4) NOT NULL,
  `begin_period` varchar(3) NOT NULL,
  `end_year` varchar(4) NOT NULL,
  `end_period` varchar(3) NOT NULL,
  PRIMARY KEY (`idseries`),
  KEY `seriesid` (`series_id`),
  KEY `area_code` (`area_code`)
) ENGINE=InnoDB AUTO_INCREMENT=5846041 DEFAULT CHARSET=utf8$$

delimiter $$

CREATE TABLE `statemsa` (
  `idstatemsa` int(11) NOT NULL AUTO_INCREMENT,
  `state_code` varchar(2) NOT NULL,
  `msa_code` varchar(7) NOT NULL,
  `msa_name` varchar(100) NOT NULL,
  PRIMARY KEY (`idstatemsa`),
  KEY `state_code` (`state_code`)
) ENGINE=InnoDB AUTO_INCREMENT=648 DEFAULT CHARSET=utf8$$