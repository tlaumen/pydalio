import typer

from pydalio.principle import Principle
from pydalio.principle import Option

app = typer.Typer()
principle1 = Principle("Principle 1: ...", options=[Option(id_=1, explanation="This is the first option")])

@app.command()
def principles_check():
    principle1.echo()


if __name__ == "__main__":
    app()

