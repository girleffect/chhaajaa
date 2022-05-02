import os

from click import command
from helpers.arg import command_line_args

os.environ["API_KEY"] = command_line_args.api_key
os.environ["BASE_URL"] = command_line_args.base_url

from helpers.connector import Warehouse
from helpers.utility_helpers import general
import pandas as pd
from api.rapidpro import pyRapid
import json
from helpers.date_formatter import format_date

if __name__ == '__main__':
	try:
		warehouse = Warehouse()
		if command_line_args.start_time and command_line_args.end_time:
			print(f"Using start and end time from user input")
			start_time = format_date(command_line_args.start_time, b'start_date')
			end_time = format_date(command_line_args.end_time, b'end_date')
		else:
			print(f"Using start and end time from max date")
			max_date = warehouse.query('SQL/MaxDates/get_max_cont_t.sql',command_line_args.org_id)
			start_time= max_date[b'start_date']
			end_time = max_date[b'end_date']
		print("Running rpp_ftbl_contacts_contactgroupcount for start date, end date and org id",start_time,end_time,command_line_args.org_id)
		cont_group = pyRapid.rpp_ftbl_contacts_contactgroupcount.get_contact_group_count(before=end_time, after=start_time)
		warehouse.drop('staging_rpp_ftbl_contacts_contactgroupcount')

		if general.is_not_empty(cont_group):
			warehouse.load(cont_group,'staging_rpp_ftbl_contacts_contactgroupcount', "replace")
			warehouse.update(file_name='SQL/Analytic/rpp_ftbl_contacts_contactgroupcount_update.sql')
			warehouse.drop('staging_rpp_ftbl_contacts_contactgroupcount')

	except Exception as e:
		raise
