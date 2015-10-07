# coding: utf-8

from setuptools import setup
from src import ooxml_to_latex

setup(
    name='ooxml_to_latex',
    version=ooxml_to_latex.__version__,
    package_dir={'': 'src'},
    packages=["ooxml_to_latex"],
    url='https://github.com/qmagico/oxml_to_latex_parser',
    license='MIT',
    author='qmagico',
    author_email='iury@qmagico.com.br',
    description='Open office xml to latex parser ',
    install_requires=['lxml']
)
