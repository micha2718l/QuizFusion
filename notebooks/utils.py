from typing import List, Tuple, Dict, Any, Union
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

from IPython.display import HTML, Latex, Markdown, display


lt = sp.latex
sp.init_printing()


def nbprint(string):
    display(Markdown(str(string)))


def pmath(sym, ret=False, pre="", post="", preM="", postM=""):
    output = f"{pre}${preM}{lt(sym)}{postM}${post}"
    if ret:
        return output
    nbprint(output)


# string with sigfigs
def sf(val: float, sigfigs: int = 3):
    return f"{val:#.{sigfigs}g}"


def units(unit: str):
    match unit:
        case "degree":
            unit = r"^\circ"
        case "m/s":
            unit = r"\mathrm{\frac{m}{s}}"
        case "blarks per zoomer":
            unit = r"\mathrm{\frac{blarks}{zoomer}}"
        case _:
            unit = rf"\mathrm{{{unit}}}"
    return unit


# string with units
def wu(val: float, unit: str, sigfigs: int = 3):
    return rf"${sf(val, sigfigs=sigfigs)} {units(unit)}$"


class Question:
    def __init__(self, question: str, points: int, space: str):
        self.question = question
        self.points = points
        self.space = space

    def space_string(self):
        return """
<div style="
    border: 2px solid black;
    width: 100%;
    box-sizing: border-box;
    line-height: 1.5em;
    height: calc(1.5em * 5);">
    <!-- Content goes here -->
</div>
"""


class Problem:
    def __init__(
        self,
        statement: str,
        questions: List[Question],
        number: int = 1,
        extra: str = "",
    ):
        self.questions = questions
        self.statement = statement
        self.number = number
        self.extra = extra

    def __str__(self):
        out = f"# Problem #{self.number} ({sum(q.points for q in self.questions)} Points)\n"
        out += f"## {self.statement}\n"
        for i, q in enumerate(self.questions, start=1):
            out += f"### Question {i} ({q.points} Points)\n"
            out += q.question + "\n"
            out += q.space_string() + "\n"
        return out

    def __repr__(self):
        return self.__str__()
