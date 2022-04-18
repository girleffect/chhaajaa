
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
			max_date = warehouse.query('SQL/MaxDates/get_max_flowrun.sql')
			start_time= max_date[b'start_date']
			end_time = max_date[b'end_date']

		msgs_broadcast_urns = pyRapid.rpp_ftbl_msgs_broadcast_urns.get_broadcast_urls(before=end_time, after=start_time)
		
		if general.is_not_empty(msgs_broadcast_urns):
			warehouse.load(msgs_broadcast_urns,'staging_rpp_ftbl_msgs_broadcast_urns', "replace")
			warehouse.update(file_name="SQL/Conflicts/rpp_ftbl_msgs_broadcast_urns_conflict.sql")
			warehouse.update(file_name='SQL/Analytic/rpp_ftbl_msgs_broadcast_urns_update.sql')
			warehouse.drop('staging_rpp_ftbl_msgs_broadcast_urns')

			post_message(message=f'rpp_ftbl_msgs_broadcast_urns table ran successfull. {msgs_broadcast_urns.shape[0]} rows updated', channel="ds-spam")
		else:
			post_message(message=f'rpp_ftbl_msgs_broadcast_urns table ran successfull. No rows updated', channel="ds-spam")
	except Exception as e:
		post_message(message=f'rpp_ftbl_msgs_broadcast_urns.py failed: {e}', channel="ds-errors")
		raise 
