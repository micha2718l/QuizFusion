from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

from IPython.display import Markdown, display


style_string = """<style>
.spaceBox {
    border: 2px solid black;
    width: 100%;
    box-sizing: border-box;
    line-height: 1em;
    height: calc(1em * 10);
    page-break-inside: avoid;
}
</style>"""


def styled_print(string: str):
    display(Markdown(style_string + string))


def ordered_list(items):
    out = "\n<ol type='a'>\n"
    for item in items:
        out += f"<li>\n\n {item} \n\n</li> \n"
    out += f"</ol>\n"
    return out


@dataclass
class Question:
    statement: str = ""
    space: Optional[int] = None

    def statement_html(self):
        return f"<p>\n\n {self.statement} \n\n</p>"

    def space_string(self):
        return ("*" * 10 + "\n") * self.space if self.space else ""

    def space_html(self):
        return f"""<div
                        class="spaceBox"
                        style="height: calc(1em * {self.space or 0}); display: {"default" if self.space else "none"};"
                    ></div>"""

    def html(self):
        return f'<div class="question">\n\n {self.statement_html()} \n\n {self.space_html()} \n\n</div>'


@dataclass
class Choice:
    choice: str = ""
    correct: bool = False


@dataclass
class Problem:
    statement: str = ""

    def show(self):
        styled_print(self.html())


@dataclass
class MultipleChoiceProblem(Problem):
    choices: List[Choice] = field(default_factory=list)

    def html(self):
        out = f"<h3>\n\n {self.statement} \n\n</h3>"
        out += "<ul>\n"
        for choice in self.choices:
            out += f"<li>\n\n {choice.choice} \n\n</li>"
        out += "</ul>\n"
        return out


@dataclass
class WorkProblem(Problem):
    questions: List[Question] = field(default_factory=list)

    def print(self):
        print(f"Problem: {self.statement}")
        for question in self.questions:
            print(f"Question: {question.statement}")
            print(question.space_string())
            print()

    def html(self):
        out = f"<h3>\n\n {self.statement} \n\n</h3>"
        for question in self.questions:
            out += question.html()
        return out


@dataclass
class Test:
    metadata: Dict[str, Any] = field(default_factory=dict)
    problems: List[Problem] = field(default_factory=list)

    def show(self):
        styled_print(self.html())

    def html(self):
        out = ""
        for problem in self.problems:
            out += problem.html()
        return out
