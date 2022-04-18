import inspect
import json
import os

from helpers.config_files import __configpath__ #pointer to reliably get path to config file
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, From, To, Subject, Content, MimeType)

class SendGridMailer(object):

	def __init__(self, config_file_name = "config.json"):
		CONFIG_FILE_NAME = config_file_name
		CONFIG_ABS_FILE_DIR_PATH = os.path.dirname(inspect.getabsfile(__configpath__))
		with open(os.path.join(CONFIG_ABS_FILE_DIR_PATH, CONFIG_FILE_NAME)) as config_file:
			config_data = json.load(config_file)
			config_data = config_data.get("sendGridConfig", {})

		self.message = Mail()
		self.sendgrid_api_key = config_data.get("apiKey", None)
		self.send_grid = SendGridAPIClient(self.sendgrid_api_key)
		self.from_email = config_data.get("fromEmail", None)
		self.to_emails = self._proccess_string_to_emails(config_data.get("toEmails") if config_data.get("toEmails") != None else [])
		self.subject = config_data.get("subject", None)
		self.content = None
		self.html_content = None

		if self.from_email is not None:
			self.set_from_email(self.from_email)
		if self.to_emails:
			self.set_to_emails(self.to_emails)
		if self.subject is not None:
			self.set_subject(self.subject)

	def set_from_email(self, from_email):
		if from_email is None:
			return

		if type(from_email) is str:
			self.from_email = from_email
			self.message.from_email = From(from_email)
		else:
			return

	def set_to_emails(self, to_emails):
		if not to_emails:
			return

		if type(to_emails) is list:
			self.to_emails = []
			to_email_list = []
			for to_email in to_emails:
				self.to_emails.append(to_email)
				to_email_list.append(To(to_email))
			self.message.to = to_email_list
		else:
			return

	def set_subject(self, subject):
		if subject is None:
			return

		self.subject = subject
		self.message.subject = Subject(subject)

	def set_content(self, content):
		if content is None:
			return

		if self.html_content is not None:
			self,html_content = None

		self.content = content
		self.message.content = Content(MimeType.text, content)

	def set_html_content(self, html_content):
		if html_content is None:
			return

		if self.content is not None:
			self.content = None

		self.html_content = html_content
		self.message.content = Content(MimeType.html, html_content)

	def send_email(self):
		if self.sendgrid_api_key is None:
			return
		if self.from_email is None:
			return
		if self.to_emails is None:
			return

		try:
			response = self.send_grid.send(self.message)
		except Exception as e:
			return

	@staticmethod
	def _proccess_string_to_emails(to_emails):
		if to_emails is None:
			return

		if type(to_emails) is str:
			to_email_list = to_emails.split(',')
			return [x.strip(' ') for x in to_email_list]
		else:
			return
