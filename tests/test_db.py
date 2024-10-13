from pathlib import Path

from pydalio.principle import yaml_loader
from pydalio.db import _create_principles_table_query
from pydalio.db import _create_principle_table_query
from pydalio.db import _fill_principle_query

_ = Path(__file__).parent / "test_principles.yaml"
principles = yaml_loader(_)

def test_db_query_principles_table():
    query = _create_principles_table_query(principles)
    assert query == "CREATE TABLE principles(case_ TEXT NOT NULL, principle1 TEXT NOT NULL, principle2 TEXT NOT NULL)"

def test_db_query_principle_table():
    query = _create_principle_table_query(principle=principles[0], principles=principles)
    assert query == "CREATE TABLE principle1(question TEXT NOT NULL, option1 TEXT NOT NULL, option2 TEXT NOT NULL, option3 TEXT NOT NULL)"

def test_db_query_insert_principle():
    query = _fill_principle_query(principle=principles[0], principles=principles)
    assert query == "INSERT INTO principle1 (question, option1, option2, option3) VALUES ('This is a test principle', 'Option 1', 'Option 2', 'Option 3')"