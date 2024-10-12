from dataclasses import dataclass
from typing import Optional
from itertools import pairwise
from itertools import combinations

import typer

@dataclass
class Option:
    id_: int
    explanation: str
    value: Optional[int] = None

    def __str__(self) -> str:
        return f"{self.id_} - {self.explanation}"
@dataclass
class Principle:
    question: str
    options: list[Option]

    def __post_init__(self):
        if len(self.options) == 0:
            raise ValueError("No options are input, there should be at least 1 option given!")

        ids = [option.id_ for option in self.options]
        ids.sort()

        if ids[0] != 1:
            raise ValueError(f"One id values of principe object {self} options should be 1.")
        
        for id1, id2 in pairwise(ids):
            if id2 - id1 != 1:
                raise ValueError(f"All option id's should be adjacent numbers, i.e. 1, 2, 3, .... Instead, they are: {ids}")
        
        for id1, id2 in combinations(ids, 2):
            if id1 == id2:
                raise ValueError(f"All option should be unique. They are however: {self.options}")
    
    def echo(self):
        """Presents questions and options with typer for user input"""
        str_ = self.question 
        for option in self.options:
            str_ += f"\n{option}"
        typer.echo(str_)