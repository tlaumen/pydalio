from pathlib import Path

import pytest

from pydalio.principle import Option, Principle, yaml_loader


option1 = Option(id_=1, explanation="test question 1")
option2 = Option(id_=2, explanation="test question 2", value=2)
option3 = Option(id_=3, explanation="test question 3", value=1)
option4 = Option(id_=4, explanation="test question 4", value=0)

def test_option():
    assert isinstance(option1, Option)
    assert option2.value == 2

def test_principle():
    principle = Principle(question="This is a test principle", options=[option1, option2, option3])
    assert isinstance(principle, Principle)

    with pytest.raises(ValueError):
        _ = Principle(question="This principle is not allowed", options=[])

    # Not allowed because not adjacent numbers: 1, 2, 4
    with pytest.raises(ValueError):
        _ = Principle(question="This principle is not allowed", options=[option1, option2, option4])
    
    # Not allowed becuase not starting with 1
    with pytest.raises(ValueError):
        _ = Principle(question="This principle is not allowed", options=[option2, option3, option4])
    
    # Not allowed becuase the options should be unique
    with pytest.raises(ValueError):
        _ = Principle(question="This principle is not allowed", options=[option1, option1, option2])

def test_yaml_loader():
    yaml_path = Path(__file__).parent / "test_principles.yaml"
    principles = yaml_loader(yaml_path)
    assert all([isinstance(p, Principle) for p in principles])
    
    principle1, principle2 = principles[0], principles[1]
    assert principle1.question == "This is a test principle"
    assert principle2.question == "This is a second test principle"
    assert principle1.options[1].explanation == "Option 2"
