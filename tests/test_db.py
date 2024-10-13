from pathlib import Path

from pydalio.principle import yaml_loader
from pydalio.db import _create_principles_table_query
from pydalio.db import _create_principle_table_query

_ = Path(__file__).parent / "test_principles.yaml"
principles = yaml_loader(_)

def test_db_queries():
    query = _create_principles_table_query(principles)
    assert query == "CREATE TABLE principles(id INTEGER PRIMARY KEY, case TEXT NOT NULL, principle1 TEXT NOT NULL, principle2 TEXT NOT NULL)"
    query = _create_principle_table_query(id_=1, principle=principles[0])
    assert query == "CREATE TABLE principle1(id INTEGER FOREIGN KEY, question STRING NOT NULL, option1 TEXT NOT NULL, option2 TEXT NOT NULL, option3 TEXT NOT NULL)"