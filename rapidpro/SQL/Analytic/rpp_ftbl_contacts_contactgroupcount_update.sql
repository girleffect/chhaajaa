INSERT INTO rappidpro.rpp_ftbl_contacts_contactgroupcount
SELECT 
       cast(count as int8),
       group_id,
       cast(is_squashed as bigint),
       cast(id as bigint)
FROM rappidpro.staging_rpp_ftbl_contacts_contactgroupcount as a;