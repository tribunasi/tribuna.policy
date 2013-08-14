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
    version='0.1',
    description="Policy package for Tribuna project",
    long_description=long_description,
    # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
    ],
    keywords='tribuna, policy',
    author='Termitnjak Ltd.',
    author_email='info@termitnjak.com',
    url='',
    license='BSD',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['tribuna'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'collective.z3cform.widgets',
        'eea.tags',
        'five.grok',
        'five.pt',
        'mobile.sniffer',
        'Pillow',
        'Plone',
        'plone.api',
        'plone.app.jquerytools',
        'plone.formwidget.captcha',
        'setuptools',
        'tribuna.content',
        'tribuna.diazotheme',
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
            'plone.reload',
            'Products.Clouseau',
            'Products.DocFinderTab',
            'Products.PDBDebugMode',
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
