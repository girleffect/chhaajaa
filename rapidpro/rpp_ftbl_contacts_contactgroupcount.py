
from helpers.connector import Warehouse
from helpers.kslack import post_message, command_line_args
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
			max_date = warehouse.query('SQL/MaxDates/get_max_cont_t.sql')
			start_time= max_date[b'start_date']
			end_time = max_date[b'end_date']

		cont_group = pyRapid.rpp_ftbl_contacts_contactgroupcount.get_contact_group_count(before=end_time, after=start_time)
		warehouse.drop('staging_rpp_ftbl_contacts_contactgroupcount')

		if general.is_not_empty(cont_group):
			warehouse.load(cont_group,'staging_rpp_ftbl_contacts_contactgroupcount', "replace")
			warehouse.update(file_name='SQL/Analytic/rpp_ftbl_contacts_contactgroupcount_update.sql')
			warehouse.drop('staging_rpp_ftbl_contacts_contactgroupcount')

			post_message(message=f'rpp_ftbl_contacts_contactgroupcount table ran successfull. {cont_group.shape[0]} rows updated', channel="ds-spam")
		else:
			post_message(message=f'rpp_ftbl_contacts_contactgroupcount table ran successfull. No rows updated', channel="ds-spam")
	except Exception as e:
		post_message(message=f'rpp_ftbl_contacts_contactgroupcount.py failed: {e}', channel="ds-errors")
		raise 
