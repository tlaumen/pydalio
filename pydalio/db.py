from pathlib import Path
import sqlite3
from contextlib import closing

from pydalio.principle import Principle
from pydalio.constants import DB_NAME
from pydalio.utils import setup_environment

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

def from_principle_to_db_col(principle: Principle, all_principles: list[Principle]) -> str:
    """Creates appropriate column name for principle for principles table"""
    if principle not in all_principles:
        raise ValueError(f"The provided principle: {principle} is not in the list of all principles:{principles}. Please make sure this is the case!")
    for i, p in enumerate(all_principles, start=1):
        if p == principle:
            return f"principle{i}"

def _create_principles_table_query(principles: list[Principle]) -> str:
    """Creates query to create table with all principles results"""
    principle_columns: list[str] = [f"{from_principle_to_db_col(p, principles)} {p.result_type.name} NOT NULL" for p in principles]
    return f"CREATE TABLE principles(case_ TEXT NOT NULL, {', '.join(principle_columns)})"


def _create_principles_table(db_conn, principles: list[Principle]):
    """Creates table that stores all principles results"""
    db_conn.cursor().execute(_create_principles_table_query(principles))

def _create_principle_table_query(id_: int, principle: Principle) -> str:
    """Creates query to create table for principle with all possible options"""
    option_columns: list[str] = [f"option{i} {principle.result_type.name} NOT NULL" for i in range(1, len(principle.options)+1)]
    return f"CREATE TABLE principle{id_}(question TEXT NOT NULL, {', '.join(option_columns)})"

def _create_principle_table(db_conn, principle: Principle, id_: int):
    """Creates a table for a principle containing the principle and all options"""
    db_conn.cursor().execute(_create_principle_table_query(id_, principle))

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
    
def _fill_principle_query(id_: int, principle: Principle) -> str:
    """Creates query to fill table for principle"""
    table: str = f"principle{id_}"
    columns: list[str] = ["question"] + [f"option{i}" for i in range(1, len(principle.options)+1)]
    values: list[str] = [principle.question] + [option.explanation for option in principle.options]
    return _add_row_to_table_query(table=table, columns=columns, values=values)

def _fill_principle_table(db_conn, principle: Principle, id_: int):
    """Fills the principle table with the information of a principle"""
    db_conn.cursor().execute(_fill_principle_query(id_, principle))

def _add_row_to_principles_table():
    """Gets the user input of principle and inputs it into the db"""
    pass
