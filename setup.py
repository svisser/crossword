import ast
from os import path
import re
from setuptools import setup

here = path.abspath(path.dirname(__file__))

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open(path.join(here, 'README.rst')) as file_readme:
    long_description = file_readme.read()

with open('crossword/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))


setup(
    name='crossword',
    version=version,
    description='Python library for handling crossword puzzles',
    long_description=long_description,
    url='https://github.com/svisser/crossword',
    author='Simeon Visser',
    author_email='simeonvisser@gmail.com',
    license='MIT',
    packages=['crossword'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Games/Entertainment :: Puzzle Games',
    ],
    keywords='crossword puzzle ipuz puz'
)
