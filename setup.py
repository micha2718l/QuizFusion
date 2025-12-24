from setuptools import setup, find_packages

setup(
    name="quizfusion",
    version="0.1.0",
    description="A toolkit for generating, editing, and exporting quizzes and tests",
    author="Michael Haas",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "nbconvert",
        "nbformat",
        "matplotlib",
        "numpy",
        "ipython",
        "jinja2",
    ],
    entry_points={
        "console_scripts": [
            "quizfusion-convert=scripts.test:main",
        ],
    },
)
