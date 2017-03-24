from setuptools import setup, find_packages
import sys, os

version = '0.1.0'

with open('README.rst') as file_:
    long_description = file_.read()

setup(name='pyplot',
      version=version,
      description="Module to centralize plotting scripts.",
      long_description=long_description,
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Andreas Weh',
      author_email='andreas.weh@web.de',
      url='https://github.com/DerWeh/pyplot/',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests', '*.test', '*.test.*']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points={
          'console_scripts': [
              'pyplot = pyplot.__main__:main',
          ],
      },
      )
