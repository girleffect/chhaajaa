SELECT max(modified_on)  as start_date, CURRENT_TIMESTAMP as end_date FROM rappidpro.rpp_ftbl_msgs_msg where org_id={};
