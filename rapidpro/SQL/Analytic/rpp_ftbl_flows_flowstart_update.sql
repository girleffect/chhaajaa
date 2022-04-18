INSERT INTO rappidpro.rpp_ftbl_flows_flowstart
SELECT
    id,
    cast(is_active as bigint),
    created_on,
    modified_on,
    restart_participants,
    contact_count,
    cast(status as varchar(1)),
    cast(extra as varchar(65535)),
    created_by_id,
    flow_id,
    modified_by_id,
    cast(include_active as bigint),
    cast(uuid as varchar(65535))
FROM rappidpro.staging_rpp_ftbl_flows_flowstart;
