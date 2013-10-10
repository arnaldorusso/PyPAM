#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.md').read()
history = open('HISTORY.md').read().replace('.. :changelog:', '')

setup(
    name='PyPAM',
    version='0.1.0',
    description='PyPAM - Read light curves and photosynthetic yield values, obtained from PyhtoPAM equipment. Extract values as: alpha, Ik, ETR(max) and Beta.',
    long_description=readme + '\n\n' + history,
    author='Arnaldo Russo',
    author_email='arnaldorusso@gmail.com',
    url='https://github.com/arnaldorusso/PyPAM',
    packages=[
        'PyPAM',
    ],
    package_dir={'PyPAM': 'PyPAM'},
    include_package_data=True,
    install_requires=[
    ],
    license="PSF",
    zip_safe=False,
    keywords='PyPAM, Pulse Amplitude Modulate, Photosynthesis, Fluorescence, Electron Transport Rate (ETR), Primary Production, Phytoplankton',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Python Software Foundation License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
)
