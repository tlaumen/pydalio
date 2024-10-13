from pathlib import Path

from pydalio.principle import yaml_loader
from pydalio.db import _create_principles_table_query
from pydalio.db import _create_principle_table_query
from pydalio.db import _fill_principle_query

_ = Path(__file__).parent / "test_principles.yaml"
principles = yaml_loader(_)

def test_db_queries():
    query = _create_principles_table_query(principles)
    assert query == "CREATE TABLE principles(id INTEGER PRIMARY KEY, case_ TEXT NOT NULL, principle1 TEXT NOT NULL, principle2 TEXT NOT NULL)"
    query = _create_principle_table_query(id_=1, principle=principles[0])
    assert query == "CREATE TABLE principle1(id INTEGER, question TEXT NOT NULL, option1 TEXT NOT NULL, option2 TEXT NOT NULL, option3 TEXT NOT NULL)"
    query = _fill_principle_query(id_=1, principle=principles[0])
    assert query == "INSERT INTO principle1 (id, question, option1, option2, option3) VALUES (1, 'This is a test principle', 'Option 1', 'Option 2', 'Option 3')"