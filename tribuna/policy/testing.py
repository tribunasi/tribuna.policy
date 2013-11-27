#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
"""Base module for unittesting."""

from plone import api
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import login
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.testing import z2

import unittest2 as unittest


class Session(dict):
    """Dummy session class to use in tests."""
    def set(self, key, value):
        self[key] = value

    def getSessionData(self, create=True):
        return self


def session_populate_portlet_data(session):
    """Function that populates portlet_data in session with default values."""

    session.set('portlet_data', Session())
    session['portlet_data']['tags'] = []
    session['portlet_data']['content_filters'] = []
    session['portlet_data']['all_tags'] = []
    session['portlet_data']['sort_order'] = 'descending'
    session['portlet_data']['sort_on'] = 'latest'


class TribunaPolicyLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        # Load ZCML
        import tribuna.policy
        self.loadZCML(package=tribuna.policy)
        z2.installProduct(app, 'tribuna.policy')

    def setUpPloneSite(self, portal):
        """Set up Plone."""

        # set up default workflow
        wft = api.portal.get_tool('portal_workflow')
        wft.setDefaultChain('simple_publication_workflow')

        # Install into Plone site using portal_setup
        applyProfile(portal, 'tribuna.policy:default')

        # Login and create some test content
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        portal.invokeFactory('Folder', 'folder')

        # Commit so that the test browser sees these objects
        portal.portal_catalog.clearFindAndRebuild()
        import transaction
        transaction.commit()

    def tearDownZope(self, app):
        """Tear down Zope."""
        z2.uninstallProduct(app, 'tribuna.policy')


FIXTURE = TribunaPolicyLayer()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name="TribunaPolicyLayer:Integration")
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name="TribunaPolicyLayer:Functional")


class IntegrationTestCase(unittest.TestCase):
    """Base class for integration tests."""

    layer = INTEGRATION_TESTING


class FunctionalTestCase(unittest.TestCase):
    """Base class for functional tests."""

    layer = FUNCTIONAL_TESTING
