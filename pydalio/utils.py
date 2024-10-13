from pathlib import Path
import logging
import os

import typer
from dotenv import load_dotenv

from pydalio.constants import DB_PATH_ENV_VAR, YAML_PATH_ENV_VAR

def setup_environment():
    if DB_PATH_ENV_VAR not in os.environ or YAML_PATH_ENV_VAR not in os.environ:
        logging.info("Environment variables are not yet set")
        response = typer.prompt("The environment variables for the DB and principles yaml are not yet set.\nWhat is the path to the environment variables?", type=str)
        typer.echo("\n")
        path_env_vars: Path = Path(response)
        if path_env_vars.suffix != ".env":
            raise SyntaxError("The provided file should be file with suffix .env")
        if not path_env_vars.exists():
            raise ValueError(f"The path: {path_env_vars} to the .env file does not exist.")
        load_dotenv(path_env_vars)
        if DB_PATH_ENV_VAR not in os.environ or YAML_PATH_ENV_VAR not in os.environ:
            raise SyntaxError(f"Following environment variables: {YAML_PATH_ENV_VAR}, {DB_PATH_ENV_VAR} should be included in the .env file! One or more are currently missing.")
    else:
        logging.info("Environment variables are already set")
        
