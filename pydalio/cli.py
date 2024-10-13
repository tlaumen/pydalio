import os
from pathlib import Path
import logging

import typer

from pydalio.constants import YAML_PATH_ENV_VARIABLE_KEY
from pydalio.principle import yaml_loader
from pydalio.utils import setup_environment


logging.basicConfig(
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.INFO,
)

app = typer.Typer()

@app.command()
def check_principles():
    # Load the principles through the .yaml file
    #TODO: for future make .env file optional and add .yaml file / db file as options
    setup_environment()
    _yaml_path = Path(os.getenv(YAML_PATH_ENV_VARIABLE_KEY))
    principles = yaml_loader(_yaml_path)

    # Prompt principles
    responses: list[str] = []
    for p in principles:
        response_id = p.prompt()
        responses.append(p.get_option_str_from_id(response_id))
        typer.echo("\n") # Create a single line of space around the prompts

@app.command()
def overview():
    pass