#!/usr/bin/env python

from setuptools import setup, find_packages, find_namespace_packages
import pathlib

PWD = pathlib.Path(__file__).parent

README = (PWD / "README.md").read_text()

# https://docs.python.org/3/distutils/setupscript.html#meta-data
setup(name='fpinpy',
      version='1.0.0',
      description='Python Functional Library',
      long_description=README,
      long_description_content_type='text/markdown',
      author='Jonathan L. Komar',
      author_email='jonathan.komar@uibk.ac.at',
      license='MIT',
      classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
      ],
      url='https://github.com/metzenseifner/py_fpinpy',
      # keys are package names, whereby empty string means root package and keys define distribution root dir
      package_dir={'': 'src/main'},
      packages=find_packages(where='src/main', exclude=()), # list of paths
      install_requires=[''],
      setup_requires=[''],
      tests_require=[''],
      #entry_points={},
      #package_data=[]
     )
