# comanda/tests/test_database_manager.py

import pytest
from comanda.connection.database_manager import DatabaseManager

@pytest.fixture
def db_manager():
    manager = DatabaseManager()
    yield manager
    manager.close_connection()

def test_get_table_names(db_manager):
    table_names = db_manager.get_table_names()
    assert isinstance(table_names, list)

def test_get_column_names(db_manager):
    table_name = 'usuarios'  # Cambia esto por el nombre de una tabla real
    column_names = db_manager.get_column_names(table_name)
    assert isinstance(column_names, list)

def test_get_table_data(db_manager):
    table_name = 'usuarios'  # Cambia esto por el nombre de una tabla real
    column_names, rows = db_manager.get_table_data(table_name)
    assert isinstance(column_names, list)
    assert isinstance(rows, list)
