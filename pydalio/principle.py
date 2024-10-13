from dataclasses import dataclass
from typing import Optional
from itertools import pairwise
from itertools import combinations
from pathlib import Path
from copy import copy
from enum import Enum

import typer
import yaml

class ResultType(Enum):
    TEXT = 0
    INTEGER = 1


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
    result_type: ResultType = ResultType.TEXT # sets db value

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

    def _create_prompt_text(self) -> str:
        # Prompt text starts with the question/statement
        text = copy(self.question) 
        
        # Text could be a question or a statement. In case it is a statement, add colon for nicer layout
        if self.question[-1] != "?":
            text += ":"

        # Add all options to text
        for option in self.options:
            text += f"\n\t{option}"
        
        # Add explanation what to do
        text += f"\nSelect your option by providing one the corresponding number: {self._option_ids}"
        return text

    def prompt(self):
        """Presents questions and options with typer for user input"""
        valid_response: bool = False
        while not valid_response:
            response: int = typer.prompt(self._create_prompt_text(), type=int)
            valid_response = self._is_response_valid(response)
        return response
    
    def get_option_str_from_id(self, id_: int) -> str:
        option_mapping: dict[int, str] = {option.id_: option.explanation for option in self.options}
        if id_ not in option_mapping:
            raise ValueError(f"The requested id is a valid option with principle: {self}")
        return option_mapping[id_]

def _principle_factory(dict_: dict[str, list[str]]) -> list[Principle]:
    """Gets principles as keys and options as values of dictionary"""
    principles: list[Principle] = []
    for question, options in dict_.items():
        principles.append(
            Principle(
                question=question,
                options=[Option(id_=i, explanation=expl) for i, expl in enumerate(options, start=1)]
            )
        )
    return principles

def yaml_loader(path: Path) -> list[Principle]:
    if not path.exists():
        raise ValueError(f"The path {path} to the .yaml file does not exist!")
    with open(path) as f:
        dict_ = yaml.safe_load(f)
    return _principle_factory(dict_)