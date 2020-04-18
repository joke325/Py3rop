#!/usr/bin/env python

from setuptools import setup

setup(
    name='Py3rop',
    version='0.1.0',
    author='Janky',
    author_email='box@janky.tech',
    description='Python bidings for RNP OpenPGP library',
    packages=['pyrop', 'pyrop.rop'],
    python_requires='~=3.7',
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent"
        "License :: OSI Approved :: BSD License"
    ]
)
