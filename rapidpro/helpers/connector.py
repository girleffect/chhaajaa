import base64
import json
import os
import pandas as pd
import codecs


from helpers.ds_logger import DSLogger
from sqlalchemy import create_engine,types
import redshift_connector
import sqlalchemy as sa


logger = DSLogger()

class Connect(object):

	def __init__(self):
		self.db = None
		self.server = None
		self.pw = None
		self.user = None
		self.conn = None
		self.sql = None
		self.headers = None

	def __str__(self):
		return f'Connection name: {self.name}'

class SQlServer(Connect):
	
	def __init__(self):
		
		Connect.__init__(self)
		self.db = os.environ.get('trgDbServer_db')
		self.server = os.environ.get('trgDbServer')
		self.pw = os.environ.get('trgDbPassword')
		self.user = os.environ.get('trgDbUserName')
		self.enc = os.environ.get('PYTHONIOENCODING')

	def connect(self):
		try:
			if self.db is None or self.db == "":
				raise OSError
			if self.server is None or self.server == "":
				raise OSError
			if self.user is None or self.user == "":
				raise OSError
			if self.pw is None or self.pw == "":
				raise OSError

			try:
				
				self.conn = redshift_connector.connect(host=self.server,database=self.db,user=self.user,password=self.pw)
				logger.log_info(f'Successfully connected to {self.db}.')
				logger.log_info("connected with redshift_connector")
				return None

			except Exception as e:
				logger.log_info(f'Connection error with redshift_connector: {e}')
				try:
					self.conn = redshift_connector.connect(host=self.server,database=self.db,user=self.user,password=self.pw)          
					logger.log_info(f'Successfully connected to {self.db}.')
					logger.log_info("connected with redshift_connector")
					return None

				except Exception as e:
					logger.log_error(f'Connection error with redshift_connector: {e}')
					raise
		except OSError as e:
			logger.log_error(f"Check if trgDbServer_db, trgDbServer, trgDbPassword and trgDbUserName environment variables are all set. Or are you using MCA or DEV settings.")
			raise

	def open_query(self, file_name):
		try:
			file = os.path.realpath(file_name)
			with open(file, 'r') as sqlFile:
				self.sql = sqlFile.read()
				
			return self.sql
		except Exception as e:
			logger.log_error(f"Filename: {file_name}. File stream error: {e}")
			raise

	def execute(self, temp):
		if temp == False:
			self.connect()
		else:
			logger.log_info('Already Connected.')
			
		try:
			with self.conn.cursor() as curr:
				curr.execute(self.sql)
				self.headers = [desc[0] for desc in curr.description]
				fet = curr.fetchall()
				if fet:
					res = pd.DataFrame.from_records(fet)
					res.columns = self.headers
					logger.log_info('Successfully fetched results.')
					return res
				else:
					logger.log_info('No results returned from query.')
					return None

		except Exception as e:
			logger.log_error(f'Query error: {e}')
			raise
		finally:
			curr.close()
			self.conn.close()
			logger.log_info(f'Closed connection to {self.db}.')

	def query(self, file_name, temp = False, *param):
		# This function does not validate order of the format
		# Please ensure param orders are correct
		# Else the result will not be correct
		self.open_query(file_name=file_name)
		try:
			self.sql = self.sql.format(*param)

		except Exception as e:
			logger.log_error(f'Query format error: {e}')
			raise
		
		res = self.execute(temp)

		return res

	def create_temp(self, file_name, *param):
		self.open_query(file_name=file_name)

		try:
			self.sql = self.sql.format(*param)

		except Exception as e:
			logger.log_error(f'Query format error: {e}')
			raise
			
		try:
			with self.conn.cursor() as curr:
				curr.execute(self.sql)
				self.conn.commit()
				logger.log_info('No results returned from query.')
				return None

		except Exception as e:
			logger.log_error(f'Query error: {e}')
			raise

	def disconnect(self):
		try:
			self.conn.close()
			logger.log_info(f'Closed connection to {self.db}.')

			return None

		except Exception as e:
			logger.log_error(f'Connection error: {e}')
			raise

class Warehouse(Connect):
	
	def __init__(self):
		
		Connect.__init__(self)
		self.db = os.environ.get('trgDbServer_db')
		self.server = os.environ.get('trgDbServer')
		self.pw = os.environ.get('trgDbPassword')
		self.user = os.environ.get('trgDbUserName')
		self.port = os.environ.get('trgDbServer_port')
		self.eng_url_redshift = os.environ.get('eng_url_redshift')
		self.db_en = os.environ.get('trgDbServer_db_eng=')

	def connect(self):
		try:
			self.conn = redshift_connector.connect(host=self.server,database=self.db,user=self.user,password=self.pw)
			logger.log_info(f'Successfully connected to {self.db}.')

			return None

		except Exception as e:
			logger.log_error(f'Connection error: {e}')
			raise

	def open_query(self, file_name):
		try:
			file = os.path.realpath(file_name)
			with open(file, 'r') as sqlFile:
				self.sql = sqlFile.read()

			return self.sql

		except Exception as e:
			logger.log_error(f"Filename: {file_name}. File stream error: {e}")
			raise

	def execute(self):
		self.connect()

		try:
			with self.conn.cursor() as curr:
				curr.execute(self.sql)
				self.headers = [desc[0] for desc in curr.description]
				fet = curr.fetchall()
				if fet:
					res = pd.DataFrame(fet)
					res.columns = self.headers
					logger.log_info('Successfully fetched results.')
					return res
				else:
					logger.log_info('No results returned from query.')
					return None

		except Exception as e:
			logger.log_error(f'Query error: {e}')
			raise

		finally:
			curr.close()
			self.conn.close()
			logger.log_info(f'Closed connection to {self.db}.')
			
	def load(self, dataframe, table_name, if_exists):
		self.disposition = 'load'
		if if_exists is not None:
			self.write_disposition = if_exists

		self.engine = create_engine(
			f'postgresql+psycopg2://{self.user}:{self.pw}@{self.server}:{self.port}/{self.db}',client_encoding="utf8")

		#schema = table_name.split('.')[0] if len(table_name.split('.')) > 1 else None
		schema = 'rappidpro'
		if schema is not None:
			if table_name=='staging_rpp_rpp_ftbl_msgs_msg':
				dataframe.to_sql(
					name = table_name,
					schema= schema,
					con=self.engine,
					if_exists=self.write_disposition,
					index=False,
					dtype={'text': types.NVARCHAR(length=65535)},
					chunksize=1000)
			elif table_name=='staging_rpp_ftbl_flows_flowrun':
				dataframe.to_sql(
					name = table_name,
					schema= schema,
					con=self.engine,
					if_exists=self.write_disposition,
					index=False,
					dtype={'results': types.NVARCHAR(length=65535)},
					chunksize=1000)
			elif table_name=='staging_rpp_ftbl_contact':
				dataframe.to_sql(
					name=table_name,
					schema=schema,
					con=self.engine,
					if_exists=self.write_disposition,
					index=False,
					dtype={'name': types.NVARCHAR(length=65535)},
					chunksize=1000)
			else:
				dataframe.to_sql(
					name=table_name,
					schema=schema,
					con=self.engine,
					if_exists=self.write_disposition,
					index=False,
					chunksize=1000)
		else:
			dataframe.to_sql(
				name=table_name,
				con=self.engine,
				if_exists=self.write_disposition,
				index=False,
				chunksize=1000)

		return None

	def drop(self, table_name):
		self.sql = f'drop table if exists {table_name}' 
		self.connect()
		try:
			with self.conn.cursor() as curr:
				curr.execute(self.sql)
				
			self.conn.commit()
			
		except Exception as e:
			logger.log_error(f'Query error: {e}')
			raise
			
		finally:
			curr.close()
			self.conn.close()
			logger.log_info(f'Closed connection to {self.db}.')
		
		return None
	
	def update(self, file_name, *param):
		self.open_query(file_name=file_name)

		try:
			if param:
				self.sql = self.sql.format(*param)

		except Exception as e:
			logger.log_error(f'Query format error: {e}')
			raise

		self.connect()

		try:
			with self.conn.cursor() as curr:
				curr.execute(self.sql)

			self.conn.commit()
			
		except Exception as e:
			logger.log_error(f'Query error: {e}')
			raise
			
		finally:
			curr.close()
			self.conn.close()
			logger.log_info(f'Closed connection to {self.db}.')

		return None
	
	def query(self, file_name, *param):
		self.open_query(file_name=file_name)

		try:
			if param:
				self.sql = self.sql.format(*param)

		except Exception as e:
			logger.log_error(f'Query format error: {e}')
			raise

		res = self.execute()

		return res