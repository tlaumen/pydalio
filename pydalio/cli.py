import os
from pathlib import Path

import typer
from dotenv import load_dotenv

from pydalio.constants import YAML_PATH_ENV_VARIABLE_KEY
from pydalio.principle import yaml_loader

app = typer.Typer()

def setup_environment():
    path_env_vars = typer.prompt("The environment variables for the DB and principles yaml are not yet set.\nWhat is the path to the environment variables?", type=str)
    typer.echo("\n")
    if not Path(path_env_vars).exists():
        raise ValueError(f"The path: {path_env_vars} to the environment variables does not exist.")
    load_dotenv(path_env_vars)


@app.command()
def check_principles():
    # Load the principles through the .yaml file
    #TODO: for future make .env file optional and add .yaml file / db file as options
    if YAML_PATH_ENV_VARIABLE_KEY not in os.environ:
        setup_environment()
    _yaml_path = Path(os.getenv(YAML_PATH_ENV_VARIABLE_KEY))
    principles = yaml_loader(_yaml_path)

    # Prompt principles
    responses: list[str] = []
    for p in principles:
        response_id = p.prompt()
        responses.append(p.get_option_str_from_id(response_id))
        typer.echo("\n") # Create a single line of space around the prompts
    print(responses)

@app.command()
def overview():
    pass