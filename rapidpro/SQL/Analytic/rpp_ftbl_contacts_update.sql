INSERT INTO rappidpro.rpp_ftbl_contact
SELECT 
       cast(is_active as bigint),
       created_on,
       modified_on,
       cast(uuid as VARCHAR(36)),
       cast(name as VARCHAR(128)),
       cast(blocked as bigint) as is_blocked,
       cast(is_test as bigint),
       cast(stopped as bigint) as is_stopped,
       cast(language  as VARCHAR(3)),
       cast(created_by_id as int8),
       cast(modified_by_id as int8),
       cast(org_id as int8),
       cast(fields as VARCHAR(65535)),
       cast(id as bigint)
FROM rappidpro.staging_rpp_ftbl_contact as a;