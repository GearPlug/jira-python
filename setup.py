import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='jira-python',
      version='0.2.1',
      description='API wrapper for Jira CRM written in Python',
      long_description=read('README.md'),
      url='https://github.com/GearPlug/jira-python',
      author='Miguel Ferrer',
      author_email='ingferrermiguel@gmail.com',
      license='GPL',
      packages=['jira'],
      zip_safe=False)
