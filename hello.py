import eel
from notebooks.testifyr import WorkProblem, Question, Test, MultipleChoiceProblem, Choice, Bonus
from notebooks.stuff import Value, Unit

# Set web files folder and optionally specify which file types to check for eel.expose()
#   *Default allowed_extensions are: ['.js', '.html', '.txt', '.htm', '.xhtml']
eel.init("web", allowed_extensions=[".js", ".html"])


@eel.expose  # Expose this function to Javascript
def say_hello_py(x):
    print("Hello from %s" % x)

def effify(non_f_str: str):
    return eval(f'f"""{non_f_str}"""', None, {'a': 9.81})

@eel.expose
def show_problem(statement: str):
    t = Value(3.5, "s")
    a = Value(-9.81, 'm/s^2')
    statement = effify(statement)
    questions = [
        Question("Determine the velocity of the stone when it hits the ground.",
                11,
                answer=f"$v_y=v_0+at$ \n\n where $v_0=0$; $a=-g=$ {a}; $v_y=$ {a} {t} \n\n $v_y=$ {a * t} ."),
        Question("Determine the height of the building.",
                11,
                answer=f"$y=y_0+v_{{0_y}}t+\\frac{1}{2}at^2$ \n\n where $y_0=0$; $v_{{0_y}}=0$; $a=$ {a} \n\n $y=$ {(a * t ** 2) / 2} \n\n $h=|y|=$ {abs(a * t ** 2 / 2)}."),
    ]
    wp = WorkProblem(statement, questions=questions)
    h = wp.html()
    return str(h)

@eel.expose
def sand():
    return "sand"

say_hello_py("Python World!")

eel.start(
    "hello.html", size=(800, 600),
    mode="chrome-app"
)  # Start (this blocks and enters loop)
