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

from tribuna.content.behaviors.behaviors import ITags


def create_article(container, title, subject=[]):
    """Creates an article, publishes it, adaps it and runs our 'tags_new'
    property setter so the needed tags are automatically built etc.

    We need this because behaviors don't seem to work automatically in tests,
    so we need adapt each Article after creation.
    """

    article = api.content.create(
        container=container,
        type='tribuna.content.article',
        title=title,
    )
    api.content.transition(obj=article, transition='publish')
    adapter = ITags(article)
    adapter.tags_new = subject
    article.reindexObject()

    return adapter


def populate_dummy(portal):
    """Populate the portal with some dummy data useful for tests. We need some
    articles with different tags, some of the tags should be highlighted.
    """

    article_fld = portal['articles-folder']
    # Create some articles with combinations of 3 tags

    create_article(
        container=article_fld,
        title="Article 1a",
        subject=['tag1'],
    )
    create_article(
        container=article_fld,
        title="Article 2a",
        subject=['tag2'],
    )
    create_article(
        container=article_fld,
        title="Article1a",
        subject=['tag3'],
    )
    create_article(
        container=article_fld,
        title="Article 1b",
        subject=['tag1'],
    )
    create_article(
        container=article_fld,
        title="Article 12a",
        subject=['tag1', 'tag2'],
    )
    create_article(
        container=article_fld,
        title="Article 123a",
        subject=['tag1', 'tag2', 'tag3'],
    )

    create_article(
        container=article_fld,
        title="Article H",
        subject=['htag'],
    )
    create_article(
        container=article_fld,
        title="Article H2a",
        subject=['htag', 'tag2'],
    )

    # htag is highlighted in navigation
    portal['tags-folder']['htag'].highlight_in_navigation = True


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
