DELETE FROM rappidpro.staging_rpp_ftbl_auth_user 
USING rappidpro.rpp_ftbl_auth_user 
WHERE rpp_ftbl_auth_user.email = staging_rpp_ftbl_auth_user.email and rpp_ftbl_auth_user.email = staging_rpp_ftbl_auth_user.email;