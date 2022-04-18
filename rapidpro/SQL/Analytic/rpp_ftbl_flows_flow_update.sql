INSERT INTO rappidpro.rpp_ftbl_flows_flow
SELECT 
       cast(is_active as bigint),
       created_on,
       modified_on,
       uuid,
       name,
       entry_uuid,
       entry_type,
       cast(is_archived as bigint),
       flow_type,
       metadata,
       expires_after_minutes,
       cast(ignore_triggers as bigint),
       cast(saved_on as timestamp),
       cast(base_language  as VARCHAR(3)),
       version_number,
       cast(created_by_id as int8),
       cast(modified_by_id as int8),
       cast(org_id as int8),
       saved_by_id,
       id
FROM rappidpro.staging_rpp_ftbl_flows_flow as a;