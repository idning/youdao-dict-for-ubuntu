#!/usr/bin/env python
from setuptools import setup
import sys
import platform

__VERSION__ = "0.1.0"

requires = []

setup(
    name = "youdao_dict",
    version = __VERSION__,
    url = 'http://idning.github.com/',
    author = 'ning',
    author_email = 'idning@gmail.com',
    description = "youdao dict for ubuntu",
    long_description=open('README.rst').read(),
    packages = ['youdao_dict'],
    scripts = ['youdao_dict/dict.py'],
    include_package_data = True,
    install_requires = requires,
    classifiers = ['Development Status :: 5 - Production/Stable',
                   'Environment :: Console',
                   'License :: OSI Approved :: GNU Affero General Public License v3',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   ],
)

