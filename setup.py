#!/usr/bin/env python
from setuptools import setup

setup(name='pyFacebookAPI',
      version='3.6.2',
      description='Python Facebook bot api. ',
      author='ufuran',
      author_email='ufuran.ivan@gmail.com',
      url='https://github.com/ufuran/pyFacebookApi',
      packages=['facebot'],
      license='GPL2',
      keywords='facebook bot api tools',
      install_requires=['requests', 'six'],
      extras_require={
          'json': 'ujson',
      }
      )
