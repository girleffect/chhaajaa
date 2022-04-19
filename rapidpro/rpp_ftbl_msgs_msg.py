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
			max_date = warehouse.query('SQL/MaxDates/get_max_msg.sql')
			start_time= max_date[b'start_date']
			end_time = max_date[b'end_date']
		msgs = pyRapid.rpp_ftbl_msgs_msg.get_messages(before=end_time, after=start_time, org_id=command_line_args.org_id)
		warehouse.drop('staging_rpp_rpp_ftbl_msgs_msg') 

		if general.is_not_empty(msgs):	
			warehouse.load(msgs,'staging_rpp_rpp_ftbl_msgs_msg', "replace")
			warehouse.update(file_name="SQL/Conflicts/rpp_rpp_ftbl_msgs_msg_conflict.sql")
			warehouse.update(file_name='SQL/Analytic/rpp_ftbl_msgs_msg_update.sql')
			warehouse.drop('staging_rpp_rpp_ftbl_msgs_msg')

			post_message(message=f'rpp_ftbl_msgs_msg table ran successfull. {msgs.shape[0]} rows updated', channel="ds-spam")
		else:
			post_message(message=f'rpp_ftbl_msgs_msg table ran successfull. No rows updated', channel="ds-spam")
	except Exception as e:
		post_message(message=f'rpp_ftbl_msgs_msg.py failed: {e}', channel="ds-errors")
		raise
