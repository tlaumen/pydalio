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

    @property
    def _option_ids(self):
        ids = [_.id_ for _ in self.options]
        return ids

    def __post_init__(self):
        self.options.sort(key=lambda x:x.id_) # Sort the options to be sure they are shown in correct order and checks work

        if len(self.options) == 0:
            raise ValueError("No options are input, there should be at least 1 option given!")

        if self._option_ids[0] != 1:
            raise ValueError(f"One id values of principle object {self} options should be 1.")
        
        for id1, id2 in pairwise(self._option_ids):
            if id2 - id1 != 1:
                raise ValueError(f"All option id's should be adjacent numbers, i.e. 1, 2, 3, .... Instead, they are: {self._option_ids}")
        
        for id1, id2 in combinations(self._option_ids, 2):
            if id1 == id2:
                raise ValueError(f"All option should be unique. They are however: {self.options}")
    
    def _is_response_valid(self, response: int) -> bool:
        if not response in self._option_ids:
            msg = f"\nThe value {response} is not a valid response. Please enter one of the following responses: {self._option_ids}\n"
            styled_msg = typer.style(msg, fg=typer.colors.RED)
            typer.echo(styled_msg)
            return False
        return True

    def prompt(self):
        """Presents questions and options with typer for user input"""
        text = self.question 
        for option in self.options:
            text += f"\n\t{option}"
        text += f"\nSelect your option by providing one the corresponding number: {self._option_ids}"
        valid_response: bool = False
        while not valid_response:
            response: int = typer.prompt(text, type=int)
            valid_response = self._is_response_valid(response)
        return response