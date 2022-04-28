INSERT INTO rappidpro.rpp_ftbl_msgs_broadcast_urns
SELECT  
       cast(id as bigint),
       cast(broadcast_id as int8),
       cast(contacturn_id as int8)
FROM rappidpro.staging_rpp_ftbl_msgs_broadcast_urns as a;