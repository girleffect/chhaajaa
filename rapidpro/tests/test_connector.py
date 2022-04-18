import os
import pytest
import sys

AUTO_CODE_PATH = os.environ.get('AUTO_CODE_PATH')
sys.path.append(f'{AUTO_CODE_PATH}')


from helpers.connector import SQlServer

class TestConnector:
	def test_get_environment_variables(self, monkeypatch):
		# Arrange
		monkeypatch.setenv("MSSQL_DB", "Test_DB")
		monkeypatch.setenv("MSSQL_HOST", "Test_HOST")
		monkeypatch.setenv("MSSQL_USER", "Test_USER")
		monkeypatch.setenv("MSSQL_PASSWORD", "Test_PASSWORD")
		
		# Act
		server = SQlServer()

		# Assert
		assert server.db == "Test_DB"
		assert server.server == "Test_HOST"
		assert server.pw == "Test_PASSWORD"
		assert server.user == "Test_USER"

	@pytest.mark.parametrize("empty_input", [None, ''])
	def test_fail_to_get_environment_variables_catchs_oserror(self, empty_input, monkeypatch):
		# Arrange
		if empty_input is not None:
			monkeypatch.setenv("MSSQL_DB", empty_input)
		else:
			monkeypatch.delenv("MSSQL_DB")
		
		# Act
		server = SQlServer()

		# Assert Exception
		with pytest.raises(OSError):
			server.connect()

	def test_failing_to_open_sql_file_catchs_exception(self):
		# Act
		server = SQlServer()

		#Assert Exception
		with pytest.raises(Exception):
			server.open_query("")

	def test_failing_to_call_query_with_mock_open_query(self, mocker):
		# Arrange
		mocker.patch('helpers.connector.SQlServer.open_query')

		# Act
		server = SQlServer()

		#Assert & Assert Exception
		with pytest.raises(Exception):
			server.query("")
