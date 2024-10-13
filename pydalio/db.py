from pathlib import Path
import sqlite3
import os
from contextlib import closing

from pydalio.principle import Principle, yaml_loader
from pydalio.constants import DB_NAME, YAML_PATH_ENV_VARIABLE_KEY
from pydalio.utils import setup_environment
from pydalio.constants import DB_PATH_ENV_VARIABLE_KEY

def create_db(db_folder: Path):
    conn = sqlite3.connect(db_folder / DB_NAME)
    conn.close()

def initiliaze_tables(db_path: Path, principles: list[Principle]):
    """
    Creates a few tables: 
        - 1 table to track all results entered
        - a table for every principle to preserve the result space of every principle. E.g.: principle: be busy, result space: not busy, little busy, busy. If very busy is added to this in future datamodels, this should be done explicitly and not be possible implicitly/automatically.
    """
    setup_environment()

    # Based on https://martinheinz.dev/blog/34
    with closing(sqlite3.connect(db_path)) as conn:
        with conn:
            _create_principles_table(conn, principles)
            for i, p in enumerate(principles, start=1):
                _create_principle_table(conn, p, i)
                _fill_principle_table(conn, p, i)
            conn.commit()

def _create_principles_table_query(principles: list[Principle]) -> str:
    """Creates query to create table with all principles results"""
    create_table_query: str = "CREATE TABLE principles(principle_id INT PRIMARY KEY, case_ STRING NOT NULL, "
    for i, p in enumerate(principles, start=1):
        create_table_query += f"principle{i} {p.result_type.name} NOT NULL" 
        create_table_query += ", " if i != len(principles) else ""
    create_table_query += ")"
    return create_table_query

def _create_principles_table(db_conn, principles: list[Principle]):
    """Creates table that stores all principles results"""
    db_conn.cursor().execute(_create_principles_table_query(principles))

def _create_principle_table_query(id_: int, principle: Principle) -> str:
    """Creates query to create table for principle with all possible options"""
    create_table_query: str = f"CREATE TABLE principle{id_}(id INTEGER, "
    create_table_query += "question STRING NOT NULL, "
    for i in range(1, len(principle.options)+1):
        create_table_query += f"option{i} {principle.result_type.name} NOT NULL" 
        create_table_query += ", " if i != len(principle.options) else ""
    create_table_query += ")"
    return create_table_query

def _create_principle_table(db_conn, principle: Principle, id_: int):
    """Creates a table for a principle containing the principle and all options"""
    db_conn.cursor().execute(_create_principle_table_query(id_, principle))

def _fill_principle_query(id_: int, principle: Principle) -> str:
    """Creates query to create table for principle with all possible options"""
    insert_principle_query: str = f"INSERT INTO principle{id_} (id, question, "
    for i in range(1, len(principle.options)+1):
        insert_principle_query += f"option{i}"
        insert_principle_query += ", " if i != len(principle.options) else ""
    insert_principle_query += ") VALUES ("
    insert_principle_query += f"{id_}, "
    insert_principle_query += f"'{principle.question}', "
    for i, option in enumerate(principle.options, start=1):
        insert_principle_query += f"'{option.explanation}'" 
        insert_principle_query += ", " if i != len(principle.options) else ""
    insert_principle_query += ")"
    return insert_principle_query

def _fill_principle_table(db_conn, principle: Principle, id_: int):
    """Fills the principle table with the information of a principle"""
    db_conn.cursor().execute(_fill_principle_query(id_, principle))