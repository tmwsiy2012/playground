SELECT ocd.onetsoc_code, ocd.title, occ.occupation_name
FROM onet_19.occupation_data ocd
	INNER JOIN bls_oe.occupation occ ON REPLACE(LEFT(ocd.onetsoc_code, 7), '-','')=occ.occupation_code;


SELECT *
  FROM onet_19.occupation_data ocd
	INNER JOIN onet_19.knowledge know ON know.onetsoc_code=ocd.onetsoc_code
	INNER JOIN onet_19.content_model_reference cmr ON cmr.element_id=know.element_id;
------------------------------------------------------------------------------------------------
drop table if exists `onet_19`.`tmp_summary`;
CREATE TABLE `onet_19`.`tmp_summary` (
  `onetsoc_code` VARCHAR(10) NOT NULL,
  `title` VARCHAR(150) NOT NULL,
  `element_id` VARCHAR(20) NOT NULL,
  `element_name` VARCHAR(150) NOT NULL,
  `scale_id` VARCHAR(3) NOT NULL,
  `data_value` DECIMAL(5,2) NOT NULL,
  `description` VARCHAR(1500) NOT NULL,
  PRIMARY KEY (`onetsoc_code`,`element_id`))
SELECT ocd.onetsoc_code, ocd.title, know.element_id, cmr.element_name, know.scale_id, know.data_value, cmr.description
  FROM onet_19.occupation_data ocd
	INNER JOIN onet_19.knowledge know ON know.onetsoc_code=ocd.onetsoc_code
	INNER JOIN onet_19.content_model_reference cmr ON cmr.element_id=know.element_id
WHERE
  know.scale_id="IM";

ALTER TABLE `onet_19`.`tmp_summary`
DROP COLUMN `scale_id`,
CHANGE COLUMN `data_value` `importance_value` DECIMAL(5,2) NOT NULL ;

ALTER TABLE `onet_19`.`tmp_summary`
ADD COLUMN `level_value` DECIMAL(5,2) NULL AFTER `importance_value`;

UPDATE tmp_summary tmp
SET level_value =
(
  SELECT data_value
    from onet_19.knowledge know
    where
    know.element_id=tmp.element_id
    AND
    know.onetsoc_code=tmp.onetsoc_code
    AND
    scale_id='LV'
);

-------------------------------------------------------------------------
drop table if exists `onet_19`.`tmp_summary`;
CREATE TABLE `onet_19`.`tmp_summary` (
  `onetsoc_code` VARCHAR(10) NOT NULL,
  `title` VARCHAR(150) NOT NULL,
  `element_id` VARCHAR(20) NOT NULL,
  `element_name` VARCHAR(150) NOT NULL,
  `scale_id` VARCHAR(3) NOT NULL,
  `data_value` DECIMAL(5,2) NOT NULL,
  `description` VARCHAR(1500) NOT NULL,
  PRIMARY KEY (`onetsoc_code`,`element_id`))
SELECT ocd.onetsoc_code, ocd.title, cmr.element_id, cmr.element_name, skill.scale_id, skill.data_value, cmr.description
  FROM onet_19.occupation_data ocd
	INNER JOIN onet_19.skills skill ON skill.onetsoc_code=ocd.onetsoc_code
	INNER JOIN onet_19.content_model_reference cmr ON cmr.element_id=skill.element_id
WHERE
  skill.scale_id="IM";

  ALTER TABLE `onet_19`.`tmp_summary`
DROP COLUMN `scale_id`,
CHANGE COLUMN `data_value` `importance_value` DECIMAL(5,2) NOT NULL ;

ALTER TABLE `onet_19`.`tmp_summary`
ADD COLUMN `level_value` DECIMAL(5,2) NULL AFTER `importance_value`;

UPDATE tmp_summary tmp
SET level_value =
(
  SELECT data_value
    from onet_19.skills skill
    where
    skill.element_id=tmp.element_id
    AND
    skill.onetsoc_code=tmp.onetsoc_code
    AND
    scale_id='LV'
);