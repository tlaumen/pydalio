from pathlib import Path
import logging
import os

import typer
from dotenv import load_dotenv

from pydalio.constants import DB_PATH_ENV_VAR, YAML_PATH_ENV_VAR


def setup_environment():
    if DB_PATH_ENV_VAR not in os.environ or YAML_PATH_ENV_VAR not in os.environ:
        logging.info("Environment variables are not yet set")
        path_env_vars = typer.prompt("The environment variables for the DB and principles yaml are not yet set.\nWhat is the path to the environment variables?", type=str)
        typer.echo("\n")
        if not Path(path_env_vars).exists():
            raise ValueError(f"The path: {path_env_vars} to the environment variables does not exist.")
        load_dotenv(path_env_vars)
    else:
        logging.info("Environment variables are already set")
        
