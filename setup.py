from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys, os
import subprocess

version_file = os.path.join(os.path.dirname(__file__), 'pyplot', '__version__.py')

try:  # create version from git tags
    version = str(subprocess.check_output(['git', 'describe', '--tags']).strip())
except subprocess.CalledProcessError:  # read exiting version if not possible
    with open(version_file, 'r') as file_:
        for line in file_.readlines():
            if "__version__" in line:
                version = line.strip().split('=')[-1].strip(" '")
                break
        else:
            raise ValueError("Could not read or generate version")
else: # save new version if one was generated
    with open(version_file, 'w') as file_:
        file_.writelines([
            '"""The package version"""\n',
            '# Do not change this file, it is automatically generated.\n'
            '__version__ = "' + version + '"',
        ])

with open('README.rst') as file_:
    long_description = file_.read()



class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        pytest.main(self.test_args)

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
          'argcomplete',
      ],
      entry_points={
          'console_scripts': [
              'pyplot = pyplot.__main__:main',
          ],
      },
      tests_require=['pytest'],
      cmdclass = {'test': PyTest},
      )
