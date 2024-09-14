import matplotlib

matplotlib.use("agg")

from typing import List, Tuple, Dict, Any, Union
import sympy as sp
import numpy as np

import matplotlib.pyplot as plt


from IPython.display import HTML, Latex, Markdown, display

import pint

ureg = pint.UnitRegistry()
pint.set_application_registry(ureg)

lt = sp.latex
sp.init_printing()


def nbprint(string):
    display(Markdown(str(string)))


def ordered_list(items):
    out = "\n<ol type='a'>\n"
    for item in items:
        out += f"<li>\n\n {item} \n\n</li> \n"
    out += f"</ol>\n"
    return out


class Question:
    def __init__(self, question: str, points: int, space: str = ""):
        self.question = question
        self.points = points
        self.space = space

    def space_string(self):
        return """
<div style="
    border: 2px solid black;
    width: 100%;
    box-sizing: border-box;
    line-height: 1em;
    height: calc(1em * 10);
    page-break-inside: avoid;">
    <!-- Content goes here -->
</div>
"""


class Choice:
    def __init__(self, choice: str, correct: bool = False):
        self.choice = choice
        self.correct = correct

    def __str__(self):
        return str(self.choice)

    def __repr__(self):
        return self.__str__()


class Problem:
    def __init__(
        self,
        statement: str,
        questions: List[Question],
        number: int = 1,
        extras: List[str] = [],
        fig: str = None,
    ):
        self.questions = questions
        self.statement = statement
        self.number = number
        self.extras = extras
        self.fig = fig

    def __str__(self):
        out = f"# Problem #{self.number} ({sum(q.points for q in self.questions)} Points)\n"
        out += f"## {self.statement}\n"
        if self.extras:
            out += "<div>Extra information</div>\n"
            out += ordered_list(self.extras)
        for i, q in enumerate(self.questions, start=1):
            out += f"\n\n<div class='question'>Question {i} ({q.points} Points)\n\n"
            out += q.question + "\n\n"
            out += q.space_string() + "\n</div>"
        return out

    def __repr__(self):
        return self.__str__()


class ProblemSet:
    def __init__(self, problems: List[Problem], title: str = "Calculation Problems"):
        self.problems = problems
        self.title = title

    def __str__(self):
        out = f"# {self.title}\n"
        for p in self.problems:
            out += str(p)
        return out

    def __repr__(self):
        return self.__str__()


class Value(pint.Quantity):
    def __new__(cls, value=1, unit="", sigfigs=3, pre_zeros=0):
        # Create a new instance of the class using the pint.Quantity factory
        # This is why we need to use super().__new__ instead of super().__init__
        obj = super().__new__(cls, value, unit)
        obj.sigfigs = sigfigs
        obj.pre_zeros = pre_zeros
        return obj

    def __format__(self, format_spec):
        if format_spec:
            self.sigfigs = int(format_spec)
        unit = self.units
        if isinstance(unit, pint.Unit):
            match self.units:
                case ureg.degree:
                    unit = r"^\circ"
                case _:
                    unit = f"{unit:~L}"
        return f"${'0'*self.pre_zeros}{self.magnitude:#.{self.sigfigs}g} {unit}$"

    def __repr__(self):
        return self.__format__(None)

    def __str__(self):
        return self.__repr__()


class MultipleChoice:
    def __init__(self, statement: str, choices: List[Choice]):
        self.statement = statement
        self.choices = choices

    def __str__(self):
        out = f"### {self.statement}\n"
        out += ordered_list(self.choices)
        return out

    def __repr__(self):
        return self.__str__()
