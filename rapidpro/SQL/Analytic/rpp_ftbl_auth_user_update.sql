INSERT INTO rappidpro.rpp_ftbl_auth_user
SELECT 
       last_login,
       cast(is_superuser as bigint),
       username,
       first_name,
       last_name,
       email,
       cast(is_staff as bigint),
       cast(is_active as bigint),
       cast(date_joined as timestamp),
       id
FROM rappidpro.staging_rpp_ftbl_auth_user;