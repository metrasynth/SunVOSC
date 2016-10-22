========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        |
    * - package
      - |version| |downloads| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/sunvosc/badge/?style=flat
    :target: https://readthedocs.org/projects/sunvosc
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/metrasynth/sunvosc.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/metrasynth/sunvosc

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/metrasynth/sunvosc?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/metrasynth/sunvosc

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

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/sunvosc.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/sunvosc

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/sunvosc.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/sunvosc


.. end-badges

Bidirectional OSC bridge for SunVox DLL

* Free software: BSD license

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
