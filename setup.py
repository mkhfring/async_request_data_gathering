from setuptools import setup, find_packages
import os.path
import re

# reading package's version (same way sqlalchemy does)
with open(
    os.path.join(os.path.dirname(__file__), 'async_requet', '__init__.py')
) as v_file:
    package_version = \
        re.compile('.*__version__ = \'(.*?)\'', re.S)\
        .match(v_file.read())\
        .group(1)


dependencies = [
    'balebot==1.6.12',
]


setup(
    name='async_requet',
    version=package_version,
    author='Mohamad Khajezade',
    author_email='khajezade.mohamad@gmail.com',
    description='A balebot to send async_requet reports',
    install_requires=dependencies,
    packages=find_packages(),
)
