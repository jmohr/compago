from setuptools import setup, find_packages

setup(
    name = 'compago',
    description = 'A framework for simple command-line option parsing.',
    author = 'Justin Mohr',
    author_email = 'jmohr@bytepulse.net',
    packages = find_packages(exclude=['*.test.*', '*.test']),
    version = '1.1',
    install_requires = ['argparse'],
    license = 'BSD',
    url = 'http://github.com/jmohr/compago',
    package_data = {'':['README']},
)
