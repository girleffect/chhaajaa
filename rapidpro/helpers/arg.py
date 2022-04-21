import os

import requests
import argparse

command_line_parser = argparse.ArgumentParser()
command_line_parser.add_argument("-tm", "--test_mode", action="store_true")
command_line_parser.add_argument("-tc", "--temp_channel", type=str, nargs='*')
command_line_parser.add_argument("-s", "--start_time", help="Start date in yyyy-mm-dd", required=False)
command_line_parser.add_argument("-e", "--end_time", help="End date in yyyy-mm-dd", required=False)
command_line_parser.add_argument("-id", "--org_id", help="Rapidpro organisation id (int)", required=True)
command_line_parser.add_argument("-k", "--api_key", help="Rapidpro API key value (string).", required=True)
command_line_parser.add_argument("-u", "--base_url", help="Rapidpro base URL value (string).", required=True)
command_line_args = command_line_parser.parse_args()
