import matplotlib

matplotlib.use("agg")

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

from IPython.display import Markdown, display

with open("testifyr.css", "r") as f:
    style_string = "<style>" + f.read() + "</style>"


def _styled_print(string: str):
    display(Markdown(style_string + string))


@dataclass
class Question:
    statement: str = ""
    space: Optional[int] = None
    points: int = 3
    answer: str = ""
    figure: Optional[str] = None

    def statement_html(self):
        return f"<p>\n\n {self.statement} \n\n</p>"

    def space_string(self):
        return ("*" * 10 + "\n") * self.space if self.space else ""

    def space_html(self, answers=False):
        out = f"""<div class="fig_space_container">
        <div
                        class="spaceBox"
                        style="height: calc(1em * {self.space or 0}); display: {"default" if self.space else "none"}; background-color: {'lightgreen' if answers else 'white'}"
                    >

{self.answer if answers else ""}

</div>"""
        if self.figure:
            out += f"""<div class="img_container"><img src='data:image/png;base64, {self.figure.decode('utf-8')}' style="height: calc(1em * {self.space or 0})"/></div>"""
        return out + "</div>"

    def html(self, number=None, answers=False):
        if number:
            return f"<div class='question'><p><div class='question_info'> \n\n Question #{number} ({self.points} points) </div> \n\n {self.statement_html()} \n\n {self.space_html(answers=answers)} \n\n</p></div>"
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
    figure_svg: str = ""
    extras: List[str] = field(default_factory=list)

    @property
    def points(self):
        if isinstance(self, MultipleChoiceProblem):
            return 3
        elif isinstance(self, WorkProblem):
            return sum([q.points for q in self.questions])

    def content_html(self, answers=False):
        out = f"<div>\n\n {self.statement} \n\n "
        if self.figure:
            out += f"<img src='data:image/png;base64, {self.figure.decode('utf-8')}'/>"
        if self.figure_svg:
            out += f"<div class='svg_container'>\n\n {self.figure_svg} \n\n</div>"
        out += "\n\n</div>"
        return out

    def html(self, number=None, answers=False):
        if number:
            return f"<div class='problem'><p><div class='problem_info'> \n\n Problem #{number} ({self.points} points) </div> \n\n {self.content_html(answers=answers)} \n\n</p></div>"
        return f"<div class='problem'><p>\n\n {self.content_html(answers=answers)} \n\n</p></div>"

    def show(self, answers=False):
        _styled_print(self.html(answers=answers))


@dataclass
class MultipleChoiceProblem(Problem):
    choices: List[Choice] = field(default_factory=list)

    def content_html(self, answers=False):
        def choice_class(correct):
            if answers:
                return "choice_correct" if correct else "choice_incorrect"
            return "choice"

        out = super().content_html()
        out += "<ol>\n"
        for choice in self.choices:
            out += f"<li class='{choice_class(choice.correct)}'>\n\n {choice.html()} \n\n</li>"
        out += "</ol>\n"
        return out


@dataclass
class WorkProblem(Problem):
    questions: List[Question] = field(default_factory=list)

    def content_html(self, answers=False):
        out = super().content_html()
        if self.extras:
            out += "<div class='extra_info'> Extra information \n\n"
            for extra in self.extras:
                out += f"<div class='extra_item'>\n\n {extra} \n\n</div>\n"
            out += "</div> \n\n"
        for i, question in enumerate(self.questions, start=1):
            out += question.html(number=i, answers=answers)
        return out


@dataclass
class Bonus:
    statement: str = ""
    points: int = 3
    answer: str = ""

    def answer_html(self, answers=False):
        if answers:
            return f"<span class='choice_correct'>\n{self.answer}\n</span>"
        return ""

    def html(self, number=0, answers=False):
        return f"<div class='bonus'><p><div class='bonus_info'> \n\n Bonus #{number} ({self.points} points) {self.answer_html(answers)}</div> \n\n {self.statement} \n\n</p></div>"

    def show(self, answers=False):
        _styled_print(self.html(answers=answers))


@dataclass
class Information:
    statement: str = ""
    points = None

    def html(self, number=0, answers=False):
        return f"<div class='information'><p>\n\n {self.statement} \n\n</p></div>"

    def show(self, answers=False):
        _styled_print(self.html(answers=answers))


@dataclass
class Test:
    metadata: Dict[str, Any] = field(default_factory=dict)
    problems: List[Problem] = field(default_factory=list)

    def show(self, answers=False):
        _styled_print(self.html(answers=answers))

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

    def html(self, answers=False):
        points = self.total_points()
        out = f"<div class='test_info_box'> <div class='test_info'> \n\n Score: <span class='spacer_span'></span> / {points['total']} + Bonus: <span class='spacer_span'></span> / {points['bonus']} = Total: <span class='spacer_span'></span> / {points['total']} || Final: <span class='spacer_span'></span>% -> [A, B, C, D, F]</div></div> \n\n"

        skip = 0
        for i, problem in enumerate(self.problems, start=1):
            if isinstance(problem, Information):
                skip += 1
            out += problem.html(number=i - skip, answers=answers)
        return out

    def get_grade_list(self):
        grades = []
        skip = 0
        for i, problem in enumerate(self.problems, start=1):
            if isinstance(problem, Information):
                skip += 1
                continue
            n = str(i - skip).zfill(2)
            if isinstance(problem, MultipleChoiceProblem):
                grades.append(f"P-{n}-MC(3)")
            elif isinstance(problem, WorkProblem):
                for j, q in enumerate(problem.questions):
                    grades.append(f"P-{n}-W{j}({q.points})")
            elif isinstance(problem, Bonus):
                grades.append(f"P-{n}-BN({problem.points})")
        return grades
