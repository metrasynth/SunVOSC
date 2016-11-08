========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |requires|
        |
    * - package
      - |version| |downloads| |wheel|

.. |docs| image:: https://readthedocs.org/projects/sunvosc/badge/?style=flat
    :target: https://readthedocs.org/projects/sunvosc
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/metrasynth/SunVOSC.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/metrasynth/SunVOSC

.. |requires| image:: https://requires.io/github/metrasynth/sunvosc/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/metrasynth/sunvosc/requirements/?branch=master

.. |version| image:: https://img.shields.io/pypi/v/sunvosc.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/sunvosc

.. |downloads| image:: https://img.shields.io/pypi/dm/sunvosc.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/sunvosc

.. |wheel| image:: https://img.shields.io/pypi/wheel/sunvosc.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/sunvosc

.. end-badges

Bidirectional OSC bridge for SunVox DLL

* Free software: MIT license

Installation
============

::

    pip install sunvosc

Documentation
=============

https://sunvosc.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
