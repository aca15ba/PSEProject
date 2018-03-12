import re

from setuptools import setup, find_packages

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('evaluator/evaluator.py').read(),
    re.M
    ).group(1)

setup(
    name="evaluator",
    version= version,
    packages=find_packages(),
    entry_points = {
        "console_scripts": ['evaluator = evaluator.evaluator:main']
        },
    description = "Python command line application to evaluate source code style.",
    author = "Babatunde N. Adeola",
    author_email = "babatunde.adeola12@yahoo.com",
)
