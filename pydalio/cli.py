import os
from pathlib import Path
import logging

import typer

from pydalio.constants import MAX_LEN_CASE_DESCR, YAML_PATH_ENV_VAR
from pydalio.db import add_row_to_principles_table
from pydalio.principle import yaml_loader
from pydalio.utils import setup_environment
from pydalio.db import create_db
from pydalio.db import initiliaze_tables


logging.basicConfig(
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.INFO,
)

app = typer.Typer()

@app.command()
def check_principles():
    """Perfom a check of your principles on a case you are facing"""
    # Load the principles through the .yaml file
    #TODO: for future make .env file optional and add .yaml file / db file as options
    setup_environment()
    _yaml_path = Path(os.getenv(YAML_PATH_ENV_VAR))
    principles = yaml_loader(_yaml_path)
    # TODO: check principles are still in alignment with database tables

    # Prompt principles
    case_descr = typer.prompt("What is this case about? Please describe in 1 sentence (max. 100 characters)", type=str)
    if len(case_descr) > MAX_LEN_CASE_DESCR:
        raise ValueError(f"The case should be less then {MAX_LEN_CASE_DESCR} characters long.")
    responses: list[str] = [case_descr]
    for p in principles:
        response_id = p.prompt()
        responses.append(p.get_option_str_from_id(response_id))
        typer.echo("\n") # Create a single line of space around the prompts
    # TODO: give overview of what user has filled in to confirm BEFORE entry in database
    # TODO: ask on final decision what the decision is you are going to do
    add_row_to_principles_table(principles, responses)

@app.command()
def initial_setup():
    """Initial setup to create database with correct structure and load principles into database"""
    create_db()
    initiliaze_tables()

@app.command()
def overview():
    """Display all principles decisions in a structured manner for user"""
    pass