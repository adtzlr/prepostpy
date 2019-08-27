# -*- coding: utf-8 -*-
# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='trusspy',
    version='2019.09.1',
    description='High-level scripting Interface for FEA Pre- and Postprocessing',
    long_description=readme,
    author='Andreas Dutzler',
    author_email='a.dutzler@gmail.com',
    url='https://github.com/adtzlr/prepostpy',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)