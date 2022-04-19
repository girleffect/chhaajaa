import os

from click import command
from helpers.kslack import command_line_args, post_message

os.environ["API_KEY"] = command_line_args.api_key
os.environ["BASE_URL"] = command_line_args.base_url

from helpers.connector import Warehouse
from api.rapidpro import pyRapid
from helpers.utility_helpers import general
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
			start_time = max_date[b'start_date']
			end_time = max_date[b'end_date']

		contacts = pyRapid.rpp_ftbl_contact.get_contacts(before=end_time, after=start_time, org_id=command_line_args.org_id)
		warehouse.drop('staging_rpp_ftbl_contact')

		if general.is_not_empty(contacts):	
			warehouse.load(contacts,'staging_rpp_ftbl_contact', "replace")
			warehouse.update(file_name="SQL/Conflicts/rpp_ftbl_contacts_conflict.sql")
			warehouse.update(file_name='SQL/Analytic/rpp_ftbl_contacts_update.sql')
			warehouse.drop('staging_rpp_ftbl_contact')
			post_message(message=f'rpp_ftbl_contact table ran successfull. {contacts.shape[0]} rows updated', channel="ds-spam")
		else:
			post_message(message=f'rpp_ftbl_contact table ran successfull. No rows updated', channel="ds-spam")
	except Exception as e:
		post_message(message=f'rpp_ftbl_contact.py failed: {e}', channel="ds-errors")
		raise

