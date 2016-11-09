#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""Bidirectional OSC bridge for SunVox DLL"""

import io
import os
import re
import sys
from glob import glob

from setuptools import find_packages
from setuptools import setup

SETUP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(SETUP_DIR)
import sunvosc  # NOQA isort:skip


def read(*names, **kwargs):
    return io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


setup(
    name='sunvosc',
    version=sunvosc.__version__,
    license='MIT',
    description=__doc__,
    long_description='%s\n%s' % (
        re.compile(r'^\.\.\s+start-badges.*^\.\.\s+end-badges', re.M | re.S).sub('', read('README.rst')),
        re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))
    ),
    author='Matthew Scott',
    author_email='matt@11craft.com',
    url='https://github.com/metrasynth/sunvosc',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[os.path.splitext(os.path.basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Utilities',
    ],
    keywords=[
        'sunvox',
        'osc',
        'audio',
        'music',
        'sound',
        'tracker',
    ],
    install_requires=[
        # eg: 'aspectlib==1.1.1', 'six>=1.7',
        'begins',
        'python-osc',
        'sounddevice',
        'sunvox-dll-python',
    ],
    extras_require={
        # eg:
        #   'rst': ['docutils>=0.11'],
        #   ':python_version=="2.6"': ['argparse'],
    },
    entry_points={
        'console_scripts': [
            'sunvosc = sunvosc.cli:main.start',
        ]
    },
)
