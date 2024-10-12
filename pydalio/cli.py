import typer

from pydalio.principle import Principle
from pydalio.principle import Option

app = typer.Typer()
principle1 = Principle("Principle 1: ...", options=[Option(id_=1, explanation="This is the first option"), Option(id_=2, explanation="Option 2")])

@app.command()
def check_principles():
    a = principle1.prompt()
    
@app.command()
def overview():
    pass