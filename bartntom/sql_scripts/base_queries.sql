SELECT ocd.onetsoc_code, ocd.title, occ.occupation_name
FROM onet_19.occupation_data ocd
	INNER JOIN bls_oe.occupation occ ON REPLACE(LEFT(ocd.onetsoc_code, 7), '-','')=occ.occupation_code;


	SELECT *
  FROM onet_19.occupation_data ocd
	INNER JOIN onet_19.knowledge know ON know.onetsoc_code=ocd.onetsoc_code
	INNER JOIN onet_19.skills skill ON skill.onetsoc_code=ocd.onetsoc_code;

		SELECT *
  FROM onet_19.occupation_data ocd
	INNER JOIN onet_19.knowledge know ON know.onetsoc_code=ocd.onetsoc_code
	INNER JOIN onet_19.skills skill ON skill.onetsoc_code=ocd.onetsoc_code
	INNER JOIN onet_19.content_model_reference cmr ON cmr.element_id=ocd.element_id;