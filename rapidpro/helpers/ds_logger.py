import inspect
import json
import logging
import os
import socket
import traceback

from datetime import date
from helpers.config_files import __configpath__ #pointer to reliably get path to config file
from helpers.sendgrid_mailer import SendGridMailer

mailer = SendGridMailer()

class DSLogger(object):

	def __init__(self, config_file_name = "config.json"):
		CONFIG_FILE_NAME = config_file_name
		CONFIG_ABS_FILE_DIR_PATH = os.path.dirname(inspect.getabsfile(__configpath__))
		with open(os.path.join(CONFIG_ABS_FILE_DIR_PATH, CONFIG_FILE_NAME)) as config_file:
			ds_logger_config_data = json.load(config_file)
			config_data = ds_logger_config_data.get("loggerConfig", {})

		today = date.today()
		# Acceptable value for `level` are: DEBUG, INFO, WARNING, EXCEPTION and ERROR
		self.level = config_data.get("level", None)
		self.storedir = config_data.get("storedir", None)
		self.filename = f"{today.strftime('%d-%b-%Y')}.log"
		self.filemode = config_data.get("filemode", None)
		self.format = config_data.get("format", None)
		self.datefmt = config_data.get("datefmt", None)
		self.logger = logging.getLogger(__name__)

		try:
			hostname = socket.gethostname()    
			ipaddr = socket.gethostbyname(hostname)
			self.islocal = config_data.get("serverIP") != ipaddr if config_data.get("serverIP") != None else True
		except:
			self.islocal = True

		try:
			if not os.path.exists(self.storedir):
				os.makedirs(self.storedir)
		except OSError as e:
			if e.errno != errno.EEXIST:
				self.log_error(f"Error occured on creating logs folder. Exception: {e}")
				raise

		logging.basicConfig(filename= f"{self.storedir}{self.filename}",
							format= self.format,
							datefmt= self.datefmt)

		#If level is not set in config then it will default the log level to WARNING
		if self.level.lower() == "debug":
			self.logger.setLevel(logging.DEBUG)
		if self.level.lower() == "info":
			self.logger.setLevel(logging.INFO)
		if self.level.lower() == "warning":
			self.logger.setLevel(logging.WARNING)
		if self.level.lower() == "exception":
			self.logger.setLevel(logging.EXCEPTION)
		if self.level.lower() == "error":
			self.logger.setLevel(logging.ERROR)
		else:
			self.logger.setLevel(logging.WARNING)

	def log_debug(self, msg, *args, **kwargs):
		trace_back_info = traceback.format_exc()
		proccessed_msg = self._proccess_message(trace_back_info, msg)
		self.logger.debug(trace_back_info, *args, **kwargs)

	def log_info(self, msg, *args, **kwargs):
		trace_back_info = traceback.format_exc()
		proccessed_msg = self._proccess_message(trace_back_info, msg)
		self.logger.info(proccessed_msg, *args, **kwargs)

	def log_warning(self, msg, *args, **kwargs):
		trace_back_info = traceback.format_exc()
		proccessed_msg = self._proccess_message(trace_back_info, msg)
		self.logger.warning(proccessed_msg, *args, **kwargs)

	def log_exception(self, msg, *args, **kwargs):
		trace_back_info = traceback.format_exc()
		proccessed_msg = self._proccess_message(trace_back_info, msg)
		self.logger.exception(proccessed_msg, *args, **kwargs)
		if not self.islocal:
			mailer.set_content(proccessed_msg)
			mailer.send_email()

	def log_error(self, msg, *args, **kwargs):
		trace_back_info = traceback.format_exc()
		proccessed_msg = self._proccess_message(trace_back_info, msg)
		self.logger.error(proccessed_msg, *args, **kwargs)
		if not self.islocal:
			mailer.set_content(proccessed_msg)
			mailer.send_email()

	@staticmethod
	def _proccess_message(trace_back_info, msg):
		return f"{msg}, Traceback Info: [{trace_back_info[0]}]"
