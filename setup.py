# coding: utf-8

from setuptools import setup

setup(
    name='ooxml_to_latex',
    version="0.0.4",
    package_dir={'': 'src'},
    packages=["ooxml_to_latex"],
    url='https://github.com/qmagico/oxml_to_latex_parser',
    license='MIT',
    author='qmagico',
    author_email='iury@qmagico.com.br',
    description='Open office xml to latex parser ',
    install_requires=['lxml']
)
