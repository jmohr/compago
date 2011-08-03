import sys
from setuptools import setup, find_packages

if sys.version_info[0] == 2 and sys.version_info[1] < 7:
  install_requires = ['argparse']
else:
  install_requires = []

setup(
    name = 'compago',
    description = 'A framework for simple command-line option parsing.',
    author = 'Justin Mohr',
    author_email = 'jmohr@bytepulse.net',
    packages = find_packages(exclude=['*.test.*', '*.test']),
    version = '1.2',
    install_requires = install_requires,
    license = 'BSD',
    url = 'http://github.com/jmohr/compago',
    package_data = {'':['README']},
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development',
    ]
)
