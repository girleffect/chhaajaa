
SELECT max(modified_on) - 1 as start_date, CURRENT_TIMESTAMP as end_date FROM rappidpro.rpp_ftbl_flows_flowrun where org_id={};
