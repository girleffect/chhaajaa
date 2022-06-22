DELETE FROM rappidpro.rpp_ftbl_contact
USING rappidpro.staging_rpp_ftbl_contact
WHERE rpp_ftbl_contact.uuid = staging_rpp_ftbl_contact.uuid
and rpp_ftbl_contact.uuid is not null and staging_rpp_ftbl_contact.uuid is not null;