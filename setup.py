from setuptools import setup, find_packages

setup(
    name='ticket-to-ride',
    version='1.0.0',
    description='Ticket to ride with autonomous agents',
    author='UNAL',
    author_email='me@unal.edu.co',
    packages=find_packages(exclude=('tests'))
)