from os import path
from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst')) as file_readme:
    long_description = file_readme.read()


setup(
    name='crossword',
    version='0.1.2',
    description='Python library for handling crossword puzzles',
    long_description=long_description,
    url='https://github.com/svisser/crossword',
    author='Simeon Visser',
    author_email='simeonvisser@gmail.com',
    license='MIT',
    packages=['crossword'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='crossword puzzle ipuz'
)
