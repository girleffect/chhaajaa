DELETE FROM rappidpro.staging_rpp_rpp_ftbl_msgs_msg 
USING rappidpro.rpp_ftbl_msgs_msg 
WHERE rpp_ftbl_msgs_msg.id = staging_rpp_rpp_ftbl_msgs_msg.id;