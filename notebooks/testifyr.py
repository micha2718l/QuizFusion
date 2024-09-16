import matplotlib

matplotlib.use("agg")

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
//.question {
//    page-break-inside: avoid;
//}
.problem {
    font-size: 1em;
    page-break-inside: avoid;
    padding-left: 0.5em;
    padding-right: 0.5em;
    padding-top: 0.1em;
    padding-bottom: 0.1em;
}
.problem_info {
    font-size: 1.2em;
    font-weight: bold;
}
.question {
    font-size: 1em;
    page-break-inside: avoid;
}
.question_info {
    font-size: 0.8em;
    font-weight: bold;
}
.extra_info {
    font-size: 0.8em;
    font-weight: bold;
    width: 50%;
    text-align: center;
    border: 2px solid black;
    margin: 1em;
    padding: 1em;
}
.extra_item {
    font-size: 1.1em;
}
.bonus {
    page-break-inside: avoid;
    border: 2px solid black;
    font-size: 1em;
    margin-top: 1em;
    margin-bottom: 1em;
    margin-left: 1.5em;
    margin-right: 1.5em;
    padding: 0.2em
}
.bonus_info {
    font-size: 1.2em;
    font-weight: bold;
}
.problem ol {
    list-style-type: upper-alpha;
}
.problem img {
    max-width: 100%;
    height: 15em;
}
.spacer_span {
    width: 5em;
    display: inline-block;
    border-bottom: 1px solid black;
}
.test_info {
    font-size: 0.8em;
    border: 1px solid black;
    text-align: center;
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
    points: int = 3

    def statement_html(self):
        return f"<p>\n\n {self.statement} \n\n</p>"

    def space_string(self):
        return ("*" * 10 + "\n") * self.space if self.space else ""

    def space_html(self):
        return f"""<div
                        class="spaceBox"
                        style="height: calc(1em * {self.space or 0}); display: {"default" if self.space else "none"};"
                    ></div>"""

    def html(self, number=None):
        if number:
            return f"<div class='question'><p><div class='question_info'> \n\n Question #{number} ({self.points} points) </div> \n\n {self.statement_html()} \n\n {self.space_html()} \n\n</p></div>"
        return f'<div class="question">\n\n {self.statement_html()} \n\n {self.space_html()} \n\n</div>'


@dataclass
class Choice:
    statement: str = ""
    correct: bool = False

    def html(self):
        return f"<div class='choice'>\n\n {self.statement} \n\n</div>"


@dataclass
class Problem:
    statement: str = ""
    figure: str = ""
    extras: List[str] = field(default_factory=list)

    @property
    def points(self):
        if isinstance(self, MultipleChoiceProblem):
            return 3
        elif isinstance(self, WorkProblem):
            return sum([q.points for q in self.questions])

    def content_html(self):
        if self.figure:
            return f"<div>\n\n {self.statement} \n\n <img src='data:image/png;base64, {self.figure.decode('utf-8')}'/> \n\n</div>"
        return f"<div>\n\n {self.statement} \n\n</div>"

    def html(self, number=None):
        if number:
            return f"<div class='problem'><p><div class='problem_info'> \n\n Problem #{number} ({self.points} points) </div> \n\n {self.content_html()} \n\n</p></div>"
        return f"<div class='problem'><p>\n\n {self.content_html()} \n\n</p></div>"

    def show(self):
        styled_print(self.html())


@dataclass
class MultipleChoiceProblem(Problem):
    choices: List[Choice] = field(default_factory=list)

    def content_html(self):
        out = super().content_html()
        out += "<ol>\n"
        for choice in self.choices:
            out += f"<li>\n\n {choice.html()} \n\n</li>"
        out += "</ol>\n"
        return out


@dataclass
class WorkProblem(Problem):
    questions: List[Question] = field(default_factory=list)

    def content_html(self):
        out = super().content_html()
        if self.extras:
            out += "<div class='extra_info'> Extra information \n\n"
            for extra in self.extras:
                out += f"<div class='extra_item'>\n\n {extra} \n\n</div>\n"
            out += "</div> \n\n"
        for i, question in enumerate(self.questions, start=1):
            out += question.html(number=i)
        return out


@dataclass
class Bonus:
    statement: str = ""
    points: int = 3

    def html(self, number=0):
        return f"<div class='bonus'><p><div class='bonus_info'> \n\n Bonus #{number} ({self.points} points) </div> \n\n {self.statement} \n\n</p></div>"

    def show(self):
        styled_print(self.html())


@dataclass
class Test:
    metadata: Dict[str, Any] = field(default_factory=dict)
    problems: List[Problem] = field(default_factory=list)

    def show(self):
        styled_print(self.html())

    def total_points(self):
        points = 0
        for problem in self.problems:
            if isinstance(problem, MultipleChoiceProblem):
                points += 3
            elif isinstance(problem, WorkProblem):
                points += len(problem.questions) * 3
            else:
                pass
        return {
            "total": points,
            "bonus": sum(
                [p.points if isinstance(p, Bonus) else 0 for p in self.problems]
            ),
        }

    def html(self):
        points = self.total_points()
        out = f"<div class='test_info'> \n\n Score: <span class='spacer_span'></span> / {points['total']} + Bonus: <span class='spacer_span'></span> / {points['bonus']} = Total: <span class='spacer_span'></span> / {points['total']} || Final: <span class='spacer_span'></span>% -> [A, B, C, D, F]</div> \n\n"

        for i, problem in enumerate(self.problems, start=1):
            out += problem.html(number=i)
        return out
