# setup.py
from setuptools import setup, find_packages

setup(
    name='dna_parser',
    version='0.1',
    packages=find_packages(),
    install_requires=['Pillow'],
    entry_points={
        'console_scripts': [
            'dna_parser=dna_parser.main:main',
        ],
    },
)