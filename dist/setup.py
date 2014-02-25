#!/usr/bin/env python

from setuptools import find_packages
from distutils.core import setup

EXCLUDE_FROM_PACKAGES = []

setup(name='edc',
      version='1.3.0',
      description='EDC supporting modules',
      author='Erik van Widenfelt',
      author_email='ew2789@gmail.com',
      packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
      license='BSD',
      long_description=open('README.rst').read(),
      )
