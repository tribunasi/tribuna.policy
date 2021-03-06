#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Installer for the tribuna.policy package."""

from setuptools import find_packages
from setuptools import setup

import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = \
    read('README.rst') + \
    read('docs', 'CHANGELOG.rst') + \
    read('docs', 'LICENSE.rst')

setup(
    name='tribuna.policy',
    version='0.2dev',
    description="Policy package for Tribuna webpage",
    long_description=long_description,
    # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
    ],
    keywords='tribuna, policy',
    author='Termitnjak d.o.o.',
    author_email='info@termitnjak.si',
    url='',
    license='MIT',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['tribuna'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'collective.z3cform.widgets',
        'five.grok',
        'five.pt',
        # needed if we re-enable populator.py,
        #'loremipsum',
        'mobile.sniffer',
        'Pillow',
        'Plone',
        'plone.api',
        'plone.app.jquerytools',
        'plone.app.caching',
        'plone.formwidget.captcha',
        'setuptools',
        'tribuna.annotator',
        'tribuna.content',
        'tribuna.diazotheme',
        'collective.cookiecuttr',
        'z3c.jbot'
    ],
    extras_require={
        'test': [
            'mock',
            'plone.app.testing',
            'unittest2',
        ],
        'develop': [
            'coverage',
            'flake8',
            'i18ndude',
            'jarn.mkrelease',
            'loremipsum',
            'niteoweb.loginas',
            'plone.app.debugtoolbar',
            'plone.reload',
            'Products.Clouseau',
            'Products.DocFinderTab',
            'Products.PDBDebugMode',
            'Products.PrintingMailHost',
            'Sphinx',
            'zest.releaser',
            'zptlint',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
