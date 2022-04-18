
SELECT max(last_login) - 1 as start_date, CURRENT_TIMESTAMP as end_date FROM rappidpro.rpp_ftbl_auth_user;
