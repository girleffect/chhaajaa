import requests
import argparse

command_line_parser = argparse.ArgumentParser()
command_line_parser.add_argument("-tm", "--test_mode", action="store_true")
command_line_parser.add_argument("-tc", "--temp_channel", type=str, nargs='*')
command_line_parser.add_argument("-s", "--start_time", help="Start date in yyyy-mm-dd", required=False)
command_line_parser.add_argument("-e", "--end_time", help="End date in yyyy-mm-dd", required=False)
command_line_args = command_line_parser.parse_args()

def post_message(message,channel):  
    if command_line_args.test_mode or command_line_args.temp_channel:
        channel = command_line_args.temp_channel or command_line_args.test_mode and 'ds-testing'
        print(f'Posting to slack channel {channel}:\n{message}')
    headers = {
        'Content-type': 'application/json',
    }
    data = str({ "text" : "{0}".format(message) })
    if channel == 'ds-spam':
        url = 'https://hooks.slack.com/services/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'  
    if channel == 'ds-errors':
        url = 'https://praekeltfoundation.slack.com/archives/C02LNFR25NE' 

    response = requests.post(url, headers=headers, data=data)
