#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2011-2013, The Format Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

from setuptools import setup
from glob import glob

__author__ = "Evan Bolyen"
__copyright__ = "Copyright 2011-2013"
__credits__ = ["Evan Bolyen"]
__license__ = "BSD"
__version__ = "0.1.0-dev"
__maintainer__ = "Evan Bolyen"
__email__ = "ebolyen@gmail.com"

long_description = """Chart things from QIIME output"""

classes = """
    Development Status :: 4 - Beta
    License :: OSI Approved :: BSD License
    Topic :: Scientific/Engineering :: Bio-Informatics
    Topic :: Software Development :: Libraries :: Application Frameworks
    Topic :: Software Development :: Libraries :: Python Modules
    Programming Language :: Python
    Programming Language :: Python :: 2.7
    Programming Language :: Python :: Implementation :: CPython
    Operating System :: OS Independent
    Operating System :: POSIX :: Linux
    Operating System :: MacOS :: MacOS X
"""
classifiers = [s.strip() for s in classes.split('\n') if s]

setup(name='qiimecharts',
    version=__version__,
    description='Create charts from QIIME output',
    long_description=long_description,
    license=__license__,
    author=__maintainer__,
    author_email=__email__,
    maintainer=__maintainer__,
    maintainer_email=__email__,
    url='', #TODO
    packages=['qiimecharts',
              'qiimecharts/commands',
              'qiimecharts/core',
              'qiimecharts/core/charts',
              'qiimecharts/core/colors',
              'qiimecharts/core/groups',
              'qiimecharts/interfaces',
              'qiimecharts/interfaces/optparse',
              'qiimecharts/interfaces/optparse/config',
              ],
    scripts=glob('scripts/*'),
    install_requires=["numpy >= 1.3.0",
                      "pyqi == 0.3.1-dev"],
    dependency_links=[
        "git+https://github.com/bipy/pyqi.git#egg=pyqi-0.3.1-dev"
    ],
    extras_require={'scipy_sparse':["scipy >= 0.9.0"],
                    'test':["nose >= 0.10.1",
                            "tox >= 1.6.1"]
                   }
)
