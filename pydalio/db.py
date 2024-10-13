from pathlib import Path
import sqlite3
from contextlib import closing
import os

from pydalio.principle import Principle, yaml_loader
from pydalio.constants import DB_NAME, DB_PATH_ENV_VAR, PRINCIPLES_TABLE_NAME, YAML_PATH_ENV_VAR
from pydalio.utils import setup_environment

def create_db():
    setup_environment()
    db_path = Path(os.getenv(DB_PATH_ENV_VAR)) / DB_NAME 
    conn = sqlite3.connect(db_path)
    conn.close()

def initiliaze_tables():
    """
    Creates a few tables: 
        - 1 table to track all results entered
        - a table for every principle to preserve the result space of every principle. E.g.: principle: be busy, result space: not busy, little busy, busy. If very busy is added to this in future datamodels, this should be done explicitly and not be possible implicitly/automatically.
    """
    setup_environment()

    # Load principles from .yaml file
    principles: list[Principle] = yaml_loader(Path(os.getenv(YAML_PATH_ENV_VAR)))

    # Based on https://martinheinz.dev/blog/34
    db_path = Path(os.getenv(DB_PATH_ENV_VAR)) / DB_NAME 
    with closing(sqlite3.connect(db_path)) as conn:
        with conn:
            _create_principles_table(conn, principles)
            for p in principles:
                _create_principle_table(conn, p, principles)
                _fill_principle_table(conn, p, principles)
            conn.commit()

def from_principle_to_db_col(principle: Principle, all_principles: list[Principle]) -> str:
    """Creates appropriate column name for principle for principles table"""
    for i, p in enumerate(all_principles, start=1):
        if p == principle:
            return f"principle{i}"
    raise ValueError(f"The provided principle: {principle} is not in the list of all principles:{all_principles}. Please make sure this is the case!")

def _create_principles_table_query(principles: list[Principle]) -> str:
    """Creates query to create table with all principles results"""
    principle_columns: list[str] = [f"{from_principle_to_db_col(p, principles)} {p.result_type.name} NOT NULL" for p in principles]
    # TODO: add date and time of response in database --> important data on decision moment!
    # TODO: add final decision to database: YES/NO/POSTPONE 
    return f"CREATE TABLE {PRINCIPLES_TABLE_NAME}(case_ TEXT NOT NULL, {', '.join(principle_columns)})"

def _create_principles_table(db_conn, principles: list[Principle]):
    """Creates table that stores all principles results"""
    db_conn.cursor().execute(_create_principles_table_query(principles))

def _create_principle_table_query(principle: Principle, principles: list[Principle]) -> str:
    """Creates query to create table for principle with all possible options"""
    option_columns: list[str] = [f"option{i} {principle.result_type.name} NOT NULL" for i in range(1, len(principle.options)+1)]
    return f"CREATE TABLE {from_principle_to_db_col(principle, principles)}(question TEXT NOT NULL, {', '.join(option_columns)})"

def _create_principle_table(db_conn, principle: Principle, principles: list[Principle]):
    """Creates a table for a principle containing the principle and all options"""
    db_conn.cursor().execute(_create_principle_table_query(principle, principles))

def _add_encapsuling_apostrophe(text: str) -> str:
    """
    Encapsulates string with apostrophes
    Example: This is a sentence -> 'This is a sentence'
    """
    return f"'{text}'"

def _add_row_to_table_query(table: str, columns: list[str], values: list[str]) -> str:
    """Base function to add row to table"""
    if len(values) != len(columns):
        raise ValueError(f"The columns and values have different lengths. This cannot be the case.\nColumns: {columns}\nValues: {values}")
    
    # Encapsulate strings with spaces with apostrophe for sqlite command
    columns_: list[str] = [_add_encapsuling_apostrophe(c) if " " in c else c for c in columns]
    values_: list[str] = [_add_encapsuling_apostrophe(v) if " " in v else v for v in values]
    return f"INSERT INTO {table} ({', '.join(columns_)}) VALUES ({', '.join(values_)})"
    
def _fill_principle_query(principle: Principle, principles: list[Principle]) -> str:
    """Creates query to fill table for principle"""
    table: str = from_principle_to_db_col(principle, principles)
    columns: list[str] = ["question"] + [f"option{i}" for i in range(1, len(principle.options)+1)]
    values: list[str] = [principle.question] + [option.explanation for option in principle.options]
    return _add_row_to_table_query(table=table, columns=columns, values=values)

def _fill_principle_table(db_conn, principle: Principle, principles):
    """Fills the principle table with the information of a principle"""
    db_conn.cursor().execute(_fill_principle_query(principle, principles))

def add_row_to_principles_table(principles: list[Principle], responses: list[str]):
    """Gets the user input of principle and inputs it into the db"""
    if len(principles) + 1 != len(responses): # len(principles) + 1 because the case description is also a response
        raise ValueError(f"The number of responses does not match the number columns in the principles table. This should be the case.\nPrinciples: case_, {','.join([p.question for p in principles])}\nResponses: {responses}")
    table: str = PRINCIPLES_TABLE_NAME
    columns: list[str] = ["case_"] + [from_principle_to_db_col(p, principles) for p in principles]
    values: list[str] = responses
    
    db_path = Path(os.getenv(DB_PATH_ENV_VAR)) / DB_NAME 
    with closing(sqlite3.connect(db_path)) as conn:
        with conn:
            conn.cursor().execute(_add_row_to_table_query(table, columns, values))
            conn.commit()


    
    
