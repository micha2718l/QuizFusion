import subprocess

templates = [
    "asciidoc",
    "base",
    "basic",
    "classic",
    "compatibility",
    "lab",
    "latex",
    "markdown",
    "python",
    "reveal",
    "rst",
    "script",
    "webpdf",
]

for template in templates:
    with open("Templates/exam/conf.json", "w") as f:
        f.write(
            f"""
{{
  "base_template": "{template}",
  "mimetypes": {{
    "text/html": true
  }}
}}
"""
        )
    subprocess.run(["python", "test.py", "--pdf", "--file", "notebooks/testify.ipynb"])
    subprocess.run(["mv", "out/testify.pdf", f"out/testify_{template}.pdf"])
