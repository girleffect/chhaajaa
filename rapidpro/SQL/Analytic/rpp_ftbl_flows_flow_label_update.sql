INSERT INTO rappidpro.rpp_ftbl_flows_flow_labels
SELECT 
cast(id as bigint),
cast(uuid as VARCHAR(15540)),
name,
cast(count as int8)
FROM rappidpro.staging_rpp_ftbl_flows_flow_label;