from pathlib import Path
import os

from pydalio import db
from pydalio.cli import app
from pydalio.constants import DB_NAME, YAML_PATH_ENV_VARIABLE_KEY
from pydalio.principle import yaml_loader
from pydalio.db import create_db, initiliaze_tables

db_path = Path(__file__).parent / DB_NAME
# try:
create_db(Path(__file__).parent)
initiliaze_tables(db_path=db_path, principles=yaml_loader(Path(__file__).parent / "example_principles.yaml"))
# app()
# finally:
#     os.remove(db_path