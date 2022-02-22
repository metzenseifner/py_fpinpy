#!/usr/bin/env python

from setuptools import setup, find_packages, find_namespace_packages
import pathlib

PWD = pathlib.Path(__file__).parent

README = (PWD / "README.md").read_text()

# https://docs.python.org/3/distutils/setupscript.html#meta-data
setup(name='fpinpy',
      version='1.1.1',
      description='A functional library for Python.',
      long_description=README,
      long_description_content_type='text/markdown',
      author='Jonathan L. Komar',
      author_email='jonathan.komar@uibk.ac.at',
      license='MIT',
      classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
        "Topic :: Software Development :: Libraries",
      ],
      url='https://github.com/metzenseifner/py_fpinpy',
      package_dir={'': 'src/main'},
      packages=find_packages(where='src/main', exclude=()),
      install_requires=[''],
      setup_requires=['wheel'],
      tests_require=['pytest', 'pyhamcrest'],
     )
