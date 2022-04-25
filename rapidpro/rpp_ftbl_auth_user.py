import os

from click import command
from helpers.arg import command_line_args

os.environ["API_KEY"] = command_line_args.api_key
os.environ["BASE_URL"] = command_line_args.base_url

from helpers.connector import Warehouse
from helpers.utility_helpers import general
from helpers.date_formatter import format_date
import pandas as pd
from api.rapidpro import pyRapid
import json

if __name__ == '__main__':
	try:
		warehouse = Warehouse()
		if command_line_args.start_time and command_line_args.end_time:
			print(f"Using start and end time from user input")
			start_time = format_date(command_line_args.start_time, b'start_date')
			end_time = format_date(command_line_args.end_time, b'end_date')
		else:
			print(f"Using start and end time from max date")
			max_date = warehouse.query('SQL/MaxDates/get_max_auth_user.sql')
			start_time = max_date[b'start_date']
			end_time = max_date[b'end_date']
        
        print("Running rpp_ftbl_auth_user for start date and end date",start_time,end_time)
		auth_user = pyRapid.rpp_ftbl_auth_user.get_auth_users(before=end_time, after=start_time)
		warehouse.drop('staging_rpp_ftbl_auth_user')

		if general.is_not_empty(auth_user):
			warehouse.load(auth_user,'staging_rpp_ftbl_auth_user', "replace")
			warehouse.update(file_name="SQL/Conflicts/rpp_ftbl_auth_user_conflict.sql")
			warehouse.update(file_name='SQL/Analytic/rpp_ftbl_auth_user_update.sql')
			warehouse.drop('staging_rpp_ftbl_auth_user')

	except Exception as e:
		raise
