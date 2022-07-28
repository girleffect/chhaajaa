DELETE FROM rappidpro.staging_rpp_ftbl_flows_flow 
USING rappidpro.rpp_ftbl_flows_flow 
WHERE staging_rpp_ftbl_flows_flow.uuid = rpp_ftbl_flows_flow.uuid and rpp_ftbl_flows_flow.uuid is not null and staging_rpp_ftbl_flows_flow.uuid is not null
and staging_rpp_ftbl_flows_flow.org_id=rpp_ftbl_flows_flow.org_id;